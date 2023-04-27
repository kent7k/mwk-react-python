"""Services for the authentication app"""


from datetime import datetime
from smtplib import SMTPException

from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
from django.utils.translation import gettext as _
from djoser.compat import get_user_email
from knox.models import AuthToken
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .email import ActivationEmail
from mwk.modules.authentication.models.profile import Profile


def send_activation_email(request, user: User) -> None:
    """
    Sends an email to activate the account to the user's email
    if the email could not be sent, deletes the user and causes error 500
    """

    context = {'user': user}
    to = [get_user_email(user)]

    try:
        ActivationEmail(request, context).send(to)
    except SMTPException:
        user.delete()
        raise ValidationError(
            detail={
                'email': _(
                    'Failed to send activation email, please try again!'
                )
            },
            code=500,
        )


def activate_user(user: User) -> None:
    """Set user.is_active to True"""

    user.is_active = True
    user.save()


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


def setup_user_profile(attrs: dict, user: User) -> Profile:
    """
    Helper function for the 'register_user' service
    Set attrs to the user.profile if attr not None
    """
    for key in attrs:
        if not attrs.get(key) is None:
            setattr(user.profile, key, attrs.get(key))
    return user.profile


def register_user(user_data: dict, password: str, user_profile_data: dict) -> User:
    """Register user (create user)"""

    user: User = User.objects.create_user(**user_data)
    user.set_password(password)
    user.is_active = False

    profile = setup_user_profile(user_profile_data, user)

    user.save()
    profile.save()

    return user
