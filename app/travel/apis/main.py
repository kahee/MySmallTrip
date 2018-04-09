from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from travel.models import CityInformation
from travel.serializer.city_serializer import CityInformationSerializer


class CityInformationView(APIView):
    def get(self, request):
        city_informations = CityInformation.objects.all()
        serializer = CityInformationSerializer(city_informations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
