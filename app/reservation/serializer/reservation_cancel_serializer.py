from django.contrib.auth import get_user_model
from rest_framework import serializers
from reservation.models import Reservation
from reservation.serializer import TravelScheduleSerializer, UserSerializer
from travel.models import TravelSchedule

User = get_user_model()


class ReservationCancelSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(queryset=Reservation.objects.all())
    member = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Reservation
        fields = (
            'pk',
            'member',
            'is_canceled',
        )

    def update(self, instance, validated_data):

        if instance.is_canceled :
            raise serializers.ValidationError('이미 취소된 예약입니다. WPS.유가희님관에게 문의해주세요.')

        instance.is_canceled = validated_data.get('is_canceled', True)
        instance.save()

        travel_schedule = TravelSchedule.objects.filter(id=instance.travel_Schedule_id).first()

        reserve_user_sum = travel_schedule.reserved_people - instance.reserve_people
        if reserve_user_sum < 0:
            reserve_user_sum = 0
        max_people = travel_schedule.travel_info.maxPeople

        reserve_user_update = TravelScheduleSerializer(
            travel_schedule,
            data={'reserved_people': reserve_user_sum },
            partial=True
        )
        if reserve_user_update.is_valid(raise_exception=True):
            reserve_user_update.save()

        if travel_schedule.reserved_people < max_people:
            reserve_user_update2 = TravelScheduleSerializer(
                travel_schedule,
                data={'is_possible_reservation': True},
                partial=True
            )
            if reserve_user_update2.is_valid(raise_exception=True):
                reserve_user_update2.save()

        return instance
