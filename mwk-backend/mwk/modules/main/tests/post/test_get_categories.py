from django.contrib.auth.models import User
from django.urls import reverse
from knox.models import AuthToken
from rest_framework.test import APITestCase

from mwk.modules.main.models import Comment, Post, PostCategory
from mwk.modules.main.serializers.post_category import PostCategorySerializer


class PostsTestCase(APITestCase):
    """Posts test"""

    def setUp(self) -> None:
        self.email = 'poststestcase@gmail.com'
        self.password = 'asd123321'

        self.user = User.objects.create_user('PostsTestCase', self.email, self.password)
        self.token: str = AuthToken.objects.create(self.user)[-1]

    def authenticate(self, token: str) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_get_categories(self):
        url = reverse('post_categories')
        self.authenticate(self.token)
        response = self.client.get(url)
        serializer = PostCategorySerializer(PostCategory.objects.all(), many=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
