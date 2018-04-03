from django.urls import path

from .apis import UserCreate, LoginfromAuthTokenView

urlpatterns = [
    path('sign-up/', UserCreate.as_view(), name='sign-up'),
    path('login/', LoginfromAuthTokenView.as_view(), name='login'),
]
