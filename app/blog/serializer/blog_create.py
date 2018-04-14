from blog.models import BlogImage, Blog
from rest_framework import serializers

from reservation.models import Reservation


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = (
            'blog_id',
            'img_field',
            'img_thumbnail',
        )


class BlogSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True)

    class Meta:
        model = Blog
        fields = (
            'pk',
            'travel_Reservation',
            'title',
            'contents',
            'score',
            'images',
        )
