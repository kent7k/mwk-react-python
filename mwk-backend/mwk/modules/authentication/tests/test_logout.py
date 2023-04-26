import copy
import os
from base64 import b64encode
from datetime import datetime, timedelta
from string import ascii_letters

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from djoser.utils import encode_uid
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework.test import APITestCase

from mwk.modules.authentication.models import Profile
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

    def authenticate(self, token: str) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def login(self):
        url = reverse('login')
        data = self.login_data
        response = self.client.post(url, data)

        return response

    def logout(self):
        url = reverse('logout')
        data = {}
        response = self.client.post(url, data)

        return response

    def logoutall(self):
        url = reverse('logout_all')
        data = {}
        response = self.client.post(url, data)

        return response

    def test_logout(self):
        """Test logout user"""

        # Login

        response = self.login()

        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in response.data)

        token: str = response.data.get('token')
        self.authenticate(token)

        # Logout

        response = self.logout()

        self.assertEqual(response.status_code, 204)

    def test_logout_not_authorized(self):
        """Test logout user which not authorized"""

        response = self.logout()

        self.assertEqual(response.status_code, 401)

    def test_logoutall(self):
        """Test logoutall user (destroy all tokens)"""

        # Login

        first_response, second_response = self.login(), self.login()
        responses = (first_response, second_response)

        self.assertTrue(
            all(map(lambda response: response.status_code == 200, responses))
        )
        self.assertTrue(all(map(lambda response: 'token' in response.data, responses)))

        first_token = first_response.data.get('token')
        self.authenticate(first_token)

        # Logout

        response = self.logoutall()

        self.assertEqual(response.status_code, 204)

    def test_logoutall_not_authorized(self):
        """Test logoutall user (destroy all tokens) which not authorized"""

        response = self.logoutall()

        self.assertEqual(response.status_code, 401)
