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

    def activate_user(self, token: str, uid: str) -> Response:
        """Activate the user and return response"""

        url = reverse('activate', kwargs={'uid': uid, 'token': token})
        response = self.client.get(url)

        return response

    def test_activate_user(self):
        """A test that tries activate non-active user"""

        inactive_user: User = User.objects.create_user(
            'AuthenticationTestCase_User_needs_activate',
            'v1234@gmail.com',
            self.password,
        )
        inactive_user.is_active = False
        inactive_user.save()

        token = AuthenticationToken().make_token(inactive_user)
        uid = encode_uid(inactive_user.pk)

        response = self.activate_user(token, uid)

        self.assertEqual(response.status_code, 204)
        response = self.activate_user(token, uid)
        self.assertEqual(response.status_code, 400)

    def test_activate_user_authorized(self):
        """A test that tries activate non-active user authorized"""

        inactive_user: User = User.objects.create_user(
            'AuthenticationTestCase_User_needs_activate_authorized',
            'v1234@gmail.com',
            self.password,
        )
        inactive_user.is_active = False
        inactive_user.save()

        token = AuthenticationToken().make_token(inactive_user)
        uid = encode_uid(inactive_user.pk)

        self.authenticate(self.token)
        response = self.activate_user(token, uid)

        self.assertEqual(response.status_code, 403)
