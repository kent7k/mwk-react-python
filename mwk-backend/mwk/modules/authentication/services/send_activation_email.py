from smtplib import SMTPException

from django.conf import settings
from djoser.utils import encode_uid
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from djoser.compat import get_user_email
from rest_framework.exceptions import ValidationError
from templated_mail.mail import BaseEmailMessage

from mwk.modules.authentication.tokens import AuthenticationToken


class ActivationEmail(BaseEmailMessage):
    template_name = 'authentication/activation.html'

    def get_context_data(self):
        context = super().get_context_data()

        user: User = context.get('user')
        uid = encode_uid(user.id)
        token = AuthenticationToken().make_token(user)

        url = f"{settings.USER_ACTIVATION_URL.format(uid, token)}"

        context['url'] = url
        context['sitename'] = settings.AUTHENTICATION_SITENAME
        return context


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
