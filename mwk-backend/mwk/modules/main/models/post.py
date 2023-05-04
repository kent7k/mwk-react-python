from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from mwk.modules.authentication.models.profile import Profile
from mwk.modules.main.models.post_category import PostCategory


class Post(models.Model):
    """The model representing the post"""

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
        """Adds a view to the post, or if there is already a view, does nothing"""

        self.viewers.add(user)

    def like(self, user: User) -> bool:
        """Like/dislike post, returns True if like false otherwise"""

        is_liked = self.liked.filter(id=user.id).exists()

        if is_liked:
            self.liked.remove(user)
            return False

        self.liked.add(user)
        return True

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ('-created_at',)

