from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from django.utils.translation import gettext as _
from knox.models import AuthToken
from rest_framework.response import Response


def create_authtoken(
    request, user: User, token_limit_per_user: int, token_ttl: datetime
) -> Response:
    """
    Creates an Auth Token for the specified user, if the token limit is exceeded, raises a 403 HTTP error
    """

    if token_limit_per_user is not None:
        now = timezone.now()
        token = user.auth_token_set.filter(expiry__gt=now)
        if token.count() >= token_limit_per_user:
            return Response(
                {'error': _('The maximum number of tokens per user has been reached.')},
                status=403,
            )

    instance, token = AuthToken.objects.create(user, token_ttl)
    user_logged_in.send(sender=user.__class__, request=request, user=user)
    return request, token, instance
