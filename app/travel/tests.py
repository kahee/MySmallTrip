from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase

from .apis import CityInformationView
from .models import TravelInformation, CityInformation


class TestMainListTest(APITestCase):
    MODEL = CityInformation
    VIEW = CityInformationView
    URL = '/travel-information/'

    TEST_NAME = 'Paris'
    TEST_CONTINENT = 'Europe'
    TEST_NATIONALITY = 'France'

    def create_city(self):
        self.MODEL.objects.create(
            id=1,
            name=self.TEST_NAME,
            continent=self.TEST_CONTINENT,
            nationality=self.TEST_NATIONALITY,
        )

    def test_list(self):
        self.create_city()
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response.data,))
