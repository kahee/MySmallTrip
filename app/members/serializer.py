# import requests
from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    def create(self, validate_data):
        password = validate_data['password']

        user = User.objects.create_user(
            email=validate_data['email'],
            username=validate_data['email'],
            first_name=validate_data['first_name'],
        )
        user.set_password(password)
        return user

    class Meta:
        model = User
        # fields = '__all__'
        fields = (
            'pk',
            'username',
            'img_profile',
            'first_name',
            'email',
        )


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()

    def validate(self, attrs):
        access_token = attrs.get('access_token')
        if access_token:
            user = authenticate(access_token=access_token)
            # authenticate가 backend에 2개가 있는데 넘겨주는 키워드를 가지고 구분해서 호출하게 된다.
            if not user:
                raise serializers.ValidationError('액세스 토큰이 잘못됬습니다.')
        else:
            raise serializers.ValidationError('액세스 토큰이 필요해요')

        attrs['user'] = user
        return attrs
