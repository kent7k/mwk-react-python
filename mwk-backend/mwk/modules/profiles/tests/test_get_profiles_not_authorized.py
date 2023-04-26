from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from knox.models import AuthToken
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase

from mwk.modules.authentication.models import Profile


class ProfileTests(APITestCase):
    """Profiles test"""

    def setUp(self) -> None:
        self.email = 'profilestestcase@gmail.com'
        self.password = 'asd123321'

        self.user = User.objects.create_user(
            'ProfilesTestCase',
            self.email,
            self.password,
            first_name='John',
            last_name='Pauls',
        )
        self.user.profile.delete()

        self.birthday = (
            (datetime.today() - timedelta(days=(365 * 15))).date().strftime('%Y-%m-%d')
        )

        self.token: str = AuthToken.objects.create(self.user)[-1]

    def authenticate(self, token: str) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def setup_user_profile(self, user: User) -> Profile:
        """Fill in the profile with test data"""

        user.profile.birthday = self.birthday

        user.profile.save()

        return user.profile

    def create_profiles(self) -> list[Profile]:
        """Fill the Profile model"""

        page_size = api_settings.PAGE_SIZE

        profiles = [
            self.setup_user_profile(
                User.objects.create_user(
                    'ProfilesTestCaseGetProfiles' + str(i),
                    'profilestestcasegetprofiles@gmail.com',
                    self.password,
                    first_name='Test' + str(i),
                )
            )
            for i in range(page_size)
        ]

        return profiles

    def test_get_profiles_not_authorized(self):
        """Test getting profiles not authorized"""

        url = reverse('profiles')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)