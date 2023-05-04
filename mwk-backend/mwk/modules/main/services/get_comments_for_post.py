from django.contrib.auth.models import User
from mwk.modules.main.models.comment import Comment
from mwk.modules.main.services.get_comments_queryset import get_comments_queryset


def get_comments_for_post(user: User, post_id: int) -> list[Comment]:
    return get_comments_queryset(Comment.objects.filter(post_id=post_id), user)
