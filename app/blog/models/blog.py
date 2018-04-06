from django.db import models

from .blog_base import BlogBase
from reservation.models import Reservation


class Blog(BlogBase):
    travel_Reservation = models.OneToOneField(
        Reservation,
        on_delete=models.CASCADE,
        primary_key=True

    )
    title = models.CharField('후기제목', max_length=100)
    Contents = models.TextField('내용', blank=True, null=True)
    score = models.IntegerField('평점', default=5)

    class Meta:
        ordering = ['-modify_datetime']