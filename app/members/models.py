from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    # nickname을 추가하고
    # username =  models .CharField(max_length=20, blank=True)
    img_profile = models.ImageField(upload_to='user', blank=True)
    nickname = models.CharField(max_length=20, blank=True)
