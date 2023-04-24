from typing import Type

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.views import Response
from rest_framework.viewsets import ModelViewSet

from .filters import PostFilter, filters
from .helpers.viewsets import CreateRetrieveUpdateDestroyViewSet
from .mixins import CacheTreeQuerysetMixin, IsAuthorPermissionsMixin
from .models import Comment, Post
from .serializers import (CommentSerializer, CommentUpdateSerializer,
                          PostCategorySerializer, PostSerializer)
from .services import (get_comment_descendants, get_comments,
                       get_post_categories, get_post_comments, get_posts)


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


class CommentViewSet(IsAuthorPermissionsMixin, CreateRetrieveUpdateDestroyViewSet):
    """Viewset for Comments"""

    serializer_class = CommentSerializer
    update_serializer_class = CommentUpdateSerializer

    def get_queryset(self):
        return get_comments(self.request.user)

    def get_serializer_context(self) -> dict:
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'show_replies': False,
        }

    def get_serializer_class(self) -> Type[Serializer]:
        if self.request.method == 'PATCH':
            return self.update_serializer_class

        return super().get_serializer_class()

    @action(detail=True, methods=['get'])
    def get_descendants(self, request, pk: int = None):
        """Get all comment descendants in a flat view"""

        parent: Comment = get_object_or_404(Comment, pk=pk)
        descendants = get_comment_descendants(parent, request.user)

        page = self.paginate_queryset(descendants)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(descendants, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def like_comment(self, request) -> Response:
        """Like a comment"""

        pk = request.data.get('comment')

        if not pk:
            return Response(status=400)

        comment = get_object_or_404(Comment, pk=pk)

        is_like = comment.like(request.user)

        if is_like:
            return Response({'action': 'add'})

        return Response({'action': 'remove'})
