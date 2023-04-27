from django.contrib.auth.models import User
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from mwk.modules.main.models.post import Post


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
