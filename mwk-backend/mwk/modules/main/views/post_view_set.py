from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from mwk.modules.main.models.post import Post
from mwk.modules.main.filters import PostFilter, filters
from mwk.modules.main.mixins.cache_tree_queryset_mixin import CacheTreeQuerysetMixin
from mwk.modules.main.serializers.comment import CommentSerializer
from mwk.modules.main.serializers.post_category import PostCategorySerializer
from mwk.modules.main.serializers.post import PostSerializer
from mwk.modules.main.mixins.author_permissions_mixin import AuthorPermissionsMixin
from mwk.modules.main.services.get_comments_for_post import get_comments_for_post
from mwk.modules.main.services.get_all_posts import get_all_posts
from mwk.modules.main.services.get_post_categories import get_post_categories


class PostViewSet(AuthorPermissionsMixin, CacheTreeQuerysetMixin, ModelViewSet):

    serializer_class = PostSerializer
    comments_serializer_class = CommentSerializer
    categories_serializer_class = PostCategorySerializer

    serializer_classes = {
        'get_all_comments': comments_serializer_class,
        'get_categories': categories_serializer_class,
    }

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilter
    depth = 2  # comments depth

    def get_queryset(self):
        return get_all_posts(self.request.user)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, super().get_serializer_class())

    @staticmethod
    def validate_post_filters(filters: dict) -> None:
        if all(filters.get(key) for key in ('is_popular', 'is_interesting')):
            raise ValidationError({'error': _('Sorting by both "interesting" and "popular" fields may result in ambiguous results.')}, code='invalid_filters')

    def list(self, request, *args, **kwargs):
        query = request.GET
        self.validate_post_filters(query)
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        instance.add_views(request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], serializer_class=CommentSerializer)
    def get_all_comments(self, request, pk: int = None) -> Response:
        """Get comments for a post"""

        comments = self.get_cached_queryset(get_comments_for_post(request.user, pk))
        page = self.paginate_queryset(comments)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def like_post(self, request) -> Response:

        pk = request.data.get('post')

        if not pk:
            raise ValidationError({'post': _('This field is required.')})

        post = get_object_or_404(Post, pk=pk)

        is_like = post.like(request.user)
        like_action = 'add' if is_like else 'remove'

        return Response({'action': like_action})

    @action(detail=False, methods=['get'])
    def get_categories(self, request) -> Response:

        categories = get_post_categories()

        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
