from django.contrib.auth import get_user_model
from rest_framework import serializers
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
        # request.data 로 받은 email데이터를 검증한 후,
        # username에도 저장
        password = validate_data['password']

        user = User.objects.create_user(
            email=validate_data['email'],
            username=validate_data['email'],
            first_name=validate_data['first_name'],
            phone_number=validate_data['phone_number'],
            img_profile=validate_data['img_profile'],
        )

        user.set_password(password)
        return user

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'email',
            'first_name',
            'phone_number',
            'img_profile',
            'password'
        )
