from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from requests import Response
from rest_framework import serializers, status
from rest_framework.exceptions import ValidationError

User = get_user_model()


class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    password2 = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
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

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class ChangeImageSerializer(serializers.ModelSerializer):
    img_profile = serializers.ImageField(allow_empty_file=True)

    class Meta:
        model = User
        fields = (
            'img_profile',
        )

    def update(self, instance, validated_data):

        if 'img_profile' in validated_data:
            instance.img_profile.delete()
            instance.img_profile = validated_data['img_profile']
            instance.save()
            return instance

        else:
            instance.img_profile.delete()
            instance.save()
            return instance


class ChangePhoneNumberSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True, max_length=11, min_length=11)

    class Meta:
        model = User
        fields = (
            'phone_number',
        )


class CheckCertificationNumberSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=True, max_length=11)
    certification_number = serializers.CharField(required=True, max_length=5, min_length=5, )

    class Meta:
        model = User
        fields = (
            'phone_number',
            'certification_number',
        )
