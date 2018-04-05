from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import FrequentQuestionSerializer


class FrequentQuestionView(APIView):
    def get(self, request):
        serializer = FrequentQuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
