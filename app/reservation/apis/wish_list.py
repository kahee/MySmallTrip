from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from reservation.models import WishTravel
from reservation.serializer.wish_list import WishListCreateSerializer
from travel.serializer import TravelInformationWishListSerializer

User = get_user_model()


class WishTravelListCreateView(APIView):
    # 모델 명 바꾸기
    # 1. WishTraveled
    # 2. api view create ,  reterive, delete 이렇게 나눠서

    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        user = User.objects.get(username=request.user)
        wish_lists = user.wish_products.all()
        serializer = TravelInformationWishListSerializer(wish_lists, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        """
        위시리스트 생성
        :param request:
        :return:
        """

        context = {
            "request": self.request,
        }

        serializer = WishListCreateSerializer(data=request.data, context=context)

        if serializer.is_valid(raise_exception=True, ):
            wishlist_created = serializer.save()
            print(wishlist_created)
            if wishlist_created:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(status.HTTP_400_BAD_REQUEST)


#  해당 상품이 위시리스트에 있는지 체크
class TravelInfoDoesNotExists(APIException):
    status_code = 400
    default_detail = '해당 상품이 위시리스트에 없습니다.'
    default_code = 'travel_info_DoesNotExists'


class WishTravelDeleteView(APIView):
    def delete(self, request):
        """
        위시리스트 삭제
        :param request:
        :return:
        """

        try:
            wish_product = WishTravel.objects.get(travel_info=request.data['travel_info'], user=request.user)

            if wish_product:
                wish_product.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status.HTTP_400_BAD_REQUEST)

        except WishTravel.DoesNotExist:
            raise TravelInfoDoesNotExists
#
