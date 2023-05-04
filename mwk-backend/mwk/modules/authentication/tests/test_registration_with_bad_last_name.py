import copy
import os
from base64 import b64encode
from datetime import datetime, timedelta
from string import ascii_letters

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

    def test_registration_with_bad_last_name(self):
        """Test register with invalid last_name"""

        url = reverse('register')

        data = copy.deepcopy(self.register_data)
        data['last_name'] = ascii_letters

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data.get('last_name')[0].code, 'max_length')

        data = copy.deepcopy(self.register_data)
        data['last_name'] = 'Harris1'

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data.get('last_name')[0].code, 'last_name_contains_digits'
        )
