
from rest_framework import serializers, status
from members.serializer import UserSerializer, get_user_model
from reservation.models import Reservation
from travel.models import TravelSchedule

from travel.serializer import TravelInformationSerializer

User = get_user_model()


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
        # 체크1 (user가 같은 상품을 같은 명수 예약할 때, 같은 예약으로 처리할 지? 다른예약으로 처리할 지?)
        # validators = UniqueTogetherValidator(
        #     queryset=Reservation.objects.all(),
        #     fields=['travel_Schedule', 'member','reserve_people']
        # )

    def update(self, instance, validated_data):
        instance.is_canceled = validated_data.get('is_canceled', instance.email)
        instance.reserve_people = validated_data.get('reserve_people', instance.reserve_people)
        instance.concept = validated_data.get('concept', instance.concept)
        instance.age_generation = validated_data.get('age_generation', instance.age_generation)
        instance.personal_request = validated_data.get('personal_request', instance.personal_request)
        instance.save()
        return instance

    def create(self, validate_data, **kwargs):
        # 1.받은 travel_id 와 user를 검증하고나서 reservation에 저장
        # 2. schedule에 reserved_people update
        reservation = Reservation.objects.create(**validate_data)

        # 체크2 reservation을 생성하면서 TravelSchedule.reserved_user와 reservation.reserve_user를 합쳐서 업데이트
        travel_schedule = TravelSchedule.objects.filter(id=reservation.travel_Schedule_id).first()
        reserve_user_sum = reservation.reserve_people + travel_schedule.reserved_people

        reserve_user_update = TravelScheduleSerializer(
            travel_schedule,
            data={'reserved_people': reserve_user_sum},
            partial=True
        )
        if reserve_user_update.is_valid(raise_exception=True):
            reserve_user_update.save()
        return reservation

