from datetime import timedelta

from django.contrib.auth.models import User
from django.db.models import Count, Exists, OuterRef
from django.urls import reverse
from django.utils import timezone
from knox.models import AuthToken
from rest_framework.settings import api_settings
from rest_framework.test import APITestCase

from .models import Comment, Post, PostCategory
from .serializers import CommentSerializer, PostCategorySerializer, PostSerializer
from .services import get_post_comments
from .services import get_posts as get_posts_queryset


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

    def test_get_posts_not_authorized(self):
        """Test getting posts not authorized"""

        url = reverse('feed')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_put_posts(self):
        """Test PUT request to posts raises 405 HTTP error"""

        url = reverse('feed')
        self.get_posts()

        self.authenticate(self.token)
        response = self.client.put(url)

        self.assertEqual(response.status_code, 405)

    def test_get_posts(self):
        """Test getting posts"""

        url = reverse('feed')
        posts = self.get_posts()

        self.authenticate(self.token)
        response = self.client.get(url)

        serializer_data = PostSerializer(
            instance=posts, many=True, context={'request': response.wsgi_request}
        ).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('results'), serializer_data)

    def test_get_categories(self):
        """Test getting post categories"""

        url = reverse('post_categories')
        categories = PostCategory.objects.all()

        self.authenticate(self.token)
        response = self.client.get(url)

        serializer_data = PostCategorySerializer(instance=categories, many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serializer_data)

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

    def test_put_post(self):
        """Test PUT request to post raises 405 HTTP error"""

        post = self.get_posts(3).last()

        url = reverse('post', kwargs={'pk': post.id})

        self.authenticate(self.token)
        response = self.client.put(url)

        self.assertEqual(response.status_code, 405)

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

        comments = Comment.objects.bulk_create(comment_objects)

        return comments

    def get_comments(self, page_size: int = api_settings.PAGE_SIZE):
        """Create comments and return ready queryset"""

        self.create_comments(page_size)

        return get_post_comments(self.user, self.post.id)

    def test_get_comments_not_authorized(self):
        """Test getting comments not authorized"""

        url = reverse('post_comments', kwargs={'pk': self.post.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 401)

    def test_get_comments(self):
        """Test getting comments"""

        url = reverse('post_comments', kwargs={'pk': self.post.id})

        comments = self.get_comments()

        self.authenticate(self.token)
        response = self.client.get(url)

        serializer_data = CommentSerializer(
            instance=comments, many=True, context={'request': response.wsgi_request}
        ).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get('results'), serializer_data)

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
        """A test to check GET request on the post like return HTTP 405"""

        url = reverse('like')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 405)

    def test_get_comment_like(self):
        """A test to check GET request on the comment like return HTTP 405"""

        url = reverse('like_comment')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 405)

    def test_post_like(self):
        """A test to check likes and remove likes on a post"""

        url = reverse('like')
        data = {'post': self.post.id}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'add'})
        self.assertTrue(self.post.liked.filter(id=self.user.id).exists())

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'remove'})
        self.assertFalse(self.post.liked.filter(id=self.user.id).exists())

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'add'})

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'remove'})

    def test_comment_like(self):
        """A test to check likes and remove likes on a comment"""
        url = reverse('like_comment')
        data = {'comment': self.comment.id}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'add'})
        self.assertTrue(self.comment.liked.filter(id=self.user.id).exists())

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'remove'})
        self.assertFalse(self.comment.liked.filter(id=self.user.id).exists())

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'add'})

        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'action': 'remove'})

    def test_without_data_post_like(self):
        """Test to check the post like without data"""
        url = reverse('like')
        data = {}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 400)

    def test_without_data_comment_like(self):
        """Test to check the comment like without data"""
        url = reverse('like_comment')
        data = {}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 400)

    def test_bad_data_post_like(self):
        """Test to check the post like with bad data"""
        url = reverse('like')
        data = {'post': 245}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 404)

        data = {'post_id': self.post.id}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 400)

        data = {'post': []}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 400)

    def test_bad_data_comment_like(self):
        """Test to check the comment like with bad data"""
        url = reverse('like_comment')
        data = {'comment': 245}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 404)

        data = {'comment_id': self.comment.id}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 400)

        data = {'comment': []}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 400)

    def test_unauthorized_post_like(self):
        """A test to check unauthorized user can't likes and remove likes on a post"""

        self.client.credentials()
        url = reverse('like')
        data = {'post_id': self.post.id}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 401)

    def test_unauthorized_comment_like(self):
        """A test to check unauthorized user can't likes and remove likes on a comment"""

        self.client.credentials()
        url = reverse('like_comment')
        data = {'comment_id': self.comment.id}
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, 401)
