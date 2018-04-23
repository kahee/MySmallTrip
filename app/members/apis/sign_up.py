from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializer import UserSerializer, AccessTokenSerializer


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer


class FacebookLogin(APIView):

    def post(self, request):
        serializer = AccessTokenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'user': UserSerializer(user).data,
        }
        return Response(data, status=status.HTTP_200_OK)
