from django.contrib.auth.models import User
from django.urls import reverse
from knox.models import AuthToken
from rest_framework.test import APITestCase

from mwk.modules.main.models import Comment, Post, PostCategory


class CommentsTestCase(APITestCase):
    """Comments test"""

    def setUp(self) -> None:
        self.email = 'commentstestcase@gmail.com'
        self.password = 'asd123321'

        self.user = User.objects.create_user(
            'CommentsTestCase', self.email, self.password
        )
        self.token: str = AuthToken.objects.create(self.user)[-1]

        self.post = Post(
            profile=self.user.profile,
            title='Post 1',
            content='lorem ipsum',
            author=self.user,
        )

        self.post.save()

    def test_get_comments_not_authorized(self):
        """Test getting comments not authorized"""

        url = reverse('post_comments', kwargs={'pk': self.post.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)
