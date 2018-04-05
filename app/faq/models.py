from django.db import models

# Create your models here.
from django.utils import timezone


class FrequentQuestion(models.Model):
    subject = models.CharField('주제', max_length=30)
    subject2 = models.CharField('소주제', max_length=20, blank=True)
    question = models.TextField('질문')
    answer = models.TextField('답변')
    isusable = models.BooleanField('사용여부', default=True)
    creationdatetime = models.DateTimeField('생성시간', default=timezone.now)
    modifydatetime = models.DateTimeField('수정시간', default=timezone.now)
