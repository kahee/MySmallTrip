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
    start_date = serializers.DateField()
    travel_info = serializers.PrimaryKeyRelatedField(queryset=TravelInformation.objects.all())
    member = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Reservation
        fields = (
            # 'travel_Schedule',
            'travel_info',
            'start_date',
            'member',
            'is_canceled',
            'total_price',
            'reserve_people',
            'concept',
            'age_generation',
            'personal_request',

        )

    def create(self, validate_data):
        """
        1.travel_info.pk와 start_date, 예약할 사람을 입력받아서
        2.해당 날짜에 대해 schedule이 없으면 만들고,있으면 reservation을 생성
        3.예약가능 점검
            3.1 현재 예약되어있는 인원 + 예약 할 인원 > 상품의 최대인원수
            -> error
            3.2 아니면
            -> 현재 예약되어 있는 인원 update
        4. 현재 예약된 인원 = 상품의 최대인원수
            -> is_possible_reservation = False로 업데이트
        :param validate_data:
        :return: reservation
        """
        # 1.받은 travel_id 와 user를 검증하고나서 reservation에 저장
        # 3.1.예약할 인원 + 예약한 인원=maxPeople이면
        #   travelschedule.is_possible_reservation update
        # 3.2.예약할 인원 + 예약한 인원>maxPeople이면
        #   예약 안된다고 에러메세지
        # 2. reservation을 생성하면서 TravelSchedule.reserved_user와 reservation.reserve_user를 합쳐서 업데이트
        # reservation = Reservation.objects.get_or_create
        ## 스케쥴을 만들고, reservation만들고
        travel_schedule_list = TravelSchedule.objects.filter(travel_info=validate_data["travel_info"]).filter(
            start_date=validate_data["start_date"]).first()

        if travel_schedule_list is None:
            travel_schedule, _ = TravelSchedule.objects.get_or_create(
                travel_info=validate_data["travel_info"],
                start_date=validate_data["start_date"],
                reserved_people=0,
                is_possible_reservation=True,
            )

        else:
            travel_schedule = travel_schedule_list

        price = travel_schedule.travel_info.price

        reservation, _ = Reservation.objects.get_or_create(
            travel_Schedule=travel_schedule,
            member=validate_data["member"],
            is_canceled=False,
            reserve_people=validate_data['reserve_people'],
            total_price=price * validate_data['reserve_people'],
        )
        max_people = travel_schedule.travel_info.maxPeople

        reserve_user_sum = reservation.reserve_people + travel_schedule.reserved_people

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

        if travel_schedule.reserved_people == max_people:
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
    travel_Schedule = TravelScheduleMinSerializer()
    member = UserSerializer()

    class Meta:
        model = Reservation
        fields = (
            'pk',
            'travel_Schedule',
            'member',
            'is_canceled',
            'total_price',
            'reserve_people',
            'concept',
            'age_generation',
            'personal_request',
        )
