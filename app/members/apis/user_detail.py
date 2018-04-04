from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializer.user_detail_serializer import ChangePasswordSerializer, ChangeImageSerializer
from ..serializer import UserSerializer

User = get_user_model()


class UserDetailView(APIView):
    # 인증
    permission_classes = (
        permissions.IsAuthenticated,
    )

    # 유저 정보
    def get(self, request):
        # 해당 유저 정보를 리턴
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 비밀번호 변경
    def patch(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)

        # 비밀번호 유효성 검사가 패스 되면, 새로운 비밀번호로 변경
        if serializer.is_valid():
            user = User.objects.get(username=request.user)
            user.set_password(serializer.validated_data['user']['password'])
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailImageView(APIView):
    # 인증
    permission_classes = (
        permissions.IsAuthenticated,
    )

    # 프로필 이미지 변경
    def patch(self, request, *args, **kwargs):
        serializer = ChangeImageSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(username=request.user)
            user.img_profile = serializer.validated_data['img_profile']
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
