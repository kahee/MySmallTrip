import filecmp
import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage
from django.core.files.temp import NamedTemporaryFile
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
        # /.media/user/cat.png
        # 테스트용 user 파일을 불러옴
        file_path = os.path.join(settings.MEDIA_ROOT, 'user', 'cat.png')
        print(file_path)

        # with create(post) 요청
        with open(file_path, 'rb') as f:
            # format에 json으로 설정하면 이미지 파일 불러오기를 못함.

            response = self.client.post(self.create_url, {
                'email': '12345@gmail.com',
                'first_name': 'kahee',
                'password': 'rkgml12345',
                'phone_number': '010-2345-0232',
                'img_profile': f,
            })

        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], response.data['username'])
        self.assertEqual(response.data['email'], '12345@gmail.com')
        self.assertEqual(response.data['phone_number'], '010-2345-0232')

        user = User.objects.get(pk=2)
        uploaded_file = user.img_profile.read()

        temp_file = NamedTemporaryFile()
        temp_file.write(uploaded_file)
        print('file_path', file_path)
        print('temp_file.name', temp_file.name)

        self.assertTrue(filecmp.cmp(file_path, temp_file.name))
