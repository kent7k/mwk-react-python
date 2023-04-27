from typing import Type

from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from mwk.modules.authentication.permissions import Authenticated
from mwk.modules.authentication.serializers.activation import ActivationSerializer
from mwk.modules.authentication.services import activate_user, create_authtoken, send_activation_email
from mwk.modules.authentication.tokens import AuthenticationToken


class UserActivateAPIView(generics.GenericAPIView):
    """Endpoint for user activation (set user field is_active to True)"""

    serializer_class = ActivationSerializer
    token_generator = AuthenticationToken()  # used in ActivationSerializer
    permission_classes = (Authenticated,)

    def get(self, request, uid: str, token: str) -> Response:
        serializer: Type[Serializer] = self.get_serializer(
            data={'uid': uid, 'token': token}
        )
        serializer.is_valid(raise_exception=True)

        user: User = serializer.user
        activate_user(user)

        return Response(status=204)
