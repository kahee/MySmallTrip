from django.contrib.auth import get_user_model

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

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

        if serializer.is_valid(raise_exception=True,):
            wishlist = serializer.save()
            print(wishlist)
            if wishlist:
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(status.HTTP_400_BAD_REQUEST)

    # def delete(self, request):
    #
    #     context = {
    #         "request": self.request,
    #     }
    #
    #     serializer = WishListSerializer(data=request.data, context=context)
    #
    #     if serializer.is_valid(raise_exception=True):
    #
    #
    #         return Response(status=status.HTTP_204_NO_CONTENT)
