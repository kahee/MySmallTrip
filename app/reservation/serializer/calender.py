from django.contrib.auth import get_user_model
from rest_framework import serializers

from reservation.models import Reservation
from travel.models import TravelSchedule

User = get_user_model()


class CalenderSerializer(serializers.ModelSerializer):
    travel_Schedule = serializers.PrimaryKeyRelatedField(read_only=False, queryset=TravelSchedule.objects.all())
    member = serializers.PrimaryKeyRelatedField(read_only=False, queryset=User.objects.all())

    class Meta:
        model = Reservation
        fields = (
            'travel_Schedule',
            'member',
            'is_canceled',
            'reserve_people',
            'concept',
            'age_generation',
            'personal_request',
        )
    #
