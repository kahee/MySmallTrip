from django.db import models

from travel.models import CityInformation, CompanyInformation
from .product_base import ProductBase


class TravelInformation(ProductBase):
    CATEGORY_TYPE_Ticket = 'ticket'
    CATEGORY_TYPE_Convenience = 'convenience'
    CATEGORY_TYPE_GuideTour = 'guide_tour'
    CATEGORY_TYPE_Restaurant = 'restaurant'
    CATEGORY_TYPE_Activity = 'activity'
    CATEGORY_TYPE_Accommodation = 'accomodation'
    CATEGORY_TYPE_Enjoy = 'enjoy'

    CHOICES_CATEGORY_TYPE = (
        (CATEGORY_TYPE_Ticket, '교통/티켓'),
        (CATEGORY_TYPE_Convenience, '여행편의'),
        (CATEGORY_TYPE_GuideTour, '가이드투어'),
        (CATEGORY_TYPE_Restaurant, '식당'),
        (CATEGORY_TYPE_Activity, '액티비티'),
        (CATEGORY_TYPE_Accommodation, '숙박/민박'),
        (CATEGORY_TYPE_Enjoy, '즐길거리')
    )

    travel_id = models.IntegerField('ID')

    name = models.CharField('상품명', max_length=200)
    category = models.CharField('카테고리', max_length=40, choices=CHOICES_CATEGORY_TYPE, blank=True)

    theme = models.CharField('테마', max_length=100, blank=True)
    # producttype 예시) 상품유형: 상품유형
    product_type = models.CharField('상품타입', max_length=100, blank=True)

    language = models.CharField('언어', max_length=40)
    city = models.ForeignKey(
        CityInformation,
        on_delete=models.CASCADE,
        verbose_name='city')
    time = models.CharField('소요시간',max_length=40)
    company = models.ForeignKey(
        CompanyInformation,
        on_delete=models.CASCADE,
        verbose_name='company')
    description = models.TextField('상품설명')
    meeting_time = models.CharField('만남시간', max_length=100)
    meeting_place = models.CharField('만남장소', max_length=100)
    
    price = models.IntegerField('상품금액', default=0)
    price_descrption = models.TextField('상품금액 포함사항')

    maxPeople = models.IntegerField('최대 사람 수')

    def __str__(self):
        return self.name
