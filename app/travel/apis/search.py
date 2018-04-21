from rest_framework import generics, permissions, filters
from travel.models import TravelInformation
from travel.serializer import TravelInformationSerializer


class SearchTravelInformationView(generics.ListCreateAPIView):
    serializer_class = TravelInformationSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    # filter_backends 의 경우 반드시 튜플로 쉼표를 적어야 한다.
    filter_backends = (filters.SearchFilter,)
    queryset = TravelInformation.objects.all()
    search_fields = ('name', 'description', 'description_title')