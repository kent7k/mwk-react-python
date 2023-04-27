from knox.models import AuthToken


class CustomAuthToken(AuthToken):
    """AuthToken proxy model"""

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
        proxy = True
