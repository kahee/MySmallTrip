from rest_framework import serializers

from travel.models import TravelInformation, CityInformation, TravelInformationImage


class TravelInformationImageSerializer(serializers.ModelSerializer):
    product_thumbnail = serializers.ImageField(read_only=True)
    product_thumbnail_2x = serializers.ImageField(read_only=True)
    product_thumbnail_3x = serializers.ImageField(read_only=True)

    class Meta:
        model = TravelInformationImage
        fields = (
            'image_id',
            'product_image',
            'product_thumbnail',
            'product_thumbnail_2x',
            'product_thumbnail_3x',
        )


class CityInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityInformation
        field = 'all'
        exclude = ('id', 'creation_datetime', 'modify_datetime', 'is_usable')


class TravelInformationSerializer(serializers.ModelSerializer):
    images = TravelInformationImageSerializer(many=True)
    city = CityInformationSerializer()

    class Meta:
        model = TravelInformation
        fields = (
            'pk',
            'name',
            'city',
            'time',
            'images',
        )
