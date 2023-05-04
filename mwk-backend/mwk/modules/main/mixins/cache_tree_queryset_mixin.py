from mptt.utils import get_cached_trees


class CacheTreeQuerysetMixin:
    """
    A mixin that caches the TreeQueryset via the mptt.get_cached_trees() function
    into the `_cached_queryset` attribute to avoid duplicate queries.

    The `depth` attribute specifies the length of mptt descendants to include.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_queryset = None

    depth = None

    def get_cached_queryset(self, queryset) -> list:
        """
        Get the cached queryset from the cache or set `get_cached_trees(queryset)`
        to the cache and return it.

        If the `depth` attribute is set, filter the queryset by descendants of
        at most that depth.
        """

        if self.depth:
            queryset = queryset.filter(level__lte=self.depth)

        self._cached_queryset = self._cached_queryset or get_cached_trees(queryset)
        return self._cached_queryset
