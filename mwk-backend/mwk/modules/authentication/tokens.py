from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AuthenticationToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp: int) -> six.text_type:
        return (
            six.text_type(user.pk) +
            six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
