import random

from django.contrib.auth import get_user_model
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializer.user_detail_serializer import ChangePasswordSerializer, ChangeImageSerializer, \
    CheckCertificationNumberSerializer, ChangePhoneNumberSerializer
from members.sms_send import send_message
from ..serializer import UserSerializer, ValidationError

User = get_user_model()


class UserDetailView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    # 유저 정보
    def get(self, request):
        # 해당 유저 정보를 리턴
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserChangePasswordView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    # 비밀번호 변경
    def patch(self, request, *args, **kwargs):
        user = User.objects.get(username=request.user)
        serializer = ChangePasswordSerializer(user, data=request.data, partial=True)

        # 비밀번호 유효성 검사가 패스 되면, 새로운 비밀번호로 변경
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangeImageView(APIView):
    # 인증
    permission_classes = (
        permissions.IsAuthenticated,
    )

    # 프로필 이미지 변경
    def patch(self, request):
        user = User.objects.get(username=request.user)
        serializer = ChangeImageSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserChangePhoneNumberView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    # 바뀐 핸드폰 번호로 인증번호 발송
    def post(self, request):

        # 특정길이의 랜덤 숫자 생성
        def rand_str(n):
            number = ''.join(["%s" % random.randint(0, 9) for num in range(0, n)])
            return number

        serializer = ChangePhoneNumberSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(username=request.user)

            # 인증하려는 번호가 이미 사용하고 있는 번호이면 400리턴
            if serializer.validated_data['phone_number'] == user.phone_number:
                data = {
                    'detail': f' {user.username}님이 이미 사용하고 있는 휴대폰 번호 입니다.'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            # 특정길이 랜덤숫자를 user객체의 인증번호로 저장 및 문자로 발송
            certification_number = rand_str(5)
            user.certification_number = certification_number
            user.save()
            send_message(serializer.validated_data['phone_number'], f'My Small Trip 인증번호 : {certification_number}')
            data = {

                'detail': '인증번호가 발송되었습니다.',
            }

            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 인증번호 검증을 통해 핸드폰 번호 변경
    def patch(self, request, *args, **kwargs):
        serializer = CheckCertificationNumberSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(username=request.user)

            if not user.certification_number == serializer.validated_data['certification_number']:
                data = {
                    'detail': '인증번호가 일치하지 않습니다.'
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

            user.phone_number = serializer.validated_data['phone_number']
            user.certification_number = None
            user.save()

            data = {
                'user': UserSerializer(user).data
            }
            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
