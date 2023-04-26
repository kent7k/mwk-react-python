from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer


class KnoxTokenSerializer(AuthTokenSerializer):
    expiry = serializers.DateTimeField(read_only=True, label=_('Expiry'))
