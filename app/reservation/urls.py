from django.urls import path

from .apis import ReservationView, ReservationCancelView

urlpatterns = [
    # 1.상품예약 url
    # 2.상품취소 url(정할것: 취소할 때, 정보를 delete할 것인가? iscanceled를 'y'처리할 것인가?
    # 3.상품예약 리스트 url

    path('', ReservationView.as_view(), name='reservation'),
    path('cancel/<int:pk>/', ReservationCancelView.as_view(), name='reservation-cancel'),
    # path('list/',ReservationListView.as_view(),)

]
