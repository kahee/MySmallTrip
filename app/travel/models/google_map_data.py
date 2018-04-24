from travel.models import ProductBase
from django.db import models


class MapData(ProductBase):
    name = models.CharField('도시이름', max_length=100)
    address = models.CharField('주소', max_length=300)
    lat = models.FloatField('lat')
    lng = models.FloatField('lng')
    type = models.CharField('타입', max_length=50)
