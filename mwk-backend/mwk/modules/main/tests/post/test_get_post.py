from datetime import timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from knox.models import AuthToken
from rest_framework.test import APITestCase

from mwk.modules.main.models.post import Post
from mwk.modules.main.serializers.post import PostSerializer
from mwk.modules.main.services.get_all_posts import get_all_posts


class PostsTestCase(APITestCase):
    """Posts test"""

    def setUp(self) -> None:
        self.email = 'poststestcase@gmail.com'
        self.password = 'asd123321'
        self.user = User.objects.create_user('PostsTestCase', self.email, self.password)
        self.token: str = AuthToken.objects.create(self.user)[-1]

    def authenticate(self, token: str) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def create_posts(self, page_size: int) -> None:
        posts = []
        for i in range(page_size):
            post = Post.objects.create(
                profile=self.user.profile,
                title='Post ' + str(i),
                content='lorem ipsum',
                author=self.user,
                created_at=timezone.now() + timedelta(minutes=i),
            )
            posts.append(post)

    def get_posts_queryset(self, page_size):
        self.create_posts(page_size)
        return get_all_posts(self.user)

    def test_get_post(self):
        posts = self.get_posts_queryset(3)
        post = posts.last()
        url = reverse('post', kwargs={'pk': post.id})
        self.authenticate(self.token)
        response = self.client.get(url)
        serializer = PostSerializer(
            post, context={'request': response.wsgi_request}
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer.data)
