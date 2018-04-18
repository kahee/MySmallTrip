from rest_framework import generics, permissions

from reservation.models import Reservation
from reservation.serializer import ReservationListSerializer


class ReservationListView(generics.ListAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    serializer_class = ReservationListSerializer

    queryset = Reservation.objects.all()

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(member=user)
