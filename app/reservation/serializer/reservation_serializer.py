from rest_framework import serializers, status
from members.serializer import UserSerializer, get_user_model
from reservation.models import Reservation, TravelInformation
from travel.models import TravelSchedule

from travel.serializer import TravelInformationSerializer

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


class ReservationSerializer(serializers.ModelSerializer):
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

    def create(self, validate_data, **kwargs):
        # 1.받은 travel_id 와 user를 검증하고나서 reservation에 저장
        # 3.1.예약할 인원 + 예약한 인원=maxPeople이면
        #   travelschedule.is_possible_reservation update
        # 3.2.예약할 인원 + 예약한 인원>maxPeople이면
        #   예약 안된다고 에러메세지
        # 2. reservation을 생성하면서 TravelSchedule.reserved_user와 reservation.reserve_user를 합쳐서 업데이트

        reservation = Reservation.objects.create(**validate_data)
        travel_schedule = TravelSchedule.objects.filter(id=reservation.travel_Schedule_id).first()
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
            raise serializers.ValidationError('해당상품은 최대인원을 초과했습니다. 관리자에게 문의해주세요.')

        if travel_schedule.reserved_people == max_people:
            reserve_user_update2 = TravelScheduleSerializer(
                travel_schedule,
                data={'is_possible_reservation': False},
                partial=True
            )
            if reserve_user_update2.is_valid(raise_exception=True):
                reserve_user_update2.save()

        return reservation
