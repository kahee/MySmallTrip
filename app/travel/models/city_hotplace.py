from django.db import models

from .city_information import CityInformation
from .product_base import ProductBase


class CityHotplace(ProductBase):
    name = models.CharField('핫플레이스', max_length=20)
    city = models.ForeignKey(
        CityInformation,
        on_delete=models.CASCADE,
        verbose_name='city')

    def __str__(self):
        return self.name
