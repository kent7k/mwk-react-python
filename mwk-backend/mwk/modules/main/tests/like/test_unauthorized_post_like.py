from django.contrib.auth.models import User
from django.urls import reverse
from knox.models import AuthToken
from rest_framework.test import APITestCase
from rest_framework import status

from mwk.modules.main.models.comment import Comment
from mwk.modules.main.models.image import Image
from mwk.modules.main.models.post_category import PostCategory
from mwk.modules.main.models.post import Post


class LikeTestCase(APITestCase):
    """Test-case for testing likes"""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='LikeTestCaseUser',
            email='liketestcase@gmail.com',
            password='asd123321'
        )

        self.post = Post.objects.create(
            title='My Awesome Post',
            content='Lorem ipsum dolor sit amet',
            author=self.user,
            profile=self.user.profile,
        )

        self.comment = Comment.objects.create(
            post=self.post, author=self.user, body='Lorem ipsum dolor sit amet'
        )

        self.token = AuthToken.objects.create(user=self.user)[-1]
        self.authenticate()

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_unauthorized_post_like(self):
        """A test to check unauthorized user can't likes and remove likes on a post"""

        self.client.credentials()
        url = reverse('like')
        data = {'post_id': self.post.id}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
