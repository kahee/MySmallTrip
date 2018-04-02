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

        user = User.objects.create_user(
            email=validate_data['email'],
            password=validate_data['password'],
            username=validate_data['email'],
            first_name=validate_data['first_name'],
        )
        return user

    class Meta:
        model = User
        fields = '__all__'
