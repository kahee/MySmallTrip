from rest_framework import serializers
from rest_framework.views import APIView

from travel.models import TravelInformation, CityInformation, TravelInformationImage, CompanyInformation


class TravelInformationImageSerializer(serializers.ModelSerializer):
    product_thumbnail = serializers.ImageField(read_only=True)
    print(product_thumbnail)
    # product_thumbnail_2x = serializers.ImageField(read_only=True)
    # product_thumbnail_3x = serializers.ImageField(read_only=True)

    class Meta:
        model = TravelInformationImage
        fields = (
            'image_id',
            'product_image',
            'product_thumbnail',
            # 'product_thumbnail_2x',
            # 'product_thumbnail_3x',
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
