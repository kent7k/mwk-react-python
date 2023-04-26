from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from knox.models import AuthToken
from rest_framework.test import APITestCase


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

    def test_get_me_not_authorized(self):
        """Test getting self profile unauthorized"""

        url = reverse('profile_details')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)
