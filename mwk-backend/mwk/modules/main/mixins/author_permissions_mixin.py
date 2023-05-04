from rest_framework.settings import api_settings

from ..permissions import IsAuthorOrReadOnly


class AuthorPermissionsMixin:
    permission_classes = [*api_settings.DEFAULT_PERMISSION_CLASSES, IsAuthorOrReadOnly]
