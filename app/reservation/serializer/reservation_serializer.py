from rest_framework import serializers

from members.serializer import UserSerializer, get_user_model
from reservation.models import Reservation
from travel.models import TravelSchedule, TravelInformation

from travel.serializer import TravelInformationSerializer, TravelInformationMinSerializer

User = get_user_model()


#  관리자가 필요한 기능
class TravelScheduleListSerializer(serializers.ModelSerializer):
    travel_info = TravelInformationSerializer()

    class Meta:
        model = TravelSchedule
        fields = (
            'travel_info',
            'reserved_people',
            'start_date',
            'end_date',
        )


class ReservationCreateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(required=True)
    travel_info = serializers.PrimaryKeyRelatedField(required=True, queryset=TravelInformation.objects.all())
    member = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    people = serializers.IntegerField(required=True)

    class Meta:
        model = Reservation
        fields = (
            'travel_info',
            'start_date',
            'member',
            'is_canceled',
            'total_price',
            'people',
            'concept',
            'age_generation',
            'personal_request',

        )

    def create(self, validate_data):
        """
        :param validate_data:
        :return: reservation
        """
        reservation = Reservation.objects.create_with_schedule(
            travel_info=validate_data["travel_info"],
            start_date=validate_data["start_date"],
            people=validate_data['people'],
            member=validate_data['member'],
        )
        return reservation


# 예약 현황 보여주는 리스트
class ReservationListSerializer(serializers.ModelSerializer):
    travel_schedule = TravelScheduleListSerializer()
    member = UserSerializer()

    class Meta:
        model = Reservation
        fields = (
            'pk',
            'travel_schedule',
            'member',
            'is_canceled',
            'total_price',
            'people',
            'concept',
            'age_generation',
            'personal_request',
        )
