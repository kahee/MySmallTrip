from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class TestChangePassword(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            email='yuygh131@gmail.com',
            username='yuygh131@gmail.com',
            password='rkgml12345',
            first_name='kahee',
        )

        self.create_url = reverse('user-password')

    def test_change_password(self):
        data = {
            'username': 'yuygh131@gmail.com',
            'password': 'rkgml12345',
        }

        response = self.client.post('/login/', data)
        print(response.data)
        user = User.objects.latest('id')
        token, _ = Token.objects.get_or_create(user=user)
        # credentials 은 request에 필요한 요청을 헤더에 포함
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        data = {
            'password': 'rkgml1234',
            'password2': 'rkgml1234',
        }

        response = self.client.patch(self.create_url, data)
        self.assertEqual(response.status_code, 204)

        data = {
            'username': 'yuygh131@gmail.com',
            'password': 'rkgml1234',
        }

        response = self.client.post('/login/',data)
        self.assertEqual(response.status_code, 200)


