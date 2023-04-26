from django.utils.translation import gettext as _
from djoser.serializers import ActivationSerializer as DjoserActivationSerializer


class ActivationSerializer(DjoserActivationSerializer):
    default_error_messages = {
        'stale_token': _('The token has expired.'),
        'invalid_token': _('Invalid or corrupted token.'),
        'invalid_uid': _('Invalid or corrupted UID.')
    }
