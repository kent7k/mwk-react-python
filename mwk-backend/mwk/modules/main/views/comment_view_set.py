from typing import Type

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from rest_framework.views import Response

from mwk.modules.main.helpers.CreateRetrieveUpdateDestroyViewSet import CreateRetrieveUpdateDestroyViewSet
from mwk.modules.main.models import Comment
from mwk.modules.main.serializers.CommentSerializer import CommentSerializer
from mwk.modules.main.serializers.CommentUpdateSerializer import CommentUpdateSerializer
from mwk.modules.main.services import get_comment_descendants
from mwk.modules.main.services import get_comments

from mwk.modules.main.mixins import IsAuthorPermissionsMixin


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
