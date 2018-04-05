from django.contrib.auth import get_user_model
from django.core.files import File
from rest_framework import status

import requests

from utils.file import download, get_buffer_ext

User = get_user_model()


class APIFacebookBackends:
    # CLIENT_ID = FACEBOOK_APP_ID
    # CLIENT_SECRET = FACEBOOK_SECRET_CODE

    def authenticate(self, request, access_token):
        params = {
            'access_token': access_token,
            'fields': ','.join([
                'id',
                'name',
                'picture.width(2500)',
                'first_name',
                'last_name',
                'email',
            ])
        }
        response = requests.get('https://graph.facebook.com/v2.12/me', params)

        if response.status_code == status.HTTP_200_OK:
            user_info = response.json()

            facebook_id = user_info['id']
            name = user_info['name']
            url_img_profile = user_info['picture']['data']['url']

            # facebook유저중에 email이 없는 경우가 있어서 없는경우는 email을 빈값으로 입력
            if 'email' in user_info:
                email = user_info['email']
            else:
                email = ''

            try:
                # email이 unique이기 때문에 email로 구분한다.
                user = User.objects.get(username=facebook_id)

            except:
                user = User.objects.create_user(
                    email=email,
                    username=facebook_id,
                    first_name=name,
                    is_facebook_user=True,
                    # img_profile=img_profile,
                    # 이미지는 따로 저장한다.
                )

            temp_file = download(url_img_profile)

            file_name = '{username}.{ext}'.format(
                username=facebook_id,
                ext=get_buffer_ext(temp_file),
            )
            if user.img_profile:
                user.img_profile.delete()
            user.img_profile.save(file_name, File(temp_file))

            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
