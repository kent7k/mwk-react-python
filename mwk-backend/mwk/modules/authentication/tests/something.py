from django.contrib.auth.models import User
from django.urls import reverse
from knox.models import AuthToken
from rest_framework.test import APITestCase

from mwk.modules.main.models import Comment, Post, PostCategory


class LikeTestCase(APITestCase):
    """Test-case for testing likes"""

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            'LikeTestCaseUser', 'liketestcase@gmail.com', 'asd123321'
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

    def test_get_post_like(self):
        """Test to check GET request on the post like return HTTP 405"""

        url = reverse('like')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 405)

    def test_get_comment_like(self):
        """Test to check GET request on the comment like return HTTP 405"""

        url = reverse('like_comment')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 405)

    def test_post_like(self):
        """Test to check likes and remove likes on a post"""

        url = reverse('like')
        data = {'post': self.post.id}

        # add like
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'add'})
        self.assertTrue(self.post.liked.filter(id=self.user.id).exists())

        # remove like
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'remove'})
        self.assertFalse(self.post.liked.filter(id=self.user.id).exists())

        # add like again
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'add'})

        # remove like again
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'remove'})

    def test_comment_like(self):
        """Test to check likes and remove likes on a comment"""
        url = reverse('like_comment')
        data = {'comment': self.comment.id}

        # add like
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'add'})
        self.assertTrue(self.comment.liked.filter(id=self.user.id).exists())

        # remove like
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'remove'})
        self.assertFalse(self.comment.liked.filter(id=self.user.id).exists())

        # add like again
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'add'})

        # remove like again
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'remove'})

    def test_without_data_post_like(self):
        """Test to check the post like without data"""
        url = reverse('like')
        data = {}

