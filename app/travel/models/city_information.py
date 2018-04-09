from .product_base import ProductBase
from django.db import models


class CityInformation(ProductBase):

    name = models.CharField('나라명', max_length=20)
    continent = models.CharField('대륙', max_length=20)
    nationality = models.CharField('나라', max_length=20)
    city_image = models.ImageField('도시이미지', upload_to='city')

    def __str__(self):
        return self.name
