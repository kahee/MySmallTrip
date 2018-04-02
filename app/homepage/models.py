from django.db import models

# Create your models here.
from django.utils import timezone


class HomepageInfomation(models.Model):
    serviceinfo = models.TextField
    companyinfo = models.TextField
    qna = models.TextField
    isusable = models.BooleanField('사용여부')
    creationdatetime = models.DateTimeField('생성시간', default=timezone.now)
    modifydatetime = models.DateTimeField('수정시간', default=timezone.now)
