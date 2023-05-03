from typing import TypeVar

from django.contrib.auth.models import User
from django.db.models import Count, Exists, OuterRef

T = TypeVar('T')


def get_comments_queryset(queryset: T, user: User) -> T:
    """Annotate and JOIN the comments queryset"""

    return (
        queryset.annotate(
            is_user_liked_comment=Exists(user.liked_comments.filter(id=OuterRef('id'))),
            like_cnt=Count('liked', distinct=True),
        )
        .select_related('author', 'author__profile')
        .prefetch_related('images_comment')
    )
