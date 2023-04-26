from drf_spectacular.utils import extend_schema
from knox.views import LogoutAllView


class UserLogoutAllAPIView(LogoutAllView):
    """Endpoint for logout all user tokens (destroy all tokens)"""

    @extend_schema(request=None, responses=None)
    def post(self, request, format=None):
        return super().post(request, format)
