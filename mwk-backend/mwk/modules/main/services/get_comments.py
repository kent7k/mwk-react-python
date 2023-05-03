from django.contrib.auth.models import User

from mwk.modules.main.models.comment import Comment
from mwk.modules.main.services.get_comments_queryset import get_comments_queryset


def get_all_comments(user: User) -> list[Comment]:
    return get_comments_queryset(Comment.objects.all(), user)
