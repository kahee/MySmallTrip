from rest_framework import serializers
from travel.models import CityInformation


class CityInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityInformation
        fields = (
            'name',
            'nationality',
            'city_image',
            'city_image_thumbnail',
        )
