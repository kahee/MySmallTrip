from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from reservation.models import WishTravel
from travel.models import CityInformation, CompanyInformation
from ..models import TravelInformation

User = get_user_model()


class TestWishTravelCreate(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_user(
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
        self.test_travel_info = TravelInformation.objects.create(
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

        self.create_url = reverse('wish-list')

    def test_wish_travel_create(self):
        """
        1. 토큰 로그인
        2. travel_info post 요청
        2-1. travel_info가 TravelInformation에 없는 경우 에러
        2-2. travel_info로 이미 WishTravel 있는 경우 에러
        3. WishTravel 목록에 생성
        :return:
        """

        data = {
            'username': 'yuygh131@gmail.com',
            'password': 'rkgml12345',
        }
        response = self.client.post('/login/', data)
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)

        # request에 필요한 사용자 토큰 헤더에 포함
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        data = {
            'travel_info': '1',
        }

        # travel_info 에 대해 wishtravel 목록 생성
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(WishTravel.objects.count(), 1)


class TestWishTravelDelete(APITestCase):
    def setUp(self):
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

        self.test_wish_list_created = WishTravel.objects.create(
            travel_info=travel_info,
            user=user,
        )

        self.create_url = reverse('wish-list-delete')

    def test_wish_travel_delete(self):
        """
        1. 토큰 로그인
        2. travel_info delete 요청
        2-1. travel_info 가 TravelInformation 에 없는 경우
        2-2. travel_info 가 유저의 WishTravel에 없는 경우
        3. WishTravel 삭제
        :return:
        """

        data = {
            'username': 'yuygh131@gmail.com',
            'password': 'rkgml12345',
        }
        response = self.client.post('/login/', data)
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)

        # request에 필요한 사용자 토큰 헤더에 포함
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        # Travel_info가 위시리스트에 없는 경우
        data = {
            'travel_info': '2',
        }
        response = self.client.delete(self.create_url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(WishTravel.objects.count(), 1)

        # Travel_info pk가 없는 경우
        data = {
            'travel_info': '2',
        }
        response = self.client.delete(self.create_url, data)
        self.assertEqual(response.status_code, 400)
        self.assertNotIn(2, TravelInformation.objects.all())

        # travel_info 에 대해 wishtravel 목록 삭제
        data = {
            'travel_info': '1',
        }
        response = self.client.delete(self.create_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(WishTravel.objects.count(), 0)
