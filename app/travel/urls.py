from django.urls import path

from travel.apis import TravelInformationView

urlpatterns = [
    path('', TravelInformationView.as_view(), name='travelinformation'),

]
