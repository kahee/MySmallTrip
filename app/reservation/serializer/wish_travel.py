from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from members.serializer import UserSerializerWishList
from reservation.models import WishTravel
from travel.models import TravelInformation

User = get_user_model()


class WishTravelSerializer(serializers.ModelSerializer):
    # CurrentUserDefault의 경우 context로 request를 넣어서 보내줘야 한다.
    user = UserSerializerWishList(read_only=True, default=serializers.CurrentUserDefault())
    travel_info = serializers.PrimaryKeyRelatedField(
        queryset=TravelInformation.objects.all(),
        read_only=False,
        required=True,
    )

    class Meta:
        model = WishTravel
        fields = (
            'id',
            'user',
            'travel_info',

        )
        validators = [
            UniqueTogetherValidator(
                queryset=WishTravel.objects.all(),
                fields=('user', 'travel_info')
            )
        ]
