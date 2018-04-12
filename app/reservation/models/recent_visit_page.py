from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model

from members.models import *
from .reservation_base import ReservationBase
from travel.models import TravelInformation


class RecentVisitPage(ReservationBase):
    travel_Schedule = models.ForeignKey(
        TravelInformation,
        on_delete=models.CASCADE)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
