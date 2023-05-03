from typing import TypeVar

from django.contrib.auth.models import User
from django.db.models import Count, Exists, OuterRef

from mwk.modules.main.models.post import Post


T = TypeVar('T')


def get_posts(user: User) -> list[Post]:
    """Get posts queryset"""

    posts = (
        Post.objects.annotate(
            viewers_count=Count('viewers', distinct=True),
            liked_count=Count('liked', distinct=True),
            comments_count=Count('comments', distinct=True),
            author_in_user_following=Exists(
                user.profile.following.filter(id=OuterRef('author__profile__id'))
            ),
            is_user_liked_post=Exists(user.liked_posts.filter(id=OuterRef('id'))),
        )
        .select_related('author__profile', 'category')
        .prefetch_related('images')
        .order_by('-created_at')
    )

    return posts

