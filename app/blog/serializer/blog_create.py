from rest_framework.exceptions import APIException
from rest_framework.validators import UniqueValidator

from blog.models import BlogImage, Blog
from rest_framework import serializers

from members.serializer import UserSerializer, UserSerializerWishList
from reservation.models import Reservation


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = (
            'blog_id',
            'img_field',
            'img_thumbnail',
        )


#  해당 예약이 회원 예약리스트에 없는 경우
class ReservationDoesNotExists(APIException):
    status_code = 400
    default_detail = '해당 예약 번호가 올바르지 않습니다.'
    default_code = 'reservation_DoesNotExists'


class BlogCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=True)
    )

    travel_reservation = serializers.PrimaryKeyRelatedField(
        queryset=Reservation.objects.all(),
        read_only=False,
        validators=[UniqueValidator(queryset=Blog.objects.all())]
    )
    title = serializers.CharField(required=True)
    contents = serializers.CharField(required=True)
    score = serializers.CharField(required=True)

    class Meta:
        model = Blog
        fields = (
            'travel_reservation',
            'title',
            'contents',
            'score',
            'images',
        )

    def validate_travel_reservation(self, travel_reservation):
        user_reservation = Reservation.objects.filter(member=self.context['request'].user)
        if travel_reservation in user_reservation:
            return travel_reservation
        else:
            raise ReservationDoesNotExists

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
