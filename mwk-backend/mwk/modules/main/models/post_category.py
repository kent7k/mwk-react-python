from django.db import models


class PostCategory(models.Model):
    title = models.CharField(max_length=50, verbose_name='Category Title')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created at')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Post Category'
        verbose_name_plural = verbose_name + 'es'
        ordering = ('title', '-created_at')
