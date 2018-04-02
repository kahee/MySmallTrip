from django.db import models

# Create your models here.
from django.utils import timezone

from members.models import *
from travel.models import Travel_Schedule


class Blog(models.Model):
    travel_Schedule = models.OneToOneField(
        Travel_Schedule,
        on_delete=models.CASCADE,
        primary_key=True

    )
    title = models.CharField('후기제목', max_length=100)
    Contents = models.TextField('내용', blank=True, null=True)
    img_blog = models.ImageField('후기이미지', upload_to='blog')
    score = models.IntegerField('평점', default=5)
    isusable = models.BooleanField('사용여부', default=True)
    creationdatetime = models.DateTimeField('생성시간', default=timezone.now)
    modifydatetime = models.DateTimeField('수정시간', default=timezone.now)

    class Meta:
        ordering = ['-modifydatetime']

    # 1. 이미 후기가 등록된 경우에는 다시등록할때 수정하기로 바꿔주기?
    # 부모 클래스의 메서드를 호출해주는 것을 잊지마세요.
    # 예제 코드에서 super(Blog, self).save(*args, **kwargs) 를 호출함으로써, 실제로 데이터베이스에 객체가 저장되었습니다.
    # 부모 클래스의 메서드를 호출해주지 않는다면,
    # 실제 데이터베이스에는 아무런 동작도 일어나지 않습니다.
