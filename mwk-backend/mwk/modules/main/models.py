from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from mwk.modules.authentication.models import Profile

from .helpers.helpers import PathAndRenameDate


class Image(models.Model):
    """
    Model representing an image used for the Post and Comment models.
    """

    post = models.ForeignKey(
        'Post',
        related_name='images',
        related_query_name='images',
        on_delete=models.CASCADE,
        verbose_name='Post',
        null=True,
        blank=True,
    )
    comment = models.ForeignKey(
        'Comment',
        related_name='images_comment',
        related_query_name='images_comment',
        on_delete=models.CASCADE,
        verbose_name='Comment',
        null=True,
        blank=True,
    )
    photo = models.ImageField(
        verbose_name='Photo', upload_to=PathAndRenameDate('photos/posts/')
    )
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')

    def __str__(self) -> str:
        return self.photo.name.split('/')[-1]

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'
        ordering = ('created_at',)


class PostCategory(models.Model):
    """
    Model representing the category of a post.
    """

    title = models.CharField(max_length=50, verbose_name='Category Title')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Post Category'
        verbose_name_plural = 'Post Categories'
        ordering = ('title', '-created_at')


class Post(models.Model):
    """
    Model representing a post.
    """

    profile = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.CASCADE,
        related_name='posts',
        related_query_name='posts',
        verbose_name='Profile',
    )
    title = models.CharField(max_length=150, verbose_name='Post title', blank=True)
    content = models.TextField(verbose_name='Post content', blank=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Created', db_index=True
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    viewers = models.ManyToManyField(
        User,
        related_name='viewed_posts',
        related_query_name='viewed_posts',
        verbose_name='Viewers',
        blank=True,
    )
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE)
    category = models.ForeignKey(
        PostCategory,
        verbose_name='Category',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='posts',
        related_query_name='posts',
    )
    liked = models.ManyToManyField(
        User,
        verbose_name='Liked by',
        related_name='liked_posts',
        related_query_name='liked_posts',
        blank=True,
    )

    def __str__(self) -> str:
        return self.title or self.content[:10] or 'Post'

    def get_absolute_url(self) -> str:
        return reverse('post', kwargs={'pk': self.pk})

    def add_views(self, user: User) -> None:
        """
        Add a view to the post, or do nothing if there is already a view.
        """

        self.viewers.add(user)

    def like(self, user: User) -> bool:
        """
        Like or dislike the post and return True if it was liked, False otherwise.
        """

        is_like = self.liked.filter(id=user.id).exists()

        if is_like:
            self.liked.remove(user)
            return False

        self.liked.add(user)
        return True

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-created_at',)


class Comment(MPTTModel):
    """
    MPTT-Model representing a comment.
    """

    post = models.ForeignKey(
        Post,
        related_name='comments',
        related_query_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Post',
    )
    author = models.ForeignKey(
        User,
        related_name='comments_author',
        related_query_name='comments_author',
        on_delete=models.CASCADE,
        verbose_name='Author',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Last updated at')
    body = models.TextField(verbose_name='Text')
    liked = models.ManyToManyField(
        User,
        verbose_name='Liked by',
        related_name='liked_comments',
        related_query_name='liked_comments',
        blank=True,
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='replies',
        verbose_name='Parent comment',
    )

    def __str__(self) -> str:
        return f'Comment {self.pk}'

    @property
    def replies_cnt(self) -> int:
        """
        Count the number of comment replies.
        """

        return self.get_descendant_count()

    def like(self, user: User) -> bool:
        """
        Like or dislike the comment and return True if it was liked, False otherwise.
        """

        is_like = self.liked.filter(id=user.id).exists()

        if is_like:
            self.liked.remove(user)
            return False

        self.liked.add(user)
        return True

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'Comments'
        ordering = ('-created_at',)

    class MPTTMeta:
        order_insertion_by = ['-created_at']
