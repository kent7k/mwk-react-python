from django.db import models

from mwk.modules.authentication.models.profile import Profile


class Contact(models.Model):
    user_to = models.ForeignKey(
        Profile, related_name='to_set',
        on_delete=models.CASCADE,
        verbose_name='To'
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

    def __str__(self):
        return f'{self.user_from} Subscribed to {self.user_to}'

    class Meta:
        ordering = ('-created_at',)
        verbose_name_plural = verbose_name = 'Subscription'
        constraints = [
            models.CheckConstraint(
                check=~models.Q(user_from=models.F('user_to')), name='check_self_follow',
            )
        ]
