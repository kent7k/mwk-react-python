from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema


class TokenCheckAPIView(APIView):
    """
    View to check if authentication token is valid.

    This view requires token authentication. If the token is valid,
    a 204 response is returned. Otherwise, an appropriate error response
    will be returned.
    """

    @extend_schema(request=None, responses=None)
    def get(self, request, format=None):
        """
        Check the validity of the authentication token.

        Returns:
            Response: A 204 response if the token is valid.
        """

        # TODO: Implement token validation logic here.
        # If validation fails, raise AuthenticationFailed.

        return Response(status=204)
