from rest_framework.permissions import BasePermission


class Authenticated(BasePermission):
    """Allows access only to authenticated users"""

    def has_permission(self, request, view):
        return not request.user.is_authenticated
