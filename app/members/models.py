from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models, IntegrityError

# Create your models here.
from django.db.models.signals import pre_save
from django.dispatch import receiver


class User(AbstractUser):
    # 이름. 메일주소, 비밀번호, 비밀번호 확인,  프로필 이미지(페이스북 로그인시)
    email = models.CharField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )

    username = models.CharField(
        verbose_name='username',
        max_length=255,
    )

    img_profile = models.ImageField(
        verbose_name='프로필 사진',
        upload_to='user',
        blank=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


@receiver(pre_save, sender=User)
def user_create(sender, instance, **kwargs):
    try:
        validate_email(instance.email)

    except ValidationError:
        raise ValidationError('이메일 형식 오류')

    except IntegrityError:
        raise IntegrityError('이메일 중복')
