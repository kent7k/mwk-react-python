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

    def test_get_profiles(self):
        """Test getting profiles"""

        url = reverse('profiles')
        self.authenticate(self.token)

        self.create_profiles()
        profiles = Profile.objects.all()

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        serializer_data = ProfileSerializer(instance=profiles, many=True).data

        self.assertEqual(response.data.get('results'), serializer_data)
