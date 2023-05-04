import copy
import os
from base64 import b64encode
from datetime import datetime, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from knox.models import AuthToken
from rest_framework.test import APITestCase

from mwk.modules.authentication.models.profile import Profile


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

    def test_registration_with_no_avatar(self):
        """
        A test that verifies that registering without specifying an avatar will
        give the user a default avatar
        """

        url = reverse('register')
        data = copy.deepcopy(self.register_data)
        data['profile']['avatar'] = None

        response = self.client.post(url, data, format='json')
        register_response_data = response.data
        self.assertEqual(response.status_code, 201)

        users = User.objects.filter(username=register_response_data.get('username'))
        self.assertTrue(users.exists())

        user: User = users.first()

        self.assertTrue(Profile.objects.filter(user=user).exists())
        self.assertFalse(user.is_active)

        self.assertEqual(
            register_response_data,
            {
                'username': data.get('username'),
                'first_name': data.get('first_name'),
                'last_name': data.get('last_name'),
                'is_active': False,
                'profile': {
                    'avatar': None,
                    'birthday': data.get('profile').get('birthday'),
                },
            },
        )

        user.delete()  # clearing user
