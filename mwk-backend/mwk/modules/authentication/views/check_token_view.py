from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView


class CheckTokenAPIView(APIView):
    """
    View to check is authentication token valid

    Requires token authentication.
    """

    @extend_schema(request=None, responses=None)
    def get(self, request, format=None):
        """
        Return 204 response if token is valid.
        """

        return Response(status=204)
