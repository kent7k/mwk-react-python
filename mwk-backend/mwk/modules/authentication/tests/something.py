from django.contrib.auth.models import User
from django.urls import reverse
from knox.models import AuthToken
from rest_framework import status
from rest_framework.test import APITestCase

from mwk.modules.main.models import Comment, Post, PostCategory


class CommentLikeTestCase(APITestCase):
    """Test case for liking and unliking a comment"""

    def setUp(self):
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
        self.token = AuthToken.objects.create(user=self.user).token
        self.authenticate()

    def authenticate(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_comment_like(self):
        """Test that liking and unliking a comment works"""
        url = reverse('like_comment')
        data = {'comment': self.comment.id}

        # add like
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'action': 'add'})
        self.assertTrue(self.comment.liked.filter(id=self.user.id).exists())

        # remove like
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'action': 'remove'})
        self.assertFalse(self.comment.liked.filter(id=self.user.id).exists())

        # add like again
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'action': 'add'})

        # remove like again
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'action': 'remove'})
