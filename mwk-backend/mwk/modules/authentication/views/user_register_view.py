from typing import Type

from rest_framework import generics
from rest_framework.serializers import Serializer

from mwk.modules.authentication.permissions import Authenticated
from mwk.modules.authentication.serializers.user_create_with_profile import UserCreateWithProfileSerializer
from mwk.modules.authentication.services import activate_user, create_authtoken, send_activation_email


class UserRegisterAPIView(generics.CreateAPIView):
    """Endpoint for user registration (create account)"""

    serializer_class = UserCreateWithProfileSerializer
    permission_classes = (Authenticated,)

    def perform_create(self, serializer: Type[Serializer]) -> None:
        user = serializer.save()
        send_activation_email(self.request, user)
