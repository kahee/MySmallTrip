from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from reservation.models import Reservation
from reservation.serializer import ReservationSerializer


class ReservationView(APIView):
    def get(self, request, **kwargs):
        reservation_informations = Reservation.objects.all()
        serializer = ReservationSerializer(reservation_informations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ReservationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            reservation = serializer.save()
            if reservation:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
