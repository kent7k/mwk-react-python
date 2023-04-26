from datetime import timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from knox.models import AuthToken
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase

from mwk.modules.main.models import Comment, Post, PostCategory
from mwk.modules.main.serializers.PostSerializer import PostSerializer
from mwk.modules.main.services import get_posts as get_posts_queryset


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
        """Fill the Post model"""

        post_objects = (
            Post(
                profile=self.user.profile,
                title='Post ' + str(i),
                content='lorem ipsum',
                author=self.user,
            )
            for i in range(page_size)
        )

        posts = Post.objects.bulk_create(post_objects)

        for i, post in enumerate(posts):
            # Because we cannot set the created_at field immediately when creating an object
            post.created_at = timezone.now() + timedelta(minutes=i)
            post.save()

    def get_posts(self, page_size: int = api_settings.PAGE_SIZE):
        """Create posts and return ready queryset"""

        self.create_posts(page_size)

        return get_posts_queryset(self.user)

    def test_get_post(self):
        """Test getting post"""

        post = self.get_posts(3).last()

        url = reverse('post', kwargs={'pk': post.id})

        self.authenticate(self.token)
        response = self.client.get(url)

        serializer_data = PostSerializer(
            instance=post, context={'request': response.wsgi_request}
        ).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer_data)
