from rest_framework import serializers

from ..models import TravelInformation, TravelSchedule


class TravelInformationScheduleSerializer(serializers.ModelSerializer):
    # is_possible = serializers.SerializerMethodField(source='get_is_possible')

    class Meta:
        model = TravelSchedule
        fields = (
            # 'is_possible',
            'travel_info',
            'start_date',
            'reserved_people',
        )

    # def get_is_possible(self, attrs):
    #     maxPeople = attrs.travel_info.maxPeople
    #     reserved_people = attrs.reserved_people
    #     reserve_people = 4
    #
    #     if maxPeople < reserve_people + reserved_people:
    #         return False
    #     else:
    #         return True


class TravelInformationDetailCalenderSerializer(serializers.ModelSerializer):
    schedules = TravelInformationScheduleSerializer(many=True)

    class Meta:
        model = TravelInformation
        fields = (
            'pk',
            'name',
            'schedules',
            'maxPeople',
        )
