from blog.models.blog import Blog
from blog.models.blog_base import BlogBase
from django.db import models


class BlogImage(BlogBase):
    blog_id = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE
    )
    img_field = models.ImageField('후기 이미지', upload_to='blog')
