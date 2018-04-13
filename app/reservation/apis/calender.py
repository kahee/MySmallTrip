from rest_framework.response import Response
from rest_framework.views import APIView

from reservation.models import Reservation
from reservation.serializer import ReservationSerializer, status, CalenderSerializer


class CalenderView(APIView):
    def get(self):
        reservation_informations= Reservation.objects.all()
        serializer = CalenderSerializer(reservation_informations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
