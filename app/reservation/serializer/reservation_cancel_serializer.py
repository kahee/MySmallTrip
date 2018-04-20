from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import APIException

from reservation.models import Reservation
from reservation.serializer import TravelScheduleSerializer, UserSerializer
from travel.models import TravelSchedule

User = get_user_model()


class AlreadyCancelReservation(APIException):
    status_code = 400
    default_detail = '이미 취소된 예약입니다. WPS 홍석재님에게 문의해주세요.'
    default_code = 'reservation_already_cancel'


class ReservationCancelSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(queryset=Reservation.objects.all(), required=True)
    member = UserSerializer()

    class Meta:
        model = Reservation
        fields = (
            'pk',
            'member',
            'is_canceled',
        )

    def update(self, instance, validated_data):
        if instance.is_canceled:
            raise AlreadyCancelReservation
        reservation = Reservation.objects.update_with_cancel_request(pk=validated_data['pk'])
        return reservation
