from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import generics
from ..models import Blog
from ..serializer import BlogUpdateSerializer

User = get_user_model()


class BlogUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = BlogUpdateSerializer
    lookup_field = 'pk'

    def get_serializer_context(self):
        """
        해당 요청에 대한 유저 정보를 넘겨 주기 위해서 사용
        :return:
        """
        return {'request': self.request}

    def get_queryset(self):
        queryset = Blog.objects.select_related('travel_reservation').filter(
            travel_reservation__member=self.request.user).filter(pk=self.request.data['pk'])
        return queryset

    def get_object(self):
        queryset= self.filter_queryset(self.get_queryset())
        obj = queryset.get()
        return obj