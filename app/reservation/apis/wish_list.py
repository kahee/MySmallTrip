from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from reservation.models import WishList
from reservation.serializer.wish_list import WishListCreateSerializer, WishListDeleteSerializer

User = get_user_model()


class WishListView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

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

    def delete(self, request):
        """
        위시리스트 삭제
        :param request:
        :return:
        """

        context = {
            "request": self.request,
        }

        serializer = WishListDeleteSerializer(data=request.data, context=context)

        if serializer.is_valid(raise_exception=True):

            user = User.objects.get(username=serializer.validated_data['user'])
            wish_product = user.wish_products_info_list.get(travel_info=serializer.validated_data['travel_info'])
            delete = wish_product.delete()

            if delete:
                return Response(status=status.HTTP_204_NO_CONTENT)

        else:
            return Response(status.HTTP_400_BAD_REQUEST)
