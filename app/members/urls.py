from django.urls import path

from members.apis import FacebookLogin
from .apis.user_detail import UserDetailView, UserDetailImageView

urlpatterns = [
    path('info/', UserDetailView.as_view(), name='user-detail'),
    path('info/img-change/', UserDetailImageView.as_view(), name='user-image-change'),
]
