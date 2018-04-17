import magic
from django.core.files import File
from imagekit.models import ImageSpecField
from io import BytesIO
from pilkit.processors import ResizeToFill, Image

from blog.models.blog import Blog
from blog.models.blog_base import BlogBase
from django.db import models


class BlogImage(BlogBase):
    blog_id = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='images'
    )
    img_field = models.ImageField('후기 이미지', upload_to='blog')
    img_thumbnail = models.ImageField(upload_to='blog-thumbnail')

    def save(self, *args, **kwargs):
        self._save_thumbnail_process()
        super().save(*args, **kwargs)

    def _save_thumbnail_process(self):
        if self.img_field:
            full_name = self.img_field.name.rsplit('/')[-1]
            full_name_split = full_name.rsplit('.', maxsplit=1)

            temp_file = BytesIO()
            temp_file.write(self.img_field.read())
            temp_file.seek(0)
            mime_info = magic.from_buffer(temp_file.read(), mime=True)
            temp_file.seek(0)

            name = full_name_split[0]
            ext = mime_info.split('/')[-1]

            im = Image.open(self.img_field)
            im.thumbnail((375, 199))
            im.save(temp_file, ext)

            self.img_thumbnail.save(
                f'{name}_thumbnail.{ext}',
                File(temp_file),
                save=False)
        else:
            self.img_thumbnail.delete(save=False)
