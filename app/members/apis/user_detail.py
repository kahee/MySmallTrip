from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializer.change_pasword_serializer import ChangePasswordSerializer
from ..serializer import UserSerializer

User = get_user_model()


class UserDetailView(APIView):
    # 인증 허가
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        # 해당 유저 정보를 리턴
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):

        user = User.objects.get(username=request.user)
        serializer = ChangePasswordSerializer(data=request.data)

        # 비밀번호 유효성 검사가 패스 되면, 새로운 비밀번호로 변경
        if serializer.is_valid():
            user.set_password(serializer.validated_data['user']['password'])
            print(user.mycoupon)
            user.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailImageView(APIView):

    def patch(self, request, *args, **kwargs):
        pass
