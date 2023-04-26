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

    def authenticate(self, token: str) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def login(self):
        url = reverse('login')
        data = self.login_data
        response = self.client.post(url, data)

        return response

    def test_registration_without_data(self):
        """A test that tries to register without data"""

        url = reverse('reg')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_login_without_data(self):
        """A test that tries to login without data"""

        url = reverse('login')
        data = {}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)

    def test_login_with_bad_credentials(self):
        """A test that tries to login with bad credentials"""

        url = reverse('login')
        data = {
            'username': self.username,
            'password': 'bla123321fthaapqkd111',
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data.get('non_field_errors')[0].code, 'authorization')

    def test_login_with_inactive_account(self):
        """A test that tries to login with inactive account"""
        inactive_user: User = User.objects.create_user(
            'Authentication_test_case_Inactive', self.email, self.password
        )
        inactive_user.is_active = False
        inactive_user.save()

        url = reverse('login')
        data = {
            'username': inactive_user.username,
            'password': self.password,
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data.get('non_field_errors')[0].code, 'authorization')

    def test_registration_without_first_and_last_name(self):
        """A test that tries to register without first and last names"""

        url = reverse('reg')
        data = copy.deepcopy(self.register_data)
        data.pop('first_name')
        data.pop('last_name')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data.get('first_name')[0].code, 'required')
        self.assertEqual(response.data.get('last_name')[0].code, 'required')

    def test_registration_without_profile(self):
        """A test that tries to register without first and last names"""

        url = reverse('reg')
        data = copy.deepcopy(self.register_data)
        data.pop('profile')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data.get('profile')[0].code, 'required')

    def test_registration_without_birthday(self):
        """A test that tries to register without birthday"""

        url = reverse('reg')
        data = copy.deepcopy(self.register_data)
        data['profile'].pop('birthday')

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)

        profile = response.data.get('profile')

        self.assertEqual(len(profile), 1)
        self.assertEqual(profile.get('birthday')[0].code, 'required')

    def test_registration_with_bad_password(self):
        """A test that tries to register with bad password"""

        url = reverse('reg')
        data = copy.deepcopy(self.register_data)
        data['password'] = 'asd1233'

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data.get('password')[0].code, 'password_too_short')

        data = copy.deepcopy(self.register_data)
        data['password'] = 'qwerty1234'

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data.get('password')[0].code, 'password_too_common')

    def test_registration_with_bad_email(self):
        """A test that tries to register with bad email"""

        url = reverse('reg')
        data = copy.deepcopy(self.register_data)
        data['email'] = 'blablalb'

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data.get('email')[0].code, 'invalid')

    def test_registration_with_bad_username(self):
        """A test that tries to register with bad username"""

        url = reverse('reg')
        data = copy.deepcopy(self.register_data)
        data['username'] = 'A*()!!371'

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data.get('username')[0].code, 'invalid')

        data = copy.deepcopy(self.register_data)
        data['username'] = 'Abo'

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data.get('username')[0].code, 'min_length')

        data = copy.deepcopy(self.register_data)
        data['username'] = ascii_letters

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data.get('username')[0].code, 'max_length')

        data = copy.deepcopy(self.register_data)
        data['username'] = 1111

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data.get('username')[0].code, 'username_contains_only_digits'
        )

    def test_registration_with_existing_username(self):
        """A test that tries to register with already existing username"""

        url = reverse('reg')
        data = copy.deepcopy(self.register_data)
        data['username'] = self.user.username

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data.get('username')[0].code, 'unique')

    def test_registration_with_bad_first_name(self):
        """Test register with bad first_name"""

        url = reverse('reg')
        data = copy.deepcopy(self.register_data)
        data['first_name'] = ascii_letters

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)

        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data.get('first_name')[0].code, 'max_length')

        data = copy.deepcopy(self.register_data)
        data['first_name'] = 'Jane1'

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data.get('first_name')[0].code, 'first_name_contains_digits'
        )

    def test_registration_with_bad_last_name(self):
        """Test register with invalid last_name"""

        url = reverse('reg')

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

    def test_registration_with_bad_avatar(self):
        """Test register with invalid avatar"""

        url = reverse('reg')

        data = copy.deepcopy(self.register_data)
        data['profile']['avatar'] = self.fake_avatar

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)

        profile = response.data.get('profile')
        self.assertEqual(len(profile), 1)

        self.assertEqual(profile.get('avatar')[0].code, 'invalid')

        data = copy.deepcopy(self.register_data)
        data['profile']['avatar'] = 'blabla'

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)

        profile = response.data.get('profile')
        self.assertEqual(len(profile), 1)

        self.assertEqual(profile.get('avatar')[0].code, 'invalid')

    def test_registration_with_bad_birthday(self):
        """Test register with invalid birthday"""

        url = reverse('reg')

        data = copy.deepcopy(self.register_data)
        data['profile']['birthday'] = 'alajhdeu'
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)

        profile = response.data.get('profile')
        self.assertEqual(len(profile), 1)

        self.assertEqual(profile.get('birthday')[0].code, 'invalid')

        data = copy.deepcopy(self.register_data)
        data['profile']['birthday'] = datetime.now()
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)

        profile = response.data.get('profile')
        self.assertEqual(len(profile), 1)

        self.assertEqual(profile.get('birthday')[0].code, 'invalid')

    def test_registration_with_age_less_than_fourteen(self):
        """Test register with age less than fourteen"""

        url = reverse('reg')

        data = copy.deepcopy(self.register_data)
        data['profile']['birthday'] = (
            (datetime.today() - timedelta(days=(365 * 10))).date().strftime('%Y-%m-%d')
        )
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)

        profile = response.data.get('profile')
        self.assertEqual(len(profile), 1)

        self.assertEqual(profile.get('birthday')[0].code, 'age_less_than_fourteen')

    def test_registration_with_age_more_than_onehundred_forty(self):
        """Test register with age more than one hundred forty"""

        url = reverse('reg')

        data = copy.deepcopy(self.register_data)
        data['profile']['birthday'] = (
            (datetime.today() - timedelta(days=(365 * 142))).date().strftime('%Y-%m-%d')
        )
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(len(response.data), 1)

        profile = response.data.get('profile')
        self.assertEqual(len(profile), 1)

        self.assertEqual(
            profile.get('birthday')[0].code, 'age_more_than_onehundred_forty'
        )
