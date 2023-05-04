from typing import Type, Dict, Any

from django.shortcuts import get_object_or_404
from django.utils.translation import gettext as _
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import Serializer
from rest_framework.response import Response

from mwk.modules.main.helpers.create_retrieve_update_destroy_viewset import CreateRetrieveUpdateDestroyViewSet
from mwk.modules.main.models.comment import Comment
from mwk.modules.main.serializers.comment import CommentSerializer
from mwk.modules.main.serializers.comment_update import CommentUpdateSerializer
from mwk.modules.main.services.get_descendant_comments import get_descendant_comments
from mwk.modules.main.mixins.author_permissions_mixin import AuthorPermissionsMixin


class CommentViewSet(AuthorPermissionsMixin, CreateRetrieveUpdateDestroyViewSet):

    serializer_class = CommentSerializer
    update_serializer_class = CommentUpdateSerializer

    def get_serializer_context(self) -> Dict[str, Any]:
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self,
            'show_replies': False,
        }

    def get_serializer_class(self) -> Type[Serializer]:
        return self.update_serializer_class if self.request.method == 'PATCH' else super().get_serializer_class()

    @action(detail=True, methods=['get'])
    def get_comment_replies(self, request, pk: int = None) -> Response:
        comment = get_object_or_404(Comment, pk=pk)
        descendants = get_descendant_comments(comment, request.user)

        page = self.paginate_queryset(descendants)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(descendants, many=True)
            return Response(serializer.data)

    @action(detail=False, methods=['put'])
    def like_post_comment(self, request) -> Response:
        comment_id = request.data.get('Comment')

        if not comment_id:
            raise ValidationError({'Comment': _('This field is required.')})

        comment = get_object_or_404(Comment, pk=comment_id)

        like_post_comment_action = 'add' if comment.like(request.user) else 'remove'

        return Response({'action': like_post_comment_action})
