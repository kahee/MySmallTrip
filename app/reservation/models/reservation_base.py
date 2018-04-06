from members.models import *
from django.utils import timezone


class ReservationBase(models.Model):
    is_usable = models.BooleanField('사용여부', default=True)
    creation_datetime = models.DateTimeField('생성시간', default=timezone.now)
    modify_datetime = models.DateTimeField('수정시간', default=timezone.now)

    class Meta:
        abstract = True
