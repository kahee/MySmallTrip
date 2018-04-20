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
        max_people = attrs.travel_info.max_people
        reserved_people = attrs.reserved_people
        reserve_people = self.context['people']

        if max_people < reserve_people + reserved_people:
            return False
        else:
            return True


class TravelInfoSerializer(serializers.ModelSerializer):
    people = serializers.SerializerMethodField()
    travel_info = TravelInformationScheduleSerializer(context={'people': people}, many=True)
    member = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = TravelInformation
        fields = (
            'pk',
            'name',
            'max_people',
            'people',
            'travel_info',
            'member',
        )

    def get_people(self, attrs):
        if "people" in self.context:
            return self.context['people']
        return None
