from django.conf import settings

from members.models import *
from . import ReservationBase
from ..models import TravelInformation

__all__ = (
    'WishTravel',
)


class WishTravel(ReservationBase):
    travel_info = models.ForeignKey(
        TravelInformation,
        on_delete=models.CASCADE,
        related_name='wish_user_info_list',
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wish_products_info_list',
    )

    class Meta:
        app_label = 'reservation'
        unique_together = (
            ('travel_info', 'user'),
        )
