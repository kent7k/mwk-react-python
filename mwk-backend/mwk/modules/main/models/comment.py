from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mwk.modules.main.models.post import Post


class Comment(MPTTModel):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Post'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments_author',
        verbose_name='Author'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created at'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Last updated at'
    )
    body = models.TextField(verbose_name='Text')
    liked = models.ManyToManyField(
        User,
        blank=True,
        related_name='liked_comments',
        verbose_name='Liked by'
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='replies',
        verbose_name='Parent comment'
    )

    def __str__(self) -> str:
        """Return the string representation of the comment"""
        return f'Comment {self.pk}'

    @property
    def replies_count(self) -> int:
        return self.get_descendant_count()

    def like(self, user: User) -> bool:
        """Like or dislike the comment and return True if it was liked, False otherwise."""
        is_liked = self.liked.filter(id=user.id).exists()

        if is_liked:
            self.liked.remove(user)
            return False

        self.liked.add(user)
        return True

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = verbose_name + 's'
        ordering = ('-created_at',)

    class MPTTMeta:
        order_insertion_by = ['-created_at']
