from django.utils import timezone

from django.db import models

from config import settings
from members.models import Member

User = settings.AUTH_USER_MODEL


class City_Information(models.Model):
    name = models.CharField('나라명', max_length=20)
    continent = models.CharField('대륙', max_length=20)
    nationality = models.CharField('나라', max_length=20)
    isusable = models.BooleanField('사용여부')
    creationdatetime = models.DateTimeField('생성시간', default=timezone.now)
    modifydatetime = models.DateTimeField('수정시간', default=timezone.now)

    def __str__(self):
        return self.name


class City_Hotplace(models.Model):
    name = models.CharField('핫플레이스', max_length=20)
    city = models.ForeignKey(
        City_Information,
        on_delete=models.CASCADE,
        verbose_name='city')
    isusable = models.BooleanField('사용여부')
    creationdatetime = models.DateTimeField('생성시간', default=timezone.now)
    modifydatetime = models.DateTimeField('수정시간', default=timezone.now)

    def __str__(self):
        return self.name


class Company_Information(models.Model):
    name = models.CharField('회사명', max_length=50)
    info = models.TextField('회사설명')
    isusable = models.BooleanField('사용여부')
    creationdatetime = models.DateTimeField('생성시간', default=timezone.now)
    modifydatetime = models.DateTimeField('수정시간', default=timezone.now)

    def __str__(self):
        return self.name


# Create your models here.
class Travel_Information(models.Model):
    CATEGORY_TYPE_Ticket = '교통/티켓'
    CATEGORY_TYPE_Convenience = '여행편의'
    CATEGORY_TYPE_GuidTour = '가이드투어'
    CATEGORY_TYPE_Restaurant = '식당'
    CATEGORY_TYPE_Activity = '액티비티'
    CATEGORY_TYPE_Accommodation = '숙박/민박'
    CATEGORY_TYPE_Enjoy = '즐길거리'

    CHOICES_CATEGORY_TYPE = (
        (CATEGORY_TYPE_Ticket, '교통/티켓'),
        (CATEGORY_TYPE_Convenience, '여행편의'),
        (CATEGORY_TYPE_GuidTour, '가이드투어'),
        (CATEGORY_TYPE_Restaurant, '식당'),
        (CATEGORY_TYPE_Activity, '액티비티'),
        (CATEGORY_TYPE_Accommodation, '숙박/민박'),
        (CATEGORY_TYPE_Enjoy, '즐길거리')
    )

    name = models.CharField('상품명', max_length=200)
    category = models.CharField('카테고리', max_length=10, choices=CHOICES_CATEGORY_TYPE, blank=True)

    theme = models.CharField('테마', max_length=100, blank=True)
    productType = models.CharField('상품타입', max_length=100, blank=True)
    language = models.CharField('언어', max_length=3)
    city = models.ForeignKey(
        City_Information,
        on_delete=models.CASCADE,
        verbose_name='city')
    time = models.IntegerField('소요시간')
    company = models.ForeignKey(
        Company_Information,
        on_delete=models.CASCADE,
        verbose_name='company')
    images = models.ImageField('이미지')
    description = models.TextField('상품설명')
    isusable = models.BooleanField('사용여부', default=True)
    creationdatetime = models.DateTimeField('생성시간', default=timezone.now)
    modifydatetime = models.DateTimeField('수정시간', default=timezone.now)

    def __str__(self):
        return self.name


class Travel_Schedule(models.Model):
    travel_info = models.ForeignKey(
        Travel_Information,
        on_delete=models.CASCADE,
        verbose_name='travelinfo')
    start_date = models.DateField('여행시작날짜', auto_now_add=True)
    end_date = models.DateField('여행마끝날짜', auto_now_add=True, blank=True)
    price = models.IntegerField('상품금액', default=0)
    price_descrption = models.TextField('상품금액 포함사항')

    maxPeople = models.IntegerField
    member = models.ManyToManyField(
        Member,
        through='Member',
        related_name='reserved_member',
        # blank=True
    )
    meetingTime = models.CharField('만남시간', max_length=100)
    mettingPlace = models.CharField('만남장소', max_length=100)
    isusable = models.BooleanField('사용여부', default=True)
    creationdatetime = models.DateTimeField('생성시간', default=timezone.now)
    modifydatetime = models.DateTimeField('수정시간', default=timezone.now)

    class Meta:
        ordering = ['-creationdatetime']

    def __str(self):
        return self.pk
