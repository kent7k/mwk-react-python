from typing import List

from django.contrib.auth.models import User

from mwk.modules.main.models.comment import Comment
from mwk.modules.main.services.get_comments_queryset import get_comments_queryset


def get_descendant_comments(comment: Comment, user: User) -> List[Comment]:
    return get_comments_queryset(comment.get_comment_replies(), user)
