from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase

from .apis import CityInformationView, TravelInformationView
from .models import TravelInformation, CityInformation


class CityListTest(APITestCase):
    MODEL = CityInformation
    VIEW = CityInformationView
    URL = '/travel-information/'

    TEST_NAME = 'dublin'
    TEST_CONTINENT = 'Europe'
    TEST_NATIONALITY = 'ireland'

    CREATE_NUM = 10

    def create_city(self, num):
        for i in range(num):
            self.MODEL.objects.create(
                id=i,
                name=self.TEST_NAME,
                continent=self.TEST_CONTINENT,
                nationality=self.TEST_NATIONALITY,
            )

    def test_city_list(self):
        self.create_city(self.CREATE_NUM)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(len(response.data))
        print(self.CREATE_NUM)
        self.assertEqual(len(response.data), self.CREATE_NUM)

        # self.assertEqual(response.data['name'], self.TEST_NAME)
        # self.assertEqual(response.data['continent'], self.TEST_CONTINENT)

# class TravelProductListTest(APITestCase):
#     MODEL = TravelInformation
#     VIEW = TravelInformationView
#     CITY_NAME ='dublin/'
#     URL = '/travel-information/'+CITY_NAME
#
#     TEST_TRAVEL_ID = 12345
#     TEST_NAME = '더블린 여행가기 1'
#     TEST_CITY = CityInformation.objects.first()
#     TEST_LANGUAGE = 'KOREAN'
#     TEST_TIME = '2시간'
#     CREATE_NUM = 10
#
#     def create_travel_product_list(self):
#         for i in range(self.CREATE_NUM):
#             self.MODEL.objects.create(
#                 id=i,
#                 travel_id=self.TEST_TRAVEL_ID,
#                 name=self.name,
#                 city=self.TEST_CITY,
#                 language=self.TEST_LANGUAGE,
#                 time=self.TEST_TIME,
#                 # company = self.
#             )
