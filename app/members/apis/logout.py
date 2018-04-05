from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

User = get_user_model()


class LogoutView(APIView):
    queryset = User.objects.all()

    def get(self, request):
        request.user.auth_token.delete()

        data = {
            "detail": "로그아웃이 되었습니다."
        }

        return Response(data,status=status.HTTP_200_OK)
