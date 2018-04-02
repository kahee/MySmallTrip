from django.contrib.auth import get_user_model
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
        fields = '__all__'
