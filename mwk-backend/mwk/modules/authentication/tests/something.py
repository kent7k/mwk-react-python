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
    """Test registration and login"""

    def setUp(self):
        self.email = 'authentication-test-case-user@gmail.com'
        self.email_register = 'authentication-test-case@gmail.com'
        self.username = 'authentication-test'
        self.first_name = 'John'
        self.last_name = 'Doe'
        self.password = 'asd123321'
        self.media_path = os.path.join(settings.TESTS_MEDIA_ROOT, 'authentication')

        with open(os.path.join(self.media_path, 'avatar.png'), 'rb') as file:
            self.avatar = b64encode(file.read())

        self.user = User.objects.create_user(
            'authentication-test-user', self.email, self.password
        )
        self.token = AuthToken.objects.create(user=self.user)[-1]

        self.register_data = {
            'email': self.email_register,
            'username': self.username,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'profile': {
                'birthday': self._get_birthday(10),
                'avatar': self.avatar,
            },
        }

        self.login_data = {'username': self.user.username, 'password': self.password}

    def _get_birthday(self, years):
        """Return a birthday 'years' years ago from today"""
        return (datetime.today() - timedelta(days=(365 * years))).date().strftime('%Y-%m-%d')

    def test_registration_with_age_less_than_fourteen(self):
        """Test registration with age less than fourteen"""

        url = reverse('reg')

        data = copy.deepcopy(self.register_data)
        data['profile']['birthday'] = self._get_birthday(10)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)

        # Check that the error message is correct
        expected_error = {
            'profile': {
                'birthday': [
                    {
                        'code': 'age_less_than_fourteen',
                        'message': 'You must be at least 14 years old to register'
                    }
                ]
            }
        }
        self.assertEqual(response.data, expected_error)
