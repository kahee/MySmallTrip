from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from travel.models import CityInformation
from travel.serializer.city_serializer import CityInformationSerializer
from rest_framework.renderers import JSONRenderer


class CityInformationView(APIView):
    renderer_classes = (JSONRenderer,)
    def get(self, request,format=None):
        city_informations = CityInformation.objects.all()
        serializer = CityInformationSerializer(city_informations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
