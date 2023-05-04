from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse

from mwk.modules.main.helpers.helpers import PathWithDateAndUUID


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        related_query_name='profile',
        verbose_name='User',
    )

    bio = models.CharField(
        max_length=100,
        verbose_name='Status',
        blank=True
    )

    birthday = models.DateField(
        verbose_name='Birthday',
        null=True
    )

    avatar = models.ImageField(
        verbose_name='Avatar',
        blank=True,
        null=True,
        upload_to=PathWithDateAndUUID('photos/avatars/'),
    )

    followers = models.ManyToManyField(
        'self',
        through='Contact',
        related_name='following',
        symmetrical=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Created'
    )

    def __str__(self) -> str:
        return self.user.username

    def get_absolute_url(self) -> str:
        return reverse('profile', kwargs={'pk': self.pk})

    def follow(self, to_profile: 'Profile') -> bool:
        """
        Follow or unfollow a profile. Returns True if followed, False otherwise.
        """
        is_following = self.following.filter(id=to_profile.id).exists()

        if is_following:
            self.following.remove(to_profile)
        else:
            self.following.add(to_profile)

        return not is_following

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['-created_at']


@receiver(post_save, sender=User)
def create_user_profile(sender: User, instance: User, created: bool, **kwargs):
    if created:
        Profile.objects.create(user=instance)
