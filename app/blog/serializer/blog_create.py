from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueValidator

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


class BlogCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True)
    )
    travel_reservation = serializers.PrimaryKeyRelatedField(
        queryset=Reservation.objects.all(),
        read_only=False,
        validators=[UniqueValidator(queryset=Blog.objects.all())]
    )

    class Meta:
        model = Blog
        fields = (
            'travel_reservation',
            'title',
            'contents',
            'score',
            'images',
        )

    def create(self, validate_data, **kwargs):
        blog = Blog.objects.create(
            travel_reservation=validate_data['travel_reservation'],
            title=validate_data['title'],
            contents=validate_data['contents'],
            score=validate_data['score'],
        )

        for item in self.validated_data['images']:
            blog.images.create(
                blog_id=blog,
                img_field=item
            )
            blog.save()
        return blog


class BlogListSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True)

    class Meta:
        model = Blog
        fields = (
            'pk',
            'travel_reservation',
            'title',
            'contents',
            'score',
            'images',
        )
