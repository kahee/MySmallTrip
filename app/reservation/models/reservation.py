from django.conf import settings
from django.contrib.auth import get_user_model

from members.models import *
from reservation.models.reservation_base import ReservationBase
from travel.models import TravelSchedule

__all__ = (
    'Reservation',
)


class Reservation(ReservationBase):
    travel_Schedule = models.ForeignKey(
        TravelSchedule,
        on_delete=models.CASCADE,
        verbose_name='travel_schedule'
    )
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='user'

    )
    is_canceled = models.BooleanField('취소여부', default=False)
    reserve_people = models.IntegerField('예약수', default=1)
    concept = models.TextField('여행컨셉', blank=True)
    age_generation = models.CharField('연령대', blank=True, max_length=50)
    personal_request = models.TextField('요청사항', blank=True)

    class Meta:
        app_label = 'reservation'
