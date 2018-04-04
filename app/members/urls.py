from django.urls import path

from members.apis.user_detail import UserDetailView
from .apis import UserCreateView, LoginfromAuthTokenView

urlpatterns = [
    path('info/', UserDetailView.as_view(), name='user-detail')
]
