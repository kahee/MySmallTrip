from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models, IntegrityError
from travel.models import TravelInformation


class User(AbstractUser):
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        blank=True,
    )

    img_profile = models.ImageField(
        verbose_name='Profile',
        upload_to='user',
        blank=True,
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
    my_point = models.IntegerField('내포인트', default=0, )
    my_coupon = models.IntegerField('내쿠폰', default=0, )
    is_get_email = models.BooleanField('메일수신여부체크', default=True)
    is_get_sms = models.BooleanField('sms수신여부체크', default=True)
    is_get_app_push = models.BooleanField('apppush수신여부체크', default=True)
    is_usable = models.BooleanField('사용여부', default=True)
    creation_datetime = models.DateTimeField('생성시간', default=timezone.now)
    modify_datetime = models.DateTimeField('수정시간', default=timezone.now)

    wish_products = models.ManyToManyField(
        TravelInformation,
        through='reservation.WishTravel',
        related_name='wish_users',
        blank=True,
    )

    REQUIRED_FIELDS = ['email', 'first_name']


@receiver(post_delete, sender=User)
def photo_delete(sender, instance, **kwargs):
    # sender - 모델 객체가 옴
    # instance - 시그널이 발생된 모델 인스턴스가 온다.
    instance.file.delete(False)
