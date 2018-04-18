from django.core.handlers import exception
from django.db.models import Q
from requests import Response
from rest_framework import generics, status
from rest_framework.exceptions import APIException

from travel.models import TravelInformation
from travel.serializer import TravelInformationSerializer


#  해당 예약이 회원 예약리스트에 없는 경우
class ReservationDoesNotExists(APIException):
    status_code = 400
    default_detail = '해당 예약 번호가 올바르지 않습니다.'
    default_code = 'reservation_DoesNotExists'


class SearchTravelInformationView(generics.ListCreateAPIView):
    serializer_class = TravelInformationSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword', None)
        # keyword가 none인 경우엔 모든게 보여짐
        # 예외처리
        # 1. 키워드가 none인 경우 return
        # 2. 검색한 키워드 결과가 없어서 빈 쿼리셋인 경우
        if keyword is not None:
            try:
                queryset = TravelInformation.objects.filter(
                    Q(name__contains=keyword) | Q(description__contains=keyword)
                    | Q(description_title__contains=keyword)
                ).distinct()

            except queryset.objects.none():
                raise ReservationDoesNotExists
            # 검색 출력을 pk값으로
            return queryset.order_by('pk')

    # def search(self, request):
    #     queryset = self.get_queryset()
    #
    #     print(queryset)
    #     if queryset.objects.none():
    #         data = {
    #             'message': '검색어를 입력해주세요.'
    #         }
    #         return Response(data, status=status.HTTP_400_BAD_REQUEST)
    #     serializer = self.get_serializer_class(queryset, many=True)
    #     return Response(serializer.data)
