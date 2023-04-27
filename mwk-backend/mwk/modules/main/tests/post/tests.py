from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models import Count, Exists, OuterRef
from django.utils import timezone
from knox.models import AuthToken
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase

from mwk.modules.main.models.comment import Comment
from mwk.modules.main.models.image import Image
from mwk.modules.main.models.post_category import PostCategory
from mwk.modules.main.models.post import Post
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

    def get_filtered_by_category_posts(
        self, category: PostCategory, posts: list[Post], category_posts_limit: int = 2
    ):
        """Get filtered by category posts"""

        for post in posts[0:category_posts_limit]:
            post.category = category
            post.save()

        posts = posts.filter(category=category)

        return posts

    def get_filtered_by_popular_posts(self, user: User, posts: list[Post]):
        """Get filtered by popular posts"""

        posts[1].like(user)

        posts = posts.annotate(liked_cnt=Count('liked')).order_by(
            '-liked_cnt', '-created_at'
        )

        return posts

    def get_filtered_by_interesting_posts(self, user: User, posts: list[Post]):
        """Get filtered by interesting posts"""

        post = posts[1]

        post.author = user
        post.save()

        following = self.user.profile.following
        posts = posts.annotate(
            flag=Exists(following.filter(id=OuterRef('author__profile__id')))
        ).order_by('-flag', '-created_at')

        return posts

    def get_filtered_by_popular_and_ordering_posts(
        self, ordering: str, user: User, posts: list[Post]
    ):
        """Get filtered by popular posts with ORDER_BY=ordering"""

        posts[2].like(user)
        posts[1].like(user)

        posts = posts.annotate(liked_cnt=Count('liked')).order_by(
            '-liked_cnt', ordering
        )

        return posts

    def get_filtered_by_interesting_and_ordering_posts(
        self, ordering: str, user: User, posts: list[Post]
    ):
        """Get filtered by interesting posts with ORDER_BY=ordering"""

        post = posts[1]
        post_two = posts[2]

        post.author = user
        post.save()

        post_two.author = user
        post_two.save()

        following = self.user.profile.following
        posts = posts.annotate(
            flag=Exists(following.filter(id=OuterRef('author__profile__id')))
        ).order_by('-flag', ordering)

        return posts

    def get_filtered_by_category_and_ordering_posts(
        self, ordering: str, category: PostCategory
    ):
        """Get filtered by category posts with ORDER_BY=ordering"""

        posts = self.get_posts()

        post = posts[1]
        post_two = posts[2]

        post.category = category
        post.save()

        post_two.category = category
        post_two.save()

        posts = posts.filter(category=category).order_by(ordering)

        return posts
