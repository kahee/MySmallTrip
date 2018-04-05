from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FrequentQuestion
from .serializer import FrequentQuestionSerializer


class FrequentQuestionView(APIView):
    def get(self, request):
        faq = FrequentQuestion.objects.all()
        serializer = FrequentQuestionSerializer(faq, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
