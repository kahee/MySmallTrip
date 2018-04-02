from django.urls import path

from .apis import UserCreate

urlpatterns = [
    path('sign-up/', UserCreate.as_view(), name='sign-up'),
]
