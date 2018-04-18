from django.urls import path

from travel.apis import TravelInformationView
from travel.apis.list_detail import TravelInformationDetailView
from travel.apis.main import CityInformationView
from travel.apis.calender import TravelInformationDetailCalenderView

urlpatterns = [
    path('', CityInformationView.as_view(), name='city-information'),
    path('<str:cityname>/', TravelInformationView.as_view(), name='travel-information'),
    path('<str:cityname>/<int:pk>/', TravelInformationDetailView.as_view(), name='travel-information-detail'),
    path('<str:cityname>/<int:pk>/calender/', TravelInformationDetailCalenderView.as_view(),
         name='travel-information-detail-reserve'),

]
