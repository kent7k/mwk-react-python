from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiAuthenticationExtension


class KnoxTokenScheme(OpenApiAuthenticationExtension):
    target_class = 'knox.auth.TokenAuthentication'
    name = 'knoxTokenAuth'

    @staticmethod
    def get_security_definition(auto_schema: "AutoSchema") -> dict[str, str]:
        return {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': _('Token-based authentication with required prefix "Token"'),
        }
