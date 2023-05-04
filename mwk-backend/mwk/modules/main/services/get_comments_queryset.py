from typing import TypeVar

from django.contrib.auth.models import User
from django.db.models import Count, Exists, OuterRef

QuerySetType = TypeVar('QuerySetType', bound='QuerySet')


def get_comments_queryset(queryset: QuerySetType, user: User) -> QuerySetType:
    return (
        queryset.annotate(
            is_user_liked_comment=Exists(user.liked_comments.filter(id=OuterRef('id'))),
            liked_count=Count('liked', distinct=True),
        )
        .select_related('author', 'author__profile')
        .prefetch_related('images_comment')
    )
