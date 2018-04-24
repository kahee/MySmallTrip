from rest_framework import status, permissions
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.serializer import ReservationDoesNotExists
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
        pk = request.data.get('pk', None)
        if pk is not None:
            try:
                reservation = Reservation.objects.filter(member=request.user).get(pk=request.data['pk'])
                serializer = ReservationCancelSerializer(reservation, data=request.data, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

            # 예약 번호가 해당 유저의 예약 리스트에 없는 경우
            except Reservation.DoesNotExist:
                raise ReservationDoesNotExists

        else:
            data = {
                'pk': '예약 pk를 입력해주세요'
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
