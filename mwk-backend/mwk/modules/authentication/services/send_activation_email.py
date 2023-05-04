from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from djoser.utils import encode_uid
from rest_framework.exceptions import ValidationError

from mwk.modules.authentication.tokens import AuthenticationToken


def send_activation_email(request, user: User) -> None:
    uid = encode_uid(user.id)
    token = AuthenticationToken().make_token(user)

    url = f"{settings.USER_ACTIVATION_URL.format(uid, token)}"
    subject = _("Activate your account")
    message = _(f"Activate your account by clicking on this link: {url}")
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list)
    except Exception:
        user.delete()
        raise ValidationError(
            detail={
                'email': _('Failed to send activation email, please try again!')
            },
            code=500,
        )
