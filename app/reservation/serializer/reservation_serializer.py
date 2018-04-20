from rest_framework import serializers

from members.serializer import UserSerializer, get_user_model
from reservation.models import Reservation
from travel.models import TravelSchedule, TravelInformation

from travel.serializer import TravelInformationSerializer, TravelInformationMinSerializer

User = get_user_model()


#  관리자가 필요한 기능
class TravelScheduleSerializer(serializers.ModelSerializer):
    travel_info = TravelInformationSerializer()

    class Meta:
        model = TravelSchedule
        fields = (
            'travel_info',
            'reserved_people',
            'start_date',
            'end_date',
        )


class TravelScheduleMinSerializer(serializers.ModelSerializer):
    travel_info = TravelInformationMinSerializer()

    class Meta:
        model = TravelSchedule
        exclude = (
            'id',
            'is_usable',
            'creation_datetime',
            'modify_datetime',
            'reserved_people',
            'travelschedule_user',
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
        1.travel_info.pk와 start_date, 예약할 사람을 입력받아서
        2.해당 날짜에 대해 schedule이 없으면 만들고,있으면  travel_info.pk와 start_date에 대한 객체를 불러온다.
        --> 이부분은 Manager에 새로운 메서드를 추가(create_with_schedule())
            TravelSchedule을 받아서 새 Reservation을 생성해주는 역할
        3.예약가능 점검
            3.1 현재 예약되어있는 인원 + 예약 할 인원 > 상품의 최대인원수
            -> error
        4. reservation 생성
        5. 현재 예약되어 있는 인원 update

        6. (삭제하고, is_possible_reservation필드 삭제, serializerMethod필드(is_possible로 통합,변경) :
            현재 예약된 인원 = 상품의 최대인원수
            -> is_possible_reservation = False로 업데이트(필드 삭제)

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
    travel_schedule = TravelScheduleMinSerializer()
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
