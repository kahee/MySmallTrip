from django.db import models
from imagekit import ImageSpec, register
from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from .product_base import ProductBase
from .travel_information import TravelInformation

class TravelInformationImage(ProductBase):
    travel_id = models.ForeignKey(
        TravelInformation,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image_id = models.IntegerField(
        '이미지 ID'
    )
    product_image = models.ImageField('상품이미지', upload_to='product')
