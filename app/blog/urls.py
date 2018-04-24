from django.urls import path

from blog.apis import BlogListCreateView
from blog.apis import BlogUpdateDeleteView

urlpatterns = [
    path('', BlogListCreateView.as_view(), name='blog'),
    path('update/', BlogUpdateDeleteView.as_view(), name='blog-update'),
    # path('delete/,',BlogDeleteView.as_view(),name='blog-delete'),
]
