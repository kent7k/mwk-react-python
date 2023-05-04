from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AuthenticationToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp: int) -> six.text_type:
        return (
            str(user.pk) +
            str(timestamp) +
            str(user.is_active)
        )
