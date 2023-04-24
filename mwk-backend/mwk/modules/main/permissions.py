from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    Permission class that allows access to the object only for the author of the object,
    and read-only access for all other users.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to perform the given action on the object.
        """

        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user
