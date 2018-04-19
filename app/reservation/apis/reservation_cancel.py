from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from reservation.models import Reservation
from reservation.serializer import ReservationCancelSerializer


class ReservationCancelView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self):
        reservation_informations = Reservation.objects.filter(is_canceled=True)
        serializer = ReservationCancelSerializer(reservation_informations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        # user filter 거르기
        #

        reservation = Reservation.objects.filter(member=request.user).get(pk=request.data['pk'])

        if reservation:
            serializer = ReservationCancelSerializer(reservation, data=request.data,  partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)
