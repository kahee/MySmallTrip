from rest_framework import serializers

from members.serializer import UserSerializer
from ..models import TravelInformation, TravelSchedule


class TravelInformationScheduleSerializer(serializers.ModelSerializer):
    is_possible = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TravelSchedule
        fields = (
            # 'travel_info',
            'start_date',
            'is_possible',
            'reserved_people',
        )

    def get_is_possible(self, attrs):
        maxPeople = attrs.travel_info.maxPeople
        reserved_people = attrs.reserved_people
        reserve_people = self.context['people']

        if attrs.is_possible_reservation:
            if maxPeople < reserve_people + reserved_people:
                return False
            else :
                return True
        else :
            return False

        # if maxPeople < reserve_people + reserved_people:
        #     return False
        # else:
        #     return True


class TravelInfoSerializer(serializers.ModelSerializer):
    people = serializers.SerializerMethodField()
    schedules = TravelInformationScheduleSerializer(context={'people': people}, many=True)
    member = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = TravelInformation
        fields = (
            'pk',
            'name',
            'maxPeople',
            'people',
            'schedules',
            'member',
        )

    def get_people(self, attrs):
        if "people" in self.context:
            return self.context['people']
        return None
