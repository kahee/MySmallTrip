from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from members.serializer import UserSerializer


class UserCreate(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
