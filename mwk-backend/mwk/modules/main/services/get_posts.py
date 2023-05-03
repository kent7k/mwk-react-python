from typing import TypeVar

from django.contrib.auth.models import User
from django.db.models import Count, Exists, OuterRef

from mwk.modules.main.models.post import Post


T = TypeVar('T')


def get_posts(user: User) -> list[Post]:
    def annotate_with_counts(queryset):
        return queryset.annotate(
            viewers_count=Count('viewers', distinct=True),
            liked_count=Count('liked', distinct=True),
            comments_count=Count('comments', distinct=True),
        )

    def author_in_user_following(queryset):
        return queryset.annotate(
            author_in_user_following=Exists(
                user.profile.following.filter(id=OuterRef('author__profile__id'))
            ),
        )

    posts = (
        Post.objects
            .all()
            .select_related('author__profile', 'category')
            .prefetch_related('images')
            .order_by('-created_at')
    )

    posts = annotate_with_counts(posts)
    posts = author_in_user_following(posts)

    return posts
