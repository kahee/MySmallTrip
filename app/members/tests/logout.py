from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

User = get_user_model()


class TestLogout(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            email='yuygh131@gmail.com',
            username='yuygh131@gmail.com',
            password='rkgml12345',
            first_name='kahee',
        )

        self.create_url = reverse('logout')

    def test_logout(self):
        self.client.login(username='yuygh131@gmail.com', password='rkgml12345')
