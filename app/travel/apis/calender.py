from rest_framework import status, generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import TravelInformation
from ..serializer import TravelInfoSerializer


class TravelInformationDetailCalenderView(APIView):

    def get(self, request, *args, **kwargs):
        # people = request.META.get('HTTP_PEOPLE')
        people = kwargs['people']
        travel_detail_informations = TravelInformation.objects.filter(city__name=kwargs['cityname']).filter(
            pk=kwargs['pk'])

        serializer = TravelInfoSerializer(data=travel_detail_informations, context={'people': people}, many=True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)
