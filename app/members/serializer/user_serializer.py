from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

User = get_user_model()


class UserSerializerWishList(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'pk',
            'username',
            'email',
            'first_name',
            'is_facebook_user',
            'wish_products',
        )


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=False,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_number = serializers.CharField(
        required=True,
    )
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    img_profile = serializers.ImageField(required=False, allow_empty_file=True)
    first_name = serializers.CharField(required=True)

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
            'is_facebook_user',
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
        )

        if 'img_profile' in validate_data:
            user.img_profile = validate_data['img_profile']

        # 비밀번호 설정 후 저장
        user.set_password(password)
        user.save()
        return user


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
