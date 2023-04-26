from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from knox.models import AuthToken
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase

from mwk.modules.authentication.models import Profile
from mwk.modules.profiles.serializers.profile import ProfileSerializer


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

        self.birthday = datetime.today() - timedelta(days=365 * 15)

        self.token = AuthToken.objects.create(self.user)[-1]

    def authenticate(self, token: str) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def create_profiles(self, page_size=None) -> list[Profile]:
        """Create and return list of profiles"""

        page_size = page_size or api_settings.PAGE_SIZE

        users = map(
            lambda i: User.objects.create_user(
                username=f"ProfilesTestCaseGetProfiles{i}",
                email=f"profilestestcasegetprofiles{i}@gmail.com",
                password=self.password,
                first_name=f"Test{i}",
            ),
            range(page_size)
        )

        profiles = Profile.objects.bulk_create(
            [Profile(user=user, birthday=self.birthday) for user in users]
        )

        return profiles

    def test_get_profiles(self)from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase

from mwk.modules.authentication.models import Profile
from mwk.modules.profiles.serializers.profile import ProfileSerializer


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
        self.token: str = AuthToken.objects.create(self.user)[-1]
        self.birthday = (
            (datetime.today() - timedelta(days=(365 * 15))).date().strftime('%Y-%m-%d')
        )
        self.setup_user_profile(self.user)

    def authenticate(self, token: str) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def setup_user_profile(self, user: User) -> Profile:
        """Fill in the profile with test data"""
        return Profile.objects.create(user=user, birthday=self.birthday)

    def create_profiles(self) -> list[Profile]:
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

    def test_get_profiles(self):
        url = reverse('profiles')
        self.authenticate(self.token)
        profiles = self.create_profiles()
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = ProfileSerializer(instance=profiles, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_get_me(self):
        """Test getting self profile"""
        url = reverse('profile_details')
        self.authenticate(self.token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_OK)
        serializer = Profile
:
        url = reverse('profiles')
        self.authenticate(self.token)

        self.create_profiles()
        profiles = Profile.objects.all()

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        serializer = ProfileSerializer(instance=profiles, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)
