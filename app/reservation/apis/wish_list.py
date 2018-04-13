from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from reservation.models import WishList
from reservation.serializer.wish_list import WishListSerializer

User = get_user_model()


class WishListView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request):

        context = {
            "request": self.request,
        }

        serializer = WishListSerializer(data=request.data, context=context)

        if serializer.is_valid(raise_exception=True, ):
            wishlist = serializer.save()
            print(wishlist)
            if wishlist:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(status.HTTP_400_BAD_REQUEST)

    def delete(self, request):

        context = {
            "request": self.request,
        }

        serializer = WishListSerializer(data=request.data, context=context)

        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(username=serializer.validated_data['user'])
            wish_product = user.wish_products_info_list.get(travel_info=serializer.validated_data['travel_info'])
            delete = wish_product.delete()
            if delete:
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status.HTTP_400_BAD_REQUEST)
