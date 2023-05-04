import os
from base64 import b64encode
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from djoser.utils import encode_uid
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework.test import APITestCase

from mwk.modules.authentication.models.profile import Profile
from mwk.modules.authentication.tokens import AuthenticationToken


class AuthenticationTestCase(APITestCase):
    """Registration and login test"""

    def setUp(self) -> None:
        self.email = 'authenticationtestcaseuser@gmail.com'
        self.email_register = 'authenticationtestcase@gmail.com'
        self.username = 'AuthenticationTest'
        self.first_name = 'John'
        self.last_name = 'Doe'
        self.password = 'asd123321'
        self.birthday = (
            (datetime.today() - timedelta(days=(365 * 15))).date().strftime('%Y-%m-%d')
        )
        self.media_path = os.path.join(settings.TESTS_MEDIA_ROOT, 'authentication')

        with open(os.path.join(self.media_path, 'avatar.png'), 'rb') as file:
            self.avatar = b64encode(file.read())

        with open(os.path.join(self.media_path, 'alt-avatar.txt'), 'rb') as file:
            self.fake_avatar = b64encode(file.read())

        self.user: User = User.objects.create_user(
            'AuthenticationTestUser', self.email, self.password
        )
        self.token: str = AuthToken.objects.create(user=self.user)[-1]

        self.register_data = {
            'email': self.email_register,
            'username': self.username,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'profile': {
                'birthday': self.birthday,
                'avatar': self.avatar,
            },
        }

        self.login_data = {'username': self.user.username, 'password': self.password}

    def activate_user(self, token: str, uid: str) -> Response:
        """Activate the user and return response"""

        url = reverse('activate', kwargs={'uid': uid, 'token': token})
        response = self.client.get(url)

        return response

    def test_registration_and_activation_and_login(self):
        """A test that tries to register and activate user and then performs a login"""

        url = reverse('register')
        data = self.register_data

        response = self.client.post(url, data, format='json')
        register_response_data = response.data
        self.assertEqual(response.status_code, 201)

        users = User.objects.filter(username=register_response_data.get('username'))
        self.assertTrue(users.exists())

        user: User = users.first()

        self.assertTrue(Profile.objects.filter(user=user).exists())
        # TODO: If activation mail is sent, this will be assertFalse
        self.assertTrue(user.is_active)

        avatar_url = f'http://testserver{user.profile.avatar.url}'
        self.assertEqual(
            register_response_data,
            {
                'username': data.get('username'),
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                # TODO: If activation mail is sent, this will be False
                'is_active': True,
                'profile': {
                    'avatar': avatar_url,
                    'birthday': data.get('profile').get('birthday'),
                },
            },
        )

        activation_token = AuthenticationToken().make_token(user)
        uid = encode_uid(user.id)

        response = self.activate_user(activation_token, uid)

        self.assertEqual(response.status_code, 204)
        user.refresh_from_db()
        self.assertTrue(user.is_active)

        url = reverse('login')
        data = {
            'username': register_response_data.get('username'),
            'password': self.password,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)
        self.assertTrue('expiry' in response.data)
        self.assertTrue('user' in response.data)

        user.delete()  # clearing user
