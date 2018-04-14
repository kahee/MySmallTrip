from django.urls import path

from blog.apis import BlogView

urlpatterns = [
    path('', BlogView.as_view(), name='blog'),
]