from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from mwk.modules.authentication.models.profile import Profile
from mwk.modules.main.models.post_category import PostCategory


class Post(models.Model):
    profile = models.ForeignKey(
        Profile,
        null=True,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Profile',
    )
    title = models.CharField(max_length=150, verbose_name='Post title', blank=True)
    content = models.TextField(verbose_name='Post content', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created', db_index=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    viewers = models.ManyToManyField(get_user_model(), related_name='viewed_posts', blank=True)
    author = models.ForeignKey(get_user_model(), verbose_name='Author', on_delete=models.CASCADE)
    category = models.ForeignKey(PostCategory, verbose_name='Category', on_delete=models.CASCADE, null=True, blank=True, related_name='posts')
    liked = models.ManyToManyField(get_user_model(), verbose_name='Liked by', related_name='liked_posts', blank=True)

    def __str__(self) -> str:
        return self.title or self.content[:10] or 'Post'

    def get_absolute_url(self) -> str:
        return reverse('post', kwargs={'pk': self.pk})

    def add_views(self, user):
        if user not in self.viewers.all():
            self.viewers.add(user)

    def like(self, user):
        if self.liked.filter(id=user.id).exists():
            self.liked.remove(user)
            return False

        self.liked.add(user)
        return True

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = verbose_name + 's'
        ordering = ('-created_at',)

