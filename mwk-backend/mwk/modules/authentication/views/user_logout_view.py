from drf_spectacular.utils import extend_schema
from knox.views import LogoutView


class UserLogoutAPIView(LogoutView):
    """Endpoint for user log-out (destroy token)"""

    @extend_schema(request=None, responses=None)
    def post(self, request):
        return super().post(request)
