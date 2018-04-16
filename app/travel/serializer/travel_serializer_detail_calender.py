from rest_framework import serializers

from ..models import TravelInformation, TravelSchedule


class TravelInformationScheduleSerializer(serializers.ModelSerializer):
    # is_possible = serializers.SerializerMethodField(read_only=True)
    # people = serializers.IntegerField(read_only=True)

    class Meta:
        model = TravelSchedule
        fields = (
            # 'is_possible',
            'travel_info',
            'start_date',
            # 'people',
            'reserved_people',
        )

    # def get_is_possible(self, attrs):
    #     maxPeople = attrs.travel_info.maxPeople
    #     reserved_people = attrs.reserved_people
    #     reserve_people = self.people
    #
    #     if maxPeople < reserve_people + reserved_people:
    #         return False
    #     else:
    #         return True


class TravelInformationDetailCalenderSerializer(serializers.ModelSerializer):
    # people = TravelInformationScheduleSerializer()
    schedules = TravelInformationScheduleSerializer(many=True)

    class Meta:
        model = TravelInformation
        fields = (
            'pk',
            'name',
            'schedules',
            'maxPeople',
            # 'people',
        )
