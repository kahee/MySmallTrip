from django.db.models import Q
from rest_framework import generics, status, permissions
from travel.models import TravelInformation
from travel.serializer import TravelInformationSerializer


class SearchTravelInformationView(generics.ListCreateAPIView):
    serializer_class = TravelInformationSerializer
    permission_classes = (
        permissions.IsAuthenticated,
    )
    # get 으로 none 처리

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', None)
        # keyword가 none인 경우엔 모든게 보여짐
        # 예외처리
        # 1. 키워드가 none인 경우 return
        # 2. 검색한 키워드 결과가 없어서 빈 쿼리셋인 경우
        if keyword is not None:
            queryset = TravelInformation.objects.filter(
                Q(name__contains=keyword) | Q(description__contains=keyword)
                | Q(description_title__contains=keyword)
            ).distinct()

        # 검색 출력을 pk값으로
        return queryset.order_by('pk')
