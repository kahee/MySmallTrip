from rest_framework import serializers

from blog.models import Blog
from blog.serializer import BlogImageSerializer


class BlogUpdateSerializer(serializers.ModelSerializer):
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

    def update(self, instance, validated_data):
        if instance is not None:
            instance.pk = validated_data.get('pk', instance.pk)
            instance.travel_reservation = validated_data.get('travel_reservation', instance.travel_reservation)
            instance.title = validated_data.get('title', instance.title)
            instance.contents = validated_data.get('contents', instance.contents)
            instance.score = validated_data.get('score', instance.score)
            # instance.images = validated_data.get('images',instance.images)
        instance.save()
        return instance
