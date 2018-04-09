


from django.contrib.auth import get_user_model

from members.models import *
from reservation.models.reservation_base import ReservationBase
from travel.models import TravelSchedule

User = get_user_model()

class Reservation(ReservationBase):
    travel_Schedule = models.ForeignKey(
        TravelSchedule,
        on_delete=models.CASCADE
    )
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE

    )
    is_canceled = models.BooleanField('취소여부', default=False)
    reversed_people = models.IntegerField('예약수', default=0)
    concept = models.TextField('여행컨셉', blank=True)
    age_generation = models.CharField('연령대', blank=True, max_length=50)
    personal_request = models.TextField('요청사항', blank=True)
