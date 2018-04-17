from rest_framework import serializers

from travel.models import TravelInformation, CityInformation, TravelInformationImage


# class TravelInformationImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TravelInformationImage
#         fields = (
#             'image_id',
#             'product_image',
#             'product_image_thumbnail',
#         )


class CityInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityInformation
        field = 'all'
        exclude = ('id', 'creation_datetime', 'modify_datetime', 'is_usable')


class TravelInformationSerializer(serializers.ModelSerializer):
    # images = TravelInformationImageSerializer(many=True)
    city = CityInformationSerializer()

    class Meta:
        model = TravelInformation
        fields = (
            'pk',
            'name',
            'city',
            'price',
            'time',
            'main_image_thumbnail',
        )


class TravelInformationWishListSerializer(serializers.ModelSerializer):
    city = CityInformationSerializer()

    class Meta:
        model = TravelInformation
        fields = (
            'pk',
            'name',
            'city',
            'price',
            'time',
        )
