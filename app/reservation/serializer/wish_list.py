from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueTogetherValidator

from members.serializer import UserSerializer
from reservation.models import WishList
from travel.models import TravelInformation

User = get_user_model()


class WishListCreateSerializer(serializers.ModelSerializer):
    # CurrentUserDefault의 경우 context로 request를 넣어서 보내줘야 한다.
    user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    travel_info = serializers.PrimaryKeyRelatedField(
        queryset=TravelInformation.objects.all(),
        read_only=False,
    )

    class Meta:
        model = WishList
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=WishList.objects.all(),
                fields=('user', 'travel_info')
            )
        ]


#  해당 상품이 위시리스트에 있는지 체크
class TravelInfoDoesNotExists(APIException):
    status_code = 400
    default_detail = '해당 상품이 위시리스트에 없습니다.'
    default_code = 'travel_info_DoesNotExists'


class WishListDeleteSerializer(serializers.ModelSerializer):
    # travel_info 가 WishList 테이블에 있는지 유효성 검사.
    user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    travel_info = serializers.PrimaryKeyRelatedField(
        queryset=TravelInformation.objects.all(),
        read_only=False,
    )

    class Meta:
        model = WishList
        fields = '__all__'

    def validate(self, attrs):
        # 해당 상품이 위시리스트에 있는지 체크
        try:
            WishList.objects.get(travel_info=attrs['travel_info'], user=attrs['user'])

        # 없으면 해당 상품이 없다는 오류 발생
        except WishList.DoesNotExist:
            raise TravelInfoDoesNotExists

        return attrs
