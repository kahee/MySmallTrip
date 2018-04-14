from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Blog
from blog.serializer import BlogSerializer
from reservation.models import Reservation

User = get_user_model()


class BlogView(APIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request):
        blog = Blog.objects.all()
        print(blog)
        blog_user = blog.select_related('travel_Reservation').filter(travel_Reservation__member=request.user)
        serializer = BlogSerializer(blog_user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # blog pk 값 받아서 수정 ,삭제 , 생성
    def post(self, request):
        serializer = BlogSerializer(request.data)
