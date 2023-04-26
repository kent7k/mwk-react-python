import os
from base64 import b64encode
from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse
from knox.models import AuthToken
from rest_framework.test import APITestCase


class AuthenticationTestCase(APITestCase):
    """Registration and login test"""

    @classmethod
    def setUpTestData(cls):
        cls.email = 'authenticationtestcaseuser@gmail.com'
        cls.email_register = 'authenticationtestcase@gmail.com'
        cls.username = 'AuthenticationTest'
        cls.first_name = 'John'
        cls.last_name = 'Doe'
        cls.password = 'asd123321'
        cls.birthday = (date.today() - timedelta(days=(365 * 15))).strftime('%Y-%m-%d')
        cls.media_path = os.path.join(settings.TESTS_MEDIA_ROOT, 'authentication')

        with open(os.path.join(cls.media_path, 'avatar.png'), 'rb') as file:
            cls.avatar = b64encode(file.read())

        with open(os.path.join(cls.media_path, 'alt-avatar.txt'), 'rb') as file:
            cls.fake_avatar = b64encode(file.read())

        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            email=cls.email, username='AuthenticationTestUser', password=cls.password
        )
        cls.token = str(AuthToken.objects.create(user=cls.user))

    def setUp(self):
        self.login_data = {'username': self.user.username, 'password': self.password}
        self.register_data = {
            'email': self.email_register,
            'username': self.username,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'profile': {'birthday': self.birthday, 'avatar': self.avatar},
        }

    def authenticate(self, token):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')

    def test_valid_token(self):
        """Test valid authentication token"""
        response = self.client.post(reverse('login'), self.login_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        token = response.data['token']

        url = reverse('check_token')
        self.authenticate(token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 204)

    def test_invalid_token(self):
        """Test invalid authentication token"""
        self.authenticate('abracadabra')
        response = self.client.get(reverse('check_token'))
        self.assertEqual(response.status_code, 401)
