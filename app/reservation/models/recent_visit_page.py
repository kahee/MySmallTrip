
from django.db import models
from .reservation_base import ReservationBase
from travel.models import TravelInformation


class RecentVisitPage(ReservationBase):
    travel_Schedule = models.ForeignKey(
        TravelInformation,
        on_delete=models.CASCADE)
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
