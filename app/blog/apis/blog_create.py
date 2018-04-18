from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework import generics
from blog.models import Blog
from blog.serializer import BlogCreateSerializer, BlogListSerializer

User = get_user_model()


class BlogListCreateView(generics.ListCreateAPIView):
    permission_classes = (
        permissions.IsAuthenticated,
    )
    serializer_class = BlogListSerializer

    def list(self, request):
        queryset = Blog.objects.select_related('travel_reservation').filter(travel_reservation__member=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):

        context = {
            "request": self.request,
        }

        serializer = BlogCreateSerializer(data=request.data, context=context)

        if serializer.is_valid(raise_exception=True):

            blog = serializer.save()

            data = {
                'blog': BlogListSerializer(blog).data
            }

            return Response(data, status=status.HTTP_201_CREATED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
