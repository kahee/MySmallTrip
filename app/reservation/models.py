from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.utils import timezone

from members.models import Member
from travel.models import Travel_Schedule, Travel_Information


class Reservation(models.Model):
    travel_Schedule = models.ForeignKey(
        Travel_Schedule,
        on_delete=models.CASCADE
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE

    )

    iscancled = models.BooleanField('취소여부', default=False)
    reversedpeople = models.IntegerField('예약수', default=0)
    concept = models.TextField('여행컨셉', blank=True)
    agegeneration = models.CharField('연령대',blank=True)
    personal_request = models.TextField('요청사항',blank=True)
    isusable = models.BooleanField('사용여부', default=True)
    creationdatetime = models.DateTimeField('생성시간', default=timezone.now)
    modifydatetime = models.DateTimeField('수정시간', default=timezone.now)


class RecentVisitPage(models.Model):
    travel_Schedule = models.ForeignKey(
        Travel_Schedule,
        on_delete=models.CASCADE)
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE)
    isusable = models.BooleanField('사용여부', default=True)
    creationdatetime = models.DateTimeField('생성시간', default=timezone.now)
    modifydatetime = models.DateTimeField('수정시간', default=timezone.now)


class WishList(models.Model):
    travel_info = models.ForeignKey(
        Travel_Information,
        on_delete=models.CASCADE
    )
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE
    )
    isusable = models.BooleanField('사용여부', default=True)
    creationdatetime = models.DateTimeField('생성시간', default=timezone.now)
    modifydatetime = models.DateTimeField('수정시간', default=timezone.now)
