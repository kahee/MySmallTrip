from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import generics
from blog.models import Blog, BlogImage
from blog.serializer import BlogCreateSerializer

User = get_user_model()


#
# class BlogView(APIView):
#     permission_classes = (
#         permissions.IsAuthenticated,
#     )
#     #
#     # def get(self, request):
#     #     """
#     #     자신이 쓴 상품 후기 리스트 출력
#     #     :param request:
#     #     :return:
#     #     """
#     #     blog = Blog.objects.all().filter(travel_Reservation__member=request.user)
#     #     serializer = BlogSerializer(blog, many=True)
#     #     return Response(serializer.data, status=status.HTTP_200_OK)
#
#     # blog pk 값 받아서 수정 ,삭제 , 생성
#     def post(self, request):
#         """
#         예약한 상품에 대해서 후기 작성
#         :param request:
#         :return:
#         """
#         serializer = BlogCreateSerializer(data=request.data)
#         print(serializer)
#
#         if serializer.is_valid(raise_exception=True):
#             print(serializer.validated_data)
#             blog = serializer.save()
#
#             if 'images' in serializer.validated_data:
#                 blog.images = serializer.validated_data['images']
#                 blog.save()
#
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)


class BlogListCreateView(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = BlogCreateSerializer

    def list(self, request):
        queryset = Blog.objects.select_related('travel_reservation').filter(travel_reservation__member=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = BlogCreateSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            blog = serializer.save()
            print(blog)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
