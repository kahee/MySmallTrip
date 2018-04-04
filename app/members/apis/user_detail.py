from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializer import UserSerializer


class UserDetailView(APIView):
    # 인증 허가
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)