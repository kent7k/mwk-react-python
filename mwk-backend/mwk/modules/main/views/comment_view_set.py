from typing import Type

from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.serializers import Serializer
from rest_framework.views import Response

from mwk.modules.main.helpers.create_retrieve_update_destroy_viewset import CreateRetrieveUpdateDestroyViewSet
from mwk.modules.main.models.comment import Comment
from mwk.modules.main.serializers.comment import CommentSerializer
from mwk.modules.main.serializers.comment_update import CommentUpdateSerializer
from mwk.modules.main.services.get_descendant_comments import get_descendant_comments

from mwk.modules.main.mixins import IsAuthorPermissionsMixin


class CommentViewSet(IsAuthorPermissionsMixin, CreateRetrieveUpdateDestroyViewSet):
    """Viewset for Comments"""

    serializer_class = CommentSerializer
    update_serializer_class = CommentUpdateSerializer

    def get_serializer_context(self) -> dict:
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'show_replies': False,
        }

    def get_serializer_class(self) -> Type[Serializer]:
        return self.update_serializer_class if self.request.method == 'PATCH' else super().get_serializer_class()

    @action(detail=True, methods=['get'])
    def get_descendants(self, request, pk: int = None):
        """Get all comment descendants in a flat view"""

        parent: Comment = get_object_or_404(Comment, pk=pk)
        descendants = get_descendant_comments(parent, request.user)

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

        action = 'add' if comment.like(request.user) else 'remove'

        return Response({'action': action})
