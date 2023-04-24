from mptt.utils import get_cached_trees
from rest_framework import serializers
from rest_framework.settings import api_settings

from .permissions import IsAuthorOrReadOnly


class CacheTreeQuerysetMixin:
    """
    A mixin that caches the TreeQueryset via the mptt.get_cached_trees() function
    into the `_cached_queryset` attribute to avoid duplicate queries.

    The `depth` attribute specifies the length of mptt descendants to include.
    """

    _cached_queryset: list = None
    depth: int = None

    def get_cached_queryset(self, queryset) -> list:
        """
        Get the cached queryset from the cache or set `get_cached_trees(queryset)`
        to the cache and return it.

        If the `depth` attribute is set, filter the queryset by descendants of
        at most that depth.
        """

        if self.depth:
            queryset = queryset.filter(level__lte=self.depth)

        if not self._cached_queryset:
            self._cached_queryset = get_cached_trees(queryset)

        return self._cached_queryset


class IsAuthorPermissionsMixin:
    """
    A mixin that extends the default permissions with the `IsAuthorOrReadOnly` permission.
    """

    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsAuthorOrReadOnly]


class ErrorMessagesSerializersMixin:
    """
    A mixin for serializers that makes it easy to raise exceptions from `default_error_messages`.

    This mixin provides a helper method `fail()` that raises a validation error with the
    specified error message key from the `error_messages` dictionary.

    This mixin was created because the default `self.fail()` method of serializers
    does not support errors in the form of dictionaries.
    """

    def fail(self, key: str) -> None:
        """
        Raises a validation error with the specified error message key from the `error_messages` dictionary.

        If the key is not found in the dictionary, a `KeyError` is raised with a
        custom error message indicating the class name and the missing key.
        """

        try:
            msg = self.error_messages[key]
        except KeyError:
            class_name = self.__class__.__name__
            error_message = "\
                ValidationError raised by `{class_name}`,\
                but error key `{key}` does not exist in the `error_messages` dictionary."
            msg = error_message.format(class_name=class_name, key=key)
            raise KeyError(msg)

        raise serializers.ValidationError(msg, code=key)
