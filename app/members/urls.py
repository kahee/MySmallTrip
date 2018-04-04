from django.urls import path

from .apis import UserCreate, FacebookLogin

urlpatterns = [
    path('sign-up/', UserCreate.as_view(), name='sign-up'),
    path('facebook-login/',FacebookLogin.as_view(), name='facebook-login'),
]
