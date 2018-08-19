import filecmp
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.temp import NamedTemporaryFile

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class TestCreateUser(APITestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(
            email='yuygh131@gmail.com',
            username='yuygh131@gmail.com',
            password='rkgml12345',
            first_name='kahee',
        )

        self.create_url = reverse('sign-up')

    def test_create_user(self):
        # /.media/user/cat.png
        # 테스트용 user 파일을 불러옴
        file_path = os.path.join(settings.MEDIA_ROOT, 'user', 'cat.jpg')
        print(file_path)

        # with create(post) 요청
        with open(file_path, 'rb') as f:
            # format에 json으로 설정하면 이미지 파일 불러오기를 못함.

            response = self.client.post(self.create_url, {
                'email': 'rkgml12345@gmail.com',
                'first_name': 'kahee',
                'password': 'rkgml12345',
                'password2': 'rkgml12345',
                'phone_number': '010-2345-0232',
                'img_profile': f,
            })

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], response.data['username'])
        self.assertEqual(response.data['email'], 'rkgml12345@gmail.com')
        self.assertEqual(response.data['phone_number'], '010-2345-0232')

        user = User.objects.get(pk=2)
        uploaded_file = user.img_profile.read()

        temp_file = NamedTemporaryFile()
        temp_file.write(uploaded_file)
        print('file_path', file_path)
        print('temp_file.name', temp_file.name)

        self.assertTrue(filecmp.cmp(file_path, temp_file.name))

    def test_create_user_with_short_password(self):
        # 비밀번호가 8자 이하일때 오류 체크
        data = {
            'email': 'rkgml12345@gmail.com',
            'first_name': 'kahee',
            'password': 'rkgml',
            'password2': 'rkgml',
            'phone_number': '010-2345-0232',
            'img_profile': '',
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_not_match_password(self):
        # 비밀번호가 일치하지 않을 때
        data = {
            'email': 'rkgml12345@gmail.com',
            'first_name': 'kahee',
            'password': 'sdfg',
            'password2': 'sdfgsdd',
            'phone_number': '010-2345-0232',
            'img_profile': '',
        }

        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_normal(self):
        data = {
            'email': 'rkgml12345@gmail.com',
            'first_name': 'kahee',
            'password': 'password',
            'password2': 'password',
            'phone_number': '010-2345-0232',
            'img_profile': '',
        }

        response = self.client.post(self.create_url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_preexisting_email(self):
        data = {
            'email': 'yuygh131@gmail.com',
            'first_name': 'kahee',
            'password': 'rkgml12345',
            'password2': 'rkgml12345',
            'phone_number': '010-2345-0232',
            'img_profile': '',
        }

        response = self.client.post(self.create_url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        data = {
            'email': 'yuygh131',
            'first_name': 'kahee',
            'password': 'rkgml12345',
            'password2': 'rkgml12345',
            'phone_number': '010-2345-0232',
            'img_profile': '',
        }

        response = self.client.post(self.create_url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)