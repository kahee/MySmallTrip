from rest_framework import serializers, status
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
            'is_possible_reservation',
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
            'is_possible_reservation',
            'travelschedule_user',
        )


class ReservationCreateSerializer(serializers.ModelSerializer):
    start_date = serializers.DateField(required=True)
    travel_info = serializers.PrimaryKeyRelatedField(required=True,queryset=TravelInformation.objects.all())
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
            -> is_possible_reservation = False로 업데이트

        :param validate_data:
        :return: reservation
        """
        travel_schedule, _ = TravelSchedule.objects.get_or_create(
            travel_info=validate_data["travel_info"],
            start_date=validate_data["start_date"],
        )

        max_people = travel_schedule.travel_info.maxPeople

        reserve_user_sum = validate_data['people'] + travel_schedule.reserved_people

        if reserve_user_sum <= max_people:
            reserve_user_update = TravelScheduleSerializer(
                travel_schedule,
                data={'reserved_people': reserve_user_sum},
                partial=True
            )
            if reserve_user_update.is_valid(raise_exception=True):
                reserve_user_update.save()
        else:
            raise serializers.ValidationError('해당상품은 최대인원을 초과했습니다. WPS.유가희님에게 문의해주세요.')

        # 매니저에 새 메서드를 추가 create_with_schedule() (TravelSchedule을 받아서 새 Reservation을 생성해주는)
        reservation, _ = Reservation.objects.get_or_create(
            travel_schedule=travel_schedule,
            member=validate_data["member"],
            is_canceled=False,
            people=validate_data['people'],
        )

        if travel_schedule.reserved_people == max_people:
            # SerializerMethodField
            reserve_user_update2 = TravelScheduleSerializer(
                travel_schedule,
                data={'is_possible_reservation': False},
                partial=True
            )
            if reserve_user_update2.is_valid(raise_exception=True):
                reserve_user_update2.save()

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
