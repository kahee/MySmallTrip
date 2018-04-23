from django.test import TestCase

# Create your tests here.
from rest_framework import status
from rest_framework.test import APITestCase

from .apis import ReservationCreateView, ReservationCreateSerializer
from .models import Reservation


class ReservationCreateTest(APITestCase):
    MODEL = Reservation
    VIEW = ReservationCreateView
    URL = '/reservation/'

    TEST_PRODUCT_ID = 1
    TEST_START_DATE = '2018-04-24'
    TEST_RESERVE_PEOPLE = 3
    TEST_IS_CANCELED = False
    TEST_TOTAL_PRICE = 0
    TEST_MEMBER = ''

    CREATE_NUM = 10

    def setUp(self, num):
        for i in range(num):
            self.MODEL.objects.create(
                id=i,
                start_date=self.TEST_START_DATE,
                reserve_people=self.TEST_RESERVE_PEOPLE,
                is_canceled=self.TEST_IS_CANCELED,
            )

    def reservation_create_test(self):
        # self.setUp(self.CREATE_NUM)
        # print('예약테스트')
        # print('success')

        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        reservations = Reservation.objects.all()
        serializer = ReservationCreateSerializer(reservations, many=True)
        self.assertEqual(response.data, serializer.data)
        # print(response.data)
        # print(serializer.data)
