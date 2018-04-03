from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializer import UserSerializer


class LoginfromAuthTokenView(APIView):

    def post(self, request):

        serializers = AuthTokenSerializer(data=request.data)

        if serializers.is_valid():
            user = serializers.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)

            data = {
                'token': token.key,
                'user': UserSerializer(user).data,
            }

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
