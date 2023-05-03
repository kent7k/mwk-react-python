from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from django.utils.translation import gettext as _
from knox.models import AuthToken
from rest_framework.exceptions import PermissionDenied


def create_auth_token(request, user: User, token_limit_per_user: int = None, token_ttl: int = None):
    if token_limit_per_user is not None:
        now = timezone.now()
        token = user.auth_token_set.filter(expiry__gt=now)
        if token.count() >= token_limit_per_user:
            raise PermissionDenied(_('The maximum number of tokens per user has been reached.'))

    instance, token = AuthToken.objects.create(user, token_ttl)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return request, token, instance
