from typing import Type

from django.contrib.auth.models import User
from knox.models import AuthToken
from knox.views import LoginView
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from drf_spectacular.utils import extend_schema

from mwk.modules.authentication.permissions import Authenticated
from mwk.modules.authentication.serializers.knox_token import KnoxTokenSerializer
from mwk.modules.authentication.services import activate_user, create_authtoken, send_activation_email


class UserLoginAPIView(LoginView):
    """Endpoint for user log-in (make token)"""

    permission_classes = (Authenticated,)

    def get_post_response_data(
        self, request, token: str, instance: AuthToken, user: User
    ) -> dict:
        UserSerializer: Type[Serializer] = self.get_user_serializer_class()

        data = {'expiry': self.format_expiry_datetime(instance.expiry), 'token': token}

        if UserSerializer is not None:
            data['user'] = UserSerializer(user, context=self.get_context()).data
        return data

    @extend_schema(request=KnoxTokenSerializer, responses=KnoxTokenSerializer)
    def post(self, request) -> Response:
        serializer = KnoxTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token_data = create_authtoken(
            request, user, self.get_token_limit_per_user(), self.get_token_ttl()
        )

        return Response(self.get_post_response_data(*token_data, user))
