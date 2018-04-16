from rest_framework import serializers

from ..models import TravelInformation, TravelSchedule


class TravelInformationScheduleSerializer(serializers.ModelSerializer):
    is_possible = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TravelSchedule
        fields = (
            'travel_info',
            'is_possible',
            'start_date',
            'reserved_people',
        )

    def get_is_possible(self, attrs):
        maxPeople = attrs.travel_info.maxPeople
        reserved_people = attrs.reserved_people
        reserve_people = self.context['people']

        if maxPeople <= reserve_people + reserved_people:
            return False
        else:
            return True


class TravelInformationSerializer(serializers.ModelSerializer):
    people = serializers.SerializerMethodField()
    schedules = TravelInformationScheduleSerializer(context={'people': people}, many=True)

    class Meta:
        model = TravelInformation
        fields = (
            'pk',
            'name',
            'maxPeople',
            'schedules',
            'people',
        )

    def get_people(self, attrs):
        if "people" in self.context:
            return self.context['people']
        return None
