from typing import Union

from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.utils.safestring import SafeString, mark_safe
from django.utils.translation import gettext as _
from mptt.admin import MPTTModelAdmin

from .admin_types import AdminModelForm
from mwk.modules.main.models.comment import Comment
from mwk.modules.main.models.image import Image
from mwk.modules.main.models.post_category import PostCategory
from mwk.modules.main.models.post import Post


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    """PostCategory model admin"""

    list_display = ['id', '__str__', 'created_at']
    list_display_links = ['id', '__str__']
    search_fields = ['id', 'title']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Post model admin"""

    list_display = [
        'id',
        '__str__',
        'author',
        'category',
        'liked_count',
        'viewers_count',
        'created_at',
        'updated_at',
        'get_post_photo',
    ]
    list_display_links = ['id', '__str__']
    list_select_related = ['author', 'profile']
    list_filter = ['category']
    search_fields = ['id', 'title', 'author__username']
    empty_value_display = '-'
    autocomplete_fields = ['author', 'profile', 'category']
    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'viewers_count',
        'liked_count',
        'get_post_photo',
    ]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category', 'author').prefetch_related(
            'liked', 'viewers', 'images'
        )

    def liked_count(self, obj: Post) -> int:
        return obj.liked.count()

    liked_count.short_description = 'Count of likes'

    def viewers_count(self, obj: Post) -> int:
        return obj.viewers.count()

    viewers_count.short_description = 'Count of views'

    def get_post_photo(self, obj: Post) -> Union[SafeString, str]:
        images = obj.images

        if images.exists():
            image = images.first().photo
            return mark_safe(f'<img src="{image.url}" height="40" width="40">')
        else:
            return '-'

    get_post_photo.short_description = 'Thumbnail'


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
    """Comment model mptt-admin"""

    list_display = [
        'id',
        'post'[:50],
        'author',
        'liked_count',
        'created_at',
        'updated_at',
        'is_reply',
    ]
    list_display_links = ['id', 'post']
    search_fields = ['author__username', 'post__title', 'id']
    empty_value_display = '-'
    readonly_fields = ['id', 'liked_count', 'created_at', 'updated_at']
    list_select_related = ['parent', 'author', 'post']
    autocomplete_fields = ['author', 'post']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('liked')

    def is_reply(self, obj: Comment) -> str:
        if not obj.parent:
            return 'No'
        else:
            return 'Yes'


