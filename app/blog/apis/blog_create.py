from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import generics
from blog.models import Blog
from blog.serializer import BlogCreateSerializer

User = get_user_model()


class BlogListCreateView(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = BlogCreateSerializer

    def get_serializer_context(self):
        """
        해당 요청에 대한 유저 정보를 넘겨 주기 위해서 사용
        :return:
        """
        return {'request': self.request}

    def get_queryset(self):
        queryset = Blog.objects.select_related('travel_reservation').filter(
            travel_reservation__member=self.request.user)
        return queryset
