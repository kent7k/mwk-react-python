import copy
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

    def test_login_with_inactive_account(self):
        """A test that tries to login with inactive account"""
        inactive_user: User = User.objects.create_user(
            'Authentication_test_case_Inactive', self.email, self.password
        )
        inactive_user.is_active = False
        inactive_user.save()

        url = reverse('login')
        data = {'username': inactive_user.username, 'password': self.password}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data.get('non_field_errors')[0].code, 'authorization')
