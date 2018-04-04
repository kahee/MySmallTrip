from django.urls import path

from .apis.user_detail import UserDetailView, UserDetailImageView

urlpatterns = [
    path('info/', UserDetailView.as_view(), name='user-detail'),
    path('info/img_change/', UserDetailImageView.as_view(), name='user-image-change')
]
