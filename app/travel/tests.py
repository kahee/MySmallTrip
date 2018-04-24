import os
import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.authtoken.models import Token
# Create your tests here.
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from reservation.models import Reservation
from .apis import CityInformationView, TravelInformationView, TravelInformationDetailCalenderView
from .models import TravelInformation, CityInformation, CompanyInformation, TravelSchedule

User = get_user_model()


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
        self.assertEqual(len(response.data), self.CREATE_NUM)
        self.assertEqual(CityInformation.objects.count(), self.CREATE_NUM)


class TravelProductListTest(APITestCase):
    MODEL = TravelInformation
    VIEW = TravelInformationView
    CITY_NAME = 'dublin'
    URL = '/travel-information/' + CITY_NAME + '/'

    TEST_TRAVEL_ID = 1
    TEST_NAME = '더블리너스 - 더블린 사람들처럼 빠른걸음 속의 여유를 갖는 워킹투어 (1인~최대10인)'
    TEST_LANGUAGE = 'KOREAN'
    TEST_TIME = '2시간'
    CREATE_NUM = 10

    def create_travel_product_list(self, num):
        city = CityInformation.objects.create(
            name=self.CITY_NAME,
            continent='Europe',
            nationality='Germany',
        )
        company = CompanyInformation.objects.create(
            name='hong',
            info='test_info_hong',
        )
        for i in range(num):
            self.MODEL.objects.create(
                travel_id=self.TEST_TRAVEL_ID,
                name=self.TEST_NAME,
                product_type='단체 투어',
                language='한국어',
                city=city,
                time='3시간',
                company=company,
                description_title='더블린에서 생활하듯이 구석구석 둘러보며 기네스와 아이리쉬 커피로 더블린사람들의 흥과 여유도 함께 즐겨보아요',
                description='test_description',
            )

    def test_Travel_product_list(self):
        self.create_travel_product_list(self.CREATE_NUM)
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.CREATE_NUM)
        self.assertEqual(TravelInformation.objects.count(), self.CREATE_NUM)


class TravelCalenderTest(APITestCase):
    MODEL = TravelInformation
    VIEW = TravelInformationDetailCalenderView
    CITY_NAME = 'dublin'

    PEOPLE =2
    URL = '/travel-information/dublin/1/calender/?people=' + str(PEOPLE)

    TEST_TRAVEL_ID = 1
    TEST_NAME = '더블리너스 - 더블린 사람들처럼 빠른걸음 속의 여유를 갖는 워킹투어 (1인~최대10인)'
    TEST_LANGUAGE = 'KOREAN'
    TEST_TIME = '2시간'
    CREATE_NUM = 1
    TEST_DATETIME = '2018-04-01'

    TEST_RESERVED_PEOPLE = 3
    TEST_MAX_PEOPLE = 5

    def create_travel_schedule_list(self):
        user = User.objects.create_user(
            email='hsj2334@gmail.com',
            username='hong',
            password='tjrwo123',
            first_name='hong',
        )
        city = CityInformation.objects.create(
            name=self.CITY_NAME,
            continent='Europe',
            nationality='Germany',
        )
        company = CompanyInformation.objects.create(
            name='hong',
            info='test_info_hong',
        )
        travel_info = TravelInformation.objects.create(
            travel_id=self.TEST_TRAVEL_ID,
            name=self.TEST_NAME,
            product_type='단체 투어',
            language='한국어',
            city=city,
            time=self.TEST_TIME,
            company=company,
            description_title='더블린에서 생활하듯이 구석구석 둘러보며 기네스와 아이리쉬 커피로 더블린사람들의 흥과 여유도 함께 즐겨보아요',
            description='test_description',
            max_people=self.TEST_MAX_PEOPLE
        )
        TravelSchedule.objects.create(
            travel_info=travel_info,
            start_date=datetime.datetime.now(),
            reserved_people=self.TEST_RESERVED_PEOPLE
            # datetime.datetime.strptime(self.TEST_DATETIME, '%Y-%m-%d') + datetime.timedelta(days=1)
        )

    def login(self):
        data = {
            'username': 'hong',
            'password': 'tjrwo123',
        }
        response = self.client.post('/login/', data)
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)
        # print(response.data['token'])
        # print(token.key)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def setUp(self):
        self.create_travel_schedule_list()
        self.login()

    def test_schedule_create_not_exists_travel_schedule(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(TravelInformation.objects.count(), 1)

    def test_compare_with_max_vs_reserved_people(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        travel_infomation_list = response.data[0]
        max_people = travel_infomation_list['max_people']
        travel_schedule_list = travel_infomation_list['travel_info'][0]
        reseved_people = travel_schedule_list['reserved_people']
        people = self.PEOPLE

        self.assertEqual(max_people, self.TEST_MAX_PEOPLE)
        self.assertEqual(reseved_people, self.TEST_RESERVED_PEOPLE)

        if max_people >= reseved_people + people:
            print("예약가능")
        else:
            print("예약불가")
        