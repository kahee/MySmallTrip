
from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from travel.models import TravelInformation
from travel.serializer import TravelInformationSerializer

class TravelInformationView(APIView):
    def get(self, request, **kwargs):
        # generics.ListAPIView
        # Filtering Doc
        # filter_fields
        #   -> city
        #   -> max_people
        travel_informations = TravelInformation.objects.filter(city__name=kwargs['cityname'])
        serializer = TravelInformationSerializer(travel_informations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

