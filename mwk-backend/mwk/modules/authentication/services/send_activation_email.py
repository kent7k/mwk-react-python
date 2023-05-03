from smtplib import SMTPException

from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from djoser.compat import get_user_email
from rest_framework.exceptions import ValidationError

from mwk.modules.authentication.email import ActivationEmail


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
