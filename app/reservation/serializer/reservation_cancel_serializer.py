from django.contrib.auth import get_user_model
from rest_framework import serializers
from reservation.models import Reservation
from reservation.serializer import TravelScheduleSerializer
from travel.models import TravelSchedule

User = get_user_model()


class ReservationCancelSerializer(serializers.ModelSerializer):
    pk = serializers.PrimaryKeyRelatedField(queryset=Reservation.objects.all())

    class Meta:
        model = Reservation
        fields = (
            'pk',
            'is_canceled',
        )

    def update(self, instance, validated_data):

        instance.is_canceled = validated_data.get('is_canceled', True)
        instance.save()

        travel_schedule = TravelSchedule.objects.filter(id=instance.travel_Schedule_id).first()
        reserve_user_sum = travel_schedule.reserved_people - instance.reserve_people

        reserve_user_update = TravelScheduleSerializer(
            travel_schedule,
            data={'reserved_people': reserve_user_sum },
            partial=True
        )
        if reserve_user_update.is_valid(raise_exception=True):
            reserve_user_update.save()
        return instance
