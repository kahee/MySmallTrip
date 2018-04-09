from django.contrib.auth import authenticate, get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializer import UserSerializer

User = get_user_model()


class LoginforAuthTokenView(APIView):

    def post(self, request):
        # username과 password 입력 받은 후, 유효성 검사
        serializers = AuthTokenSerializer(data=request.data)

        if serializers.is_valid(raise_exception=True):
            user = serializers.validated_data['user']

            token, _ = Token.objects.get_or_create(user=user)

            data = {
                'token': token.key,
                'user': UserSerializer(user).data,
            }
            return Response(data, status=status.HTTP_200_OK)

        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


