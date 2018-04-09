from rest_framework import serializers
from rest_framework.views import APIView

from travel.models import TravelInformation, CityInformation, TravelInformationImage, CompanyInformation


class TravelInformationImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelInformationImage
        fields = (
            'image_id',
            'product_image',
        )


class CityInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityInformation
        field = 'all'
        exclude = ('continent', 'id', 'creation_datetime', 'modify_datetime', 'is_usable')


class CompanyInformationSerailizer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInformation
        # field = (
        #     'company'
        # )
        field = 'all'
        exclude = ('info', 'id', 'creation_datetime', 'modify_datetime', 'is_usable')


class TravelInformationSerializer(serializers.ModelSerializer):
    images = TravelInformationImageSerializer(many=True)
    city = CityInformationSerializer()
    company = CompanyInformationSerailizer()

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
            # 'price',
            'company',
            'description',
            'meeting_time',
            'meeting_place',
            'images',
        )
