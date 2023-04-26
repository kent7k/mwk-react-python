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

        profiles = [user.profile for user in users]

        for profile in profiles:
            profile.birthday = self.birthday
            profile.save()

        return profiles

    def test_get_profiles(self):
        url = reverse('profiles')
        self.authenticate(self.token)

        self.create_profiles()
        profiles = Profile.objects.all()

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        serializer = ProfileSerializer(instance=profiles, many=True)
        self.assertEqual(response.data.get('results'), serializer.data)

    def test_get_profiles_not_authorized(self):
        """Test getting profiles not authorized"""

        url = reverse('profiles')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)
