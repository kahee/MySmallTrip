from django.urls import path

# from travel.apis import TravelInformationView
# from travel.apis.main import CityInformationView
from travel.apis import TravelInformationView
from travel.apis.list_detail import TravelInformationDetailView
from travel.apis.main import CityInformationView

urlpatterns = [
    path('', CityInformationView.as_view(), name='city-information'),
    # path('<int:travel_id>/', TravelInformationView.as_view(), name='travel-information'),
    path('<str:cityname>/',TravelInformationView.as_view(), name='travel-information'),
    path('<str:cityname>/<int:pk>', TravelInformationDetailView.as_view(), name='travel-information-detail')

    # path('travel-detail/', TravelInformationDetailView.as_view(),name='travel-information-detail')
]
