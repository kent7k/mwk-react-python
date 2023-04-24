from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from knox.models import AuthToken

from mwk.modules.main.helpers.helpers import PathAndRenameDate


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        related_query_name='profile',
        verbose_name='User',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    bio = models.CharField(max_length=100, verbose_name='Status', blank=True)

    avatar = models.ImageField(
        verbose_name='Avatar',
        blank=True,
        null=True,
        upload_to=PathAndRenameDate('photos/avatars/'),
    )

    followers = models.ManyToManyField(
        'self', through='Contact', related_name='following', symmetrical=False
    )
    birthday = models.DateField(verbose_name='Birthday', null=True)

    def __str__(self) -> str:
        return self.user.username

    def get_absolute_url(self) -> str:
        return reverse('profile', kwargs={'pk': self.pk})

    def follow(self, to_profile: 'Profile') -> bool:
        """Follow/Unfollow to_profile, returns True if follow false otherwise"""

        is_following = self.following.filter(id=to_profile.id).exists()

        if is_following:
            self.following.remove(to_profile)
            return False

        self.following.add(to_profile)
        return True

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['-created_at']


class Contact(models.Model):
    user_to = models.ForeignKey(
        Profile, related_name='to_set', on_delete=models.CASCADE, verbose_name='На'
    )
    user_from = models.ForeignKey(
        Profile, related_name='from_set', on_delete=models.CASCADE, verbose_name='От'
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name='Created at'
    )

    def __str__(self) -> str:
        return '{} Subscribed to {}'.format(self.user_from, self.user_to)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(
                    user_from=models.F('user_to')
                ),  # Prohibits subscribing to yourself
                name='check_self_follow',
            )
        ]


class CustomAuthToken(AuthToken):
    """AuthToken proxy model"""

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        proxy = True


@receiver(post_save, sender=User)
def create_user_profile(sender: User, instance: User, created: bool, **kwargs):
    if created:
        Profile.objects.create(user=instance)
