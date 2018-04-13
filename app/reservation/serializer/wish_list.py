from django.contrib.auth import get_user_model
from rest_framework import serializers
from members.serializer import UserSerializer
from reservation.models import WishList
from travel.models import TravelInformation

User = get_user_model()


class WishListSerializer(serializers.ModelSerializer):
    # CurrentUserDefault의 경우 context로 request를 넣어서 보내줘야 한다.
    user = UserSerializer(read_only=True, default=serializers.CurrentUserDefault())
    travel_info = serializers.PrimaryKeyRelatedField(
        queryset=TravelInformation.objects.all(),
        read_only=False,
        # validators=[UniqueValidator(
        #     queryset=WishList.objects.all()]
    )

    class Meta:
        model = WishList
        fields = '__all__'