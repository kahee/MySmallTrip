from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class TestLogin(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            email='yuygh131@gmail.com',
            username='yuygh131@gmail.com',
            password='rkgml12345',
            first_name='kahee',
        )
        self.create_url = reverse('login')

    def test_login(self):
        data = {
            'username': 'yuygh131@gmail.com',
            'password': 'rkgml12345',
        }

        response = self.client.post(self.create_url, data)
        print(response.data)
        user = User.objects.latest('id')

        token = Token.objects.get(user=user)
        self.assertEqual(response.data['token'], token.key)


