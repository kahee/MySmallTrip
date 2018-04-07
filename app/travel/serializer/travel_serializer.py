from rest_framework import serializers
from rest_framework.views import APIView

from travel.models import TravelInformation


class TravelInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelInformation
        fields = (
            'pk',
            'travel_id',
            'name',
            'category',
            'theme',
            'product_type',
            'language',
            'city',
            'time',
            'company',
            'description',
            'meeting_time',
            'meeting_place',
        )