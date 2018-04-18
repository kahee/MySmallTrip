from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from reservation.models import Reservation
from reservation.serializer import ReservationSerializer, ReservationCancelSerializer
from travel.models import TravelSchedule


class ReservationView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request, **kwargs):
        context = {'request': self.request}
        reservation_informations = Reservation.objects.filter(is_canceled=False)
        serializer = ReservationSerializer(reservation_informations, context=context, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        context = {
            'request': self.request,
        }
        serializer = ReservationSerializer(data=request.data, context=context)

        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            reservation = serializer.save()
            data = {
                'reservation': ReservationSerializer(reservation).data
            }
            return Response(data, status=status.HTTP_201_CREATED)

            # if reservation:
            #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
