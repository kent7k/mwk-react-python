import os
from base64 import b64encode
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from knox.models import AuthToken
from rest_framework.test import APITestCase


class AuthenticationTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='AuthenticationTestUser',
            email='authenticationtestcaseuser@gmail.com',
            password='asd123321',
        )
        self.token = AuthToken.objects.create(user=self.user)[-1]
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
            },
        }
        self.login_data = {'username': self.user.username, 'password': 'asd123321'}

    def _get_birthday(self):
        return (datetime.today() - timedelta(days=(365 * 15))).date().strftime('%Y-%m-%d')

    def _encode_file(self, filename):
        with open(os.path.join(self.media_path, filename), 'rb') as file:
            return b64encode(file.read())

    def test_get_register_returns_405(self):
        """Verify that a GET request to register returns a 405 error"""
        url = reverse('register')
        response = self.client.get(url, data=self.register_data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
