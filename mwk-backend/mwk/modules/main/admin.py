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
    list_display = ['id', '__str__', 'created_at']
    list_display_links = ['id', '__str__']
    search_fields = ['id', 'title']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
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
    fields = [
        'id',
        'profile',
        'title',
        'content',
        'category',
        'viewers_count',
        'liked_count',
        'author',
        'created_at',
        'updated_at',
        'get_post_photo',
    ]
    readonly_fields = [
        'id',
        'created_at',
        'updated_at',
        'viewers_count',
        'liked_count',
        'get_post_photo',
    ]

    def liked_count(self, obj: Post) -> int:
        return obj.liked.count()

    liked_count.short_description = 'LIKES COUNT'

    def viewers_count(self, obj: Post) -> int:
        return obj.viewers.count()

    viewers_count.short_description = 'VIEWS COUNT'

    def get_post_photo(self, obj: Post) -> Union[SafeString, str]:
        images = obj.images

        if images.exists():
            image = images.first().photo
            return mark_safe(f'<img src="{image.url}" height="40" width="40">')
        else:
            return '-'

    get_post_photo.short_description = 'Thumbnail'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('category', 'author').prefetch_related(
            'liked', 'viewers', 'images'
        )


@admin.register(Comment)
class CommentAdmin(MPTTModelAdmin):
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
    fields = [
        'id',
        'post',
        'author',
        'liked_count',
        'liked',
        'parent',
        'body',
        'created_at',
        'updated_at',
    ]
    readonly_fields = ['id', 'liked_count', 'created_at', 'updated_at']
    list_select_related = ['parent', 'author', 'post']
    autocomplete_fields = ['author', 'post']

    def is_reply(self, obj: Comment) -> str:
        if not obj.parent:
            return 'No'
        else:
            return 'Yes'

    is_reply.short_description = 'Answer?'

    def liked_count(self, obj: Comment) -> int:
        return obj.liked.count()

    liked_count.short_description = 'LIKES COUNT'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('liked')

    def validate_parent_not_references_to_other_post(
        self, parent_id: int, post_id: int
    ) -> None:
        """Checks that the parent comment is not attached to another post"""

        if not Comment.objects.filter(id=parent_id, post_id=post_id).exists():
            raise ValidationError(
                _('The parent comment belongs to a different post.')
            )

    def save_model(
        self, request, obj: Comment, form: AdminModelForm, change: bool
    ) -> None:
        """Does not allow to set parent comment from other post"""

        parent_id: int = form.data.get(
            'parent'
        )  # parent does not available yet object not save
        post_id: int = form.data.get('post')

        try:
            if parent_id:
                self.validate_parent_not_references_to_other_post(parent_id, post_id)
            super().save_model(request, obj, form, change)
        except ValidationError as err:
            form.cleaned_data.pop('liked')  # removing the m2m field to avoid an error

            messages.set_level(request, messages.ERROR)  # prevent success message
            messages.error(request, err.message)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    """Image model admin"""

    list_display = ['id', 'post', 'comment', 'author', 'get_image', 'created_at']
    list_display_links = ['id', 'post', 'comment', 'get_image']
    list_select_related = ['post', 'comment', 'author']
    search_fields = ['id', 'author__username']
    empty_value_display = '-'
    fields = ['id', 'post', 'comment', 'photo', 'get_image', 'author', 'created_at']
    readonly_fields = ['id', 'created_at', 'get_image']
    ordering = ['-created_at']
    autocomplete_fields = ['author', 'post', 'comment']

    def get_image(self, obj: Image) -> SafeString:
        return mark_safe(f'<img src="{obj.photo.url}" height="40" width="40">')

    get_image.short_description = 'Thumbnail'

    def validate_not_post_and_comment_together(self, obj: Image) -> None:
        """Checks that both post and comment fields are not set together"""

        if obj.post and obj.comment:
            raise ValidationError(
                _(
                    'You cannot attach an image to both a post and a comment at the same time.'
                )
            )

    def save_model(
        self, request, obj: Image, form: AdminModelForm, change: bool
    ) -> None:
        """Does not allow to set two fields post and comment at the same time"""

        try:
            self.validate_not_post_and_comment_together(obj)
            super().save_model(request, obj, form, change)
        except ValidationError as err:
            messages.set_level(request, messages.ERROR)  # prevent success message
            messages.error(request, err.message)
