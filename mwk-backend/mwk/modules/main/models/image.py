from django.contrib.auth import get_user_model
from django.db import models
from mwk.modules.main.helpers.helpers import PathWithDateAndUUID
from mwk.modules.main.models.post import Post
from mwk.modules.main.models.comment import Comment


class Image(models.Model):
    post = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE, verbose_name='Post', null=True, blank=True)
    comment = models.ForeignKey(Comment, related_name='images_comment', on_delete=models.CASCADE, verbose_name='Comment', null=True, blank=True)
    photo = models.ImageField(upload_to=PathWithDateAndUUID('photos/posts/'), verbose_name='Photo')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name='Author')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation date')

    def __str__(self):
        return self.photo.name.split('/')[-1]

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = verbose_name + 's'
        ordering = ('created_at',)
