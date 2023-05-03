from typing import Type

from rest_framework import generics
from rest_framework.serializers import Serializer

from rest_framework.permissions import AllowAny
from mwk.modules.authentication.serializers.user_create_with_profile import UserCreateWithProfileSerializer


class UserRegisterAPIView(generics.CreateAPIView):
    """Endpoint for user registration (create account)"""

    serializer_class = UserCreateWithProfileSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer: Type[Serializer]) -> None:
        user = serializer.save()
