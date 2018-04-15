from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

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
    img_thumbnail = ImageSpecField(
        source='img_field',
        processors=[ResizeToFill(375, 199)],
        format='JPEG',
        options={'quality': 80}
    )
