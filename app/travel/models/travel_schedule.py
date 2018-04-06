from django.db import models

from .product_base import ProductBase
from .travel_information import TravelInformation


class TravelSchedule(ProductBase):
    travel_info = models.ForeignKey(
        TravelInformation,
        on_delete=models.CASCADE,
        verbose_name='travel_info')
    start_date = models.DateField('여행시작날짜', auto_now_add=True)
    end_date = models.DateField('여행끝날짜', auto_now_add=True, blank=True)
    price = models.IntegerField('상품금액', default=0)
    price_descrption = models.TextField('상품금액 포함사항')

    maxPeople = models.IntegerField

    class Meta:
        ordering = ['-creation_datetime']

    def __str(self):
        return self.pk
