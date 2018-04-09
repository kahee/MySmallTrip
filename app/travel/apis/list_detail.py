
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from travel.models import TravelInformation
from travel.serializer.travel_serializer_detail import TravelInformationDetailSerializer


class TravelInformationDetailView(APIView):
    def get(self, request, **kwargs):
        # travel_detail_informations = TravelInformation.objects.filter(city__name=kwargs['cityname'])
        travel_detail_informations = TravelInformation.objects.filter(city__name=kwargs['cityname']).filter(pk=kwargs['pk'])
        serializer = TravelInformationDetailSerializer(travel_detail_informations,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
