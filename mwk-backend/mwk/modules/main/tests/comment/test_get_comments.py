from django.contrib.auth.models import User
from django.urls import reverse
from knox.models import AuthToken
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase

from mwk.modules.main.models.comment import Comment
from mwk.modules.main.models.post import Post
from mwk.modules.main.serializers.comment import CommentSerializer
from mwk.modules.main.services.get_comments_for_post import get_comments_for_post


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

    def authenticate(self, token: str) -> None:
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def create_comments(self, page_size: int) -> None:
        """Fill the Comments model"""

        comment_objects = (
            Comment(
                post=self.post,
                author=self.user,
                body='lorem ipsum',
                lft=0,
                rght=0,
                tree_id=0,
                level=0,
            )
            for _ in range(page_size)
        )

        Comment.objects.bulk_create(comment_objects)

    def get_all_comments(self, page_size: int = api_settings.PAGE_SIZE):
        """Create comments and return ready queryset"""

        self.create_comments(page_size)

        return get_comments_for_post(self.user, self.post.id)

    def test_get_comments(self):
        """Test getting comments"""

        url = reverse('post_comments', kwargs={'pk': self.post.id})

        comments = self.get_all_comments()

        self.authenticate(self.token)
        response = self.client.get(url)

        serializer = CommentSerializer(
            instance=comments,
            many=True,
            context={'request': response.wsgi_request}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('results'), serializer.data)
