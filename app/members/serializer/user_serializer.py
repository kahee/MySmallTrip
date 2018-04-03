from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers, status, exceptions
from rest_framework.exceptions import APIException, ValidationError
from rest_framework.validators import UniqueValidator

User = get_user_model()


class PasswordMismatchError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '비밀번호가 일치하지 않습니다!'
    default_code = 'password_mismatch'


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'email',
            'first_name',
            'phone_number',
            'img_profile',
            'password',
            'password2',
        )

    def validate_password(self, password):
        # 두개의 비밀번호가 일치하는지 검사
        # 일치하면 비밀번호 유효성 검사 실시

        password2 = self.initial_data.get('password2')

        if not password == password2:
            raise serializers.ValidationError('비밀번호가 일치하지 않습니다.')

        errors = dict()

        try:
            validate_password(password=password)

        except ValidationError as e:
            errors['password'] = list(e.messages)
            print(errors)

        if errors:
            raise serializers.ValidationError(errors)

        return password

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
