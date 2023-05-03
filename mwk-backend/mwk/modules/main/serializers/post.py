from typing import Collection, Iterable

from django.utils.translation import gettext as _
from rest_framework import serializers

from mwk.modules.main.fields import CurrentAuthorField, DateTimeTimezoneField, PostCategoryField
from mwk.modules.main.helpers.helpers import validate_images
from mwk.modules.main.mixins import ErrorMessagesSerializersMixin
from mwk.modules.main.models.post_category import PostCategory
from mwk.modules.main.models.post import Post

from mwk.modules.main.services.create_post_images import create_post_images

from mwk.modules.main.serializers.image import ImageSerializer


class PostSerializer(ErrorMessagesSerializersMixin, serializers.ModelSerializer):
    viewers_count = serializers.IntegerField(read_only=True)
    liked_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)

    author_in_user_following = serializers.BooleanField(read_only=True)
    is_user_liked_post = serializers.BooleanField(read_only=True)
    author = CurrentAuthorField(default=serializers.CurrentUserDefault())
    images = ImageSerializer(many=True, read_only=True)
    created_at = DateTimeTimezoneField(read_only=True)
    updated_at = DateTimeTimezoneField(read_only=True)
    category = PostCategoryField(queryset=PostCategory.objects.all())

    default_error_messages = {
        'empty_post': _('Empty post'),
    }

    def validate(self, attrs: dict) -> None:
        request = self.context.get('request')
        images, title, content = (
            request.FILES.getlist('images'),
            attrs.get('title'),
            attrs.get('content'),
        )

        if not any((images, title, content)):
            self.fail('empty_post')

        validate_images(images)

        return super().validate(attrs)

    def images_create(
        self, images: Iterable, post_id: int, is_update: bool = False
    ) -> None:
        """
        Adds images to the post
        """

        author = self.context.get('request').user
        create_post_images(images, post_id, author, is_update)

    def create(self, validated_data: dict) -> Post:
        instance = super().create(validated_data)
        images = self.context.get('request').FILES.getlist('images')

        self.images_create(images, instance.id)
        return instance

    def update(self, instance: Post, validated_data: dict) -> Post:
        instance = super().update(instance, validated_data)
        images = self.context.get('request').FILES.getlist('images')

        self.images_create(images, instance.id, is_update=True)
        return instance

    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'content',
            'created_at',
            'updated_at',
            'author',
            'viewers_count',
            'liked_count',
            'comments_count',
            'author_in_user_following',
            'is_user_liked_post',
            'images',
            'category',
        ]

