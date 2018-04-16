from django.urls import path

from blog.apis import BlogListCreateView

urlpatterns = [
    path('', BlogListCreateView.as_view(), name='blog'),
]