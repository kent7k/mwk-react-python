from typing import TypeVar

from django.contrib.auth.models import User

from mwk.modules.main.models.comment import Comment
from mwk.modules.main.services.get_comments_queryset import get_comments_queryset


T = TypeVar('T')


def get_comments(user: User) -> list[Comment]:
    """Get all comments"""

    comments = get_comments_queryset(Comment.objects.all(), user)
    return comments
