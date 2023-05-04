from django.contrib.auth.models import User
from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase

from mwk.modules.main.models.comment import Comment
from mwk.modules.main.models.post import Post


class LikeTestCase(APITestCase):
    """Test case for liking and unliking a comment"""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username='CommentLikeTestCaseUser',
            email='commentliketestcase@gmail.com',
            password='asd123321',
        )

        self.post = Post.objects.create(
            title='My Awesome Post',
            content='Lorem ipsum dolor sit amet',
            author=self.user,
            profile=self.user.profile,
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.user,
            body='Lorem ipsum dolor sit amet',
        )
        self.token = AuthToken.objects.create(user=self.user)[-1]
        self.authenticate()

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_bad_data_comment_like(self):
        """Test that like comment endpoint returns errors for bad data"""

        url = reverse('like_post_comment')
        data = {'Comment': 245}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        data = {'comment_id': self.comment.id}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {'Comment': []}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
