import os
from base64 import b64encode
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from knox.models import AuthToken
from rest_framework.test import APITestCase


class AuthenticationTestCase(APITestCase):
    """Registration and login test"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='AuthenticationTestUser',
            email='authenticationtestcaseuser@gmail.com',
            password='asd123321'
        )
        self.token = AuthToken.objects.create(user=self.user)[-1]
        self.login_data = {
            'username': self.user.username,
            'password': 'asd123321'
        }
        self.media_path = os.path.join(settings.TESTS_MEDIA_ROOT, 'authentication')
        self.avatar = self._encode_file('avatar.png')
        self.fake_avatar = self._encode_file('alt-avatar.txt')
        self.register_data = {
            'email': 'authenticationtestcase@gmail.com',
            'username': 'AuthenticationTest',
            'password': 'asd123321',
            'first_name': 'John',
            'last_name': 'Doe',
            'profile': {
                'birthday': self._get_birthday(),
                'avatar': self.avatar,
            }
        }

    def _get_birthday(self):
        return (datetime.today() - timedelta(days=(365 * 15))).date().strftime('%Y-%m-%d')

    def _encode_file(self, filename):
        with open(os.path.join(self.media_path, filename), 'rb') as file:
            return b64encode(file.read())

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
