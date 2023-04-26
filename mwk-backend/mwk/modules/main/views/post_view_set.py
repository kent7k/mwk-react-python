from typing import Type

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from mwk.modules.main.models import Comment, Post
from mwk.modules.main.filters import PostFilter, filters
from mwk.modules.main.mixins import CacheTreeQuerysetMixin
from mwk.modules.main.serializers.CommentSerializer import CommentSerializer
from mwk.modules.main.serializers.PostCategorySerializer import PostCategorySerializer
from mwk.modules.main.serializers.PostSerializer import PostSerializer
from mwk.modules.main.services import (get_comment_descendants, get_comments,
                       get_post_categories, get_post_comments, get_posts)
from mwk.modules.main.mixins import IsAuthorPermissionsMixin


class PostViewSet(IsAuthorPermissionsMixin, CacheTreeQuerysetMixin, ModelViewSet):
    """Viewset for Posts"""

    serializer_class = PostSerializer
    comments_serializer_class = CommentSerializer
    categories_serializer_class = PostCategorySerializer

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PostFilter

    depth = 2  # comments depth

    def get_queryset(self):
        return get_posts(self.request.user)

    def get_serializer_class(self) -> Type[Serializer]:
        actions_serializers = {
            'get_comments': self.comments_serializer_class,
            'get_categories': self.categories_serializer_class,
        }

        if self.action in actions_serializers:
            return actions_serializers.get(self.action)

        return super().get_serializer_class()

    def validate_query(self, query: dict) -> None:
        """
        Validates GET query parameters, prohibits filtering posts by is_interesting and is_popular,
        since such sorting may cause ambiguous results.
        """

        if query.get('is_popular') and query.get('is_interesting'):
            raise ValidationError(
                detail={
                    'error': _(
                        'Sorting by both "interesting" and "popular" \
                        fields may result in not very obvious results.'
                    )
                },
                code='invalid_filters',
            )

    def list(self, request, *args, **kwargs):
        query = request.GET
        self.validate_query(query)

        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs) -> Response:
        instance = self.get_object()
        instance.add_views(request.user)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def get_comments(self, request, pk: int = None) -> Response:
        """Get comments for a post"""

        comments = self.get_cached_queryset(get_post_comments(request.user, pk))

        page = self.paginate_queryset(comments)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def like_post(self, request) -> Response:
        """Like a post"""

        pk = request.data.get('post')

        if not pk:
            return Response(status=400)

        post = get_object_or_404(Post, pk=pk)

        is_like = post.like(request.user)

        if is_like:
            return Response({'action': 'add'})

        return Response({'action': 'remove'})

    @action(detail=False, methods=['get'])
    def get_categories(self, request) -> Response:
        """Get categories"""

        categories = get_post_categories()

        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)
