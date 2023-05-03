from django.db import models

from mwk.modules.authentication.models.profile import Profile


class Contact(models.Model):
    user_to = models.ForeignKey(
        Profile, related_name='to_set',
        on_delete=models.CASCADE,
        verbose_name='На'
    )
    user_from = models.ForeignKey(
        Profile,
        related_name='from_set',
        on_delete=models.CASCADE,
        verbose_name='From'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Created at'
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
