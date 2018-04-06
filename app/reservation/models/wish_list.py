
from django.db import models

from members.models import *
from .reservation_base import ReservationBase
from travel.models import TravelInformation

class WishList(ReservationBase):
    travel_info = models.ForeignKey(
        TravelInformation,
        on_delete=models.CASCADE
    )
    member = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
