import os
from base64 import b64encode
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
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

    def authenticate(self, token):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_login_with_bad_credentials_returns_400(self):
        """Verify that logging in with bad credentials returns a 400 error"""
        url = reverse('login')
        data = {
            'username': self.user.username,
            'password': 'bla123321fthaapqkd111',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data['non_field_errors'][0].code, 'authorization')
