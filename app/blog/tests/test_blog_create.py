import datetime

from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from ..models import Blog
from reservation.models import Reservation
from travel.models import CityInformation, CompanyInformation, TravelInformation, TravelSchedule

User = get_user_model()


class BlogCreateListTest(APITestCase):
    def set_up_test_data(self):
        """
        필요 데이터
        1. reservation
        2. travel_schedule
        3. user
        3. travel_information
        :return:
        """

        user = self.test_user = User.objects.create_user(
            email='yuygh131@gmail.com',
            username='yuygh131@gmail.com',
            password='rkgml12345',
            first_name='kahee',
        )

        city = self.test_city_info = CityInformation.objects.create(
            name='더블린',
            continent='유럽',
            nationality='독일',
        )
        company = self.test_company_info = CompanyInformation.objects.create(
            name='kim',
            info='test_kim',
        )
        travel_info = self.test_travel_info = TravelInformation.objects.create(
            travel_id=1,
            name='더블리너스 - 더블린 사람들처럼 빠른걸음 속의 여유를 갖는 워킹투어 (1인~최대10인)',
            product_type='단체 투어',
            language='한국어',
            city=city,
            time='3시간',
            company=company,
            description_title='더블린에서 생활하듯이 구석구석 둘러보며 기네스와 아이리쉬 커피로 더블린사람들의 흥과 여유도 함께 즐겨보아요',
            description='test_description',
        )

        travel_schedule = self.test_travel_schedule_info = TravelSchedule.objects.create(
            travel_info=travel_info,
            start_date=datetime.datetime.now()
        )

        reservation = self.test_reservation_info = Reservation.objects.create(
            travel_schedule=travel_schedule,
            member=user,
        )

    def login(self):
        data = {
            'username': 'yuygh131@gmail.com',
            'password': 'rkgml12345',
        }
        response = self.client.post('/login/', data)
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def setUp(self):
        self.set_up_test_data()
        self.login()
        self.create_url = reverse('blog')

    def test_blog_create_not_exists_travel_reservation(self):
        data = {
            'travel_reservation': '2',
            'title': 'test_review',
            'contents': 'test_contents',
            'score': 4,
        }

        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Blog.objects.count(), 0)
        self.assertNotIn(2, Reservation.objects.all())

    def test_blog_create_blank(self):
        data = {
            'travel_reservation': '1',
            'contents': 'test_contents',
            'score': 4,
        }

        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Blog.objects.count(), 0)

    def test_blog_create(self):
        """
        1. 토큰 로그인
        2. travel_reservation, title, contents, score, images로 후기 생성
        2-1. travel_reservation이 회원 예약 리스트에 없는 경우
        2-2. image이외에 정보가 빠졌을 경우
        2-3. 이미 작성된 후기 작성할 경우,
        3. 후기 생성
        :return:
        """

        data = {
            'travel_reservation': '1',
            'title': 'test_review',
            'contents': 'test_contents',
            'score': 4,
        }

        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Blog.objects.count(), 1)

    def test_blog_create_exists_review(self):
        Blog.objects.create(
            travel_reservation=self.test_blog_create_not_exists_travel_reservation(),
            title='test_review',
            contents='test',
            score=4
        )

        data = {
            'travel_reservation': '1',
            'title': 'test_review',
            'contents': 'test_contents',
            'score': 4,
        }

        response = self.client.post(self.create_url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Blog.objects.count(), 1)

    def test_blog_list(self):
        Blog.objects.create(
            travel_reservation=self.test_blog_create_not_exists_travel_reservation(),
            title='test_review',
            contents='test',
            score=4
        )

        response = self.client.get(self.create_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Blog.objects.count(), 1)
