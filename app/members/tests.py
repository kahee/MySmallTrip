from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory

User = get_user_model()


class test_create_user(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            email='yuygh131@gmail.com',
            username='yuygh131@gmail.com',
            password='rkgml12345',
            first_name='kahee',
        )

        self.create_url = reverse('sign-up')

    def test_create_user(self):
        data = {
            'email': '12345@gmail.com',
            'first_name': 'kahee',
            'password': 'rkgml12345',
        }

        response = self.client.post(self.create_url, data, format='json')

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], response.data['username'])
        self.assertEqual(response.data['email'], data['email'])
        # self.client.login(username='12345@gmail.com', password='rkgml12345')
