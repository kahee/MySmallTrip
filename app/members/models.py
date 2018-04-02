from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    img_profile = models.ImageField(upload_to='user', blank=True)
    nickname = models.CharField(max_length=20, blank=True)


class Member(models.Model):
    age = models.IntegerField('나이', blank=True)
    phonenumber = models.CharField('전화번호', max_length=15, blank=True)
    email = models.CharField('이메일', max_length=30)
    mypoint = models.IntegerField('내포인트', default=0)
    mycoupon = models.IntegerField('내쿠폰', default=0)
    isgetemail = models.BooleanField('메일수신여부체크',default=True)
    isgetsms = models.BooleanField('sms수신여부체크',default=True)
    isgetapppush = models.BooleanField('apppush수신여부체크',default=True)
    isusable = models.BooleanField('사용여부', default=True)
    creationdatetime = models.DateTimeField('생성시간', default=timezone.now)
    modifydatetime = models.DateTimeField('수정시간', default=timezone.now)
g