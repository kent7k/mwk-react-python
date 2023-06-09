from typing import Type

from django.contrib.auth.models import User
from knox.models import AuthToken
from knox.views import LoginView
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from drf_spectacular.utils import extend_schema

from mwk.modules.authentication.permissions import Authenticated
from mwk.modules.authentication.serializers.knox_token import KnoxTokenSerializer
from mwk.modules.authentication.services.generate_token import generate_token


class UserLoginAPIView(LoginView):
    """Endpoint for user log-in (make token)"""

    permission_classes = (Authenticated,)

    def get_post_response_data(
        self,
        request,
        token: str,
        instance: AuthToken,
        user: User,
    ) -> dict:
        UserSerializer: Type[Serializer] = self.get_user_serializer_class()

        data = {
            'expiry': self.format_expiry_datetime(instance.expiry),
            'token': token,
            'user': UserSerializer(user, context=self.get_context()).data if UserSerializer else None,
        }

        return data

    @extend_schema(request=KnoxTokenSerializer, responses=KnoxTokenSerializer)
    def post(self, request) -> Response:
        serializer = KnoxTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token_data = generate_token(
            request,
            user,
            self.get_token_limit_per_user(),
            self.get_token_ttl()
        )

        return Response(self.get_post_response_data(*token_data, user))
