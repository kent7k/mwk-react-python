from django.contrib.auth.models import User
from django.db import models

from mwk.modules.main.helpers.helpers import PathAndRenameDate


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
