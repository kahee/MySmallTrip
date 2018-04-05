from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models, IntegrityError

# Create your models here.
from django.db.models.signals import pre_save
from django.dispatch import receiver


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        # unique=True,
        blank=True,
    )
    img_profile = models.ImageField(
        verbose_name='Profile',
        upload_to='user',
        blank=True,
        null=True,
    )
    is_facebook_user = models.BooleanField(
        verbose_name='Facebook_user',
        default=False,
    )
    phone_number = models.CharField(
        verbose_name='Phone_number',
        max_length=100,
        blank=True,
        null=True,
    )

    certification_number = models.CharField('인증번호', blank=True, null=True, max_length=5)
    mypoint = models.IntegerField('내포인트', default=0, )
    mycoupon = models.IntegerField('내쿠폰', default=0, )
    isgetemail = models.BooleanField('메일수신여부체크', default=True)
    isgetsms = models.BooleanField('sms수신여부체크', default=True)
    isgetapppush = models.BooleanField('apppush수신여부체크', default=True)
    isusable = models.BooleanField('사용여부', default=True)
    creationdatetime = models.DateTimeField('생성시간', default=timezone.now)
    modifydatetime = models.DateTimeField('수정시간', default=timezone.now)

    REQUIRED_FIELDS = ['email', 'first_name']
