from django.urls import path

from .apis.user_detail import UserDetailView, UserChangeImageView, UserChangePhoneNumberView, UserChangePasswordView

urlpatterns = [
    path('info/', UserDetailView.as_view(), name='user-detail'),
    path('info/password/', UserChangePasswordView.as_view(), name='user-password'),
    path('info/img-change/', UserChangeImageView.as_view(), name='user-image-change'),
    path('info/phone-change/', UserChangePhoneNumberView.as_view(), name='user-phonenumber-change'),
]
