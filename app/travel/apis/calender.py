from rest_framework import status, generics, permissions
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import TravelInformation
from ..serializer import TravelInfoSerializer


class TravelInformationDetailCalenderView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request, *args, **kwargs):
        # people = request.META.get('HTTP_PEOPLE')
        # people = kwargs['people']
        people = int(self.request.query_params.get('people', None))
        if people is not None:
            context = {
                'request': self.request,
                'people': people,
            }
            travel_detail_informations = TravelInformation.objects.filter(city__name=kwargs['cityname']).filter(
                pk=kwargs['pk'])

            serializer = TravelInfoSerializer(data=travel_detail_informations, context=context, many=True)
            serializer.is_valid()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(data={'people': '예약할 사람수는 필수값입니다.'}, status=status.HTTP_400_BAD_REQUEST)
