from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from travel.models import TravelInformation
from travel.serializer import TravelInformationSerializer, TravelInformationDetailCalenderSerializer


class TravelInformationDetailCalenderView(APIView):
    def get(self, request, *args, **kwargs):
        # print(request.META)
        people = request.META.get('HTTP_PEOPLE')
        travel_detail_informations = TravelInformation.objects.filter(city__name=kwargs['cityname']).filter(
            pk=kwargs['pk'])
        serializer = TravelInformationDetailCalenderSerializer(travel_detail_informations )

        # serializer = TravelInformationDetailCalenderSerializer(data={'people':people})

        # serializer.is_valid()
        return Response(serializer.data, status=status.HTTP_200_OK)
