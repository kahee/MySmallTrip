from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase

from .apis import CityInformationView
from .models import TravelInformation, CityInformation


class CityListTest(APITestCase):
    MODEL = CityInformation
    VIEW = CityInformationView
    URL = '/travel-information/'

    TEST_NAME = 'Paris'
    TEST_CONTINENT = 'Europe'
    TEST_NATIONALITY = 'France'

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
        # self.assertEqual(len(response.data), self.CREATE_NUM)
        #
        # self.assertEqual(response.data['name'], self.TEST_NAME)
        # self.assertEqual(response.data['continent'], self.TEST_CONTINENT)
