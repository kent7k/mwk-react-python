from typing import Collection, Iterable

from django.utils.translation import gettext as _
from mptt.models import MPTTModel
from rest_framework import serializers

from .fields import (CurrentAuthorField, DateTimeTimezoneField,
                     PostCategoryField)
from .helpers.helpers import validate_images
from .mixins import ErrorMessagesSerializersMixin
from .models import Comment, Image, Post, PostCategory
from .services import create_comment_images, create_post_images


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['photo']


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id', 'title']


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


class CommentSerializer(ErrorMessagesSerializersMixin, serializers.ModelSerializer):
    is_user_liked_comment = serializers.BooleanField(read_only=True)
    like_cnt = serializers.IntegerField(read_only=True, default=0)
    replies_cnt = serializers.IntegerField(read_only=True)
    images = ImageSerializer(many=True, read_only=True, source='images_comment')
    author = CurrentAuthorField(default=serializers.CurrentUserDefault())
    replies = serializers.SerializerMethodField(read_only=True)

    default_error_messages = {
        'empty_comment': _('Empty comment'),
        'parent_comment_references_to_other_post': {
            'parent': _('The parent comment is left under a different post.')
        },
    }

    def get_grandchildren(self, childrens: Collection[MPTTModel]) -> list:
        """
        This method is designed to form a flat list of node descendants up to the second level,
        thereby greatly facilitating the work of the frontend.

        It avoids the need to navigate through a complex tree structure of descendants,
        by outputting only descendants of level 2 or less, and limiting the page to 3 nodes.

        This method has not been tested with a large number of nodes and levels, so it may cause overhead.

        If the QuerySet in the view was cached in advance using mptt.utils.get_cached_trees(),
        this method will not cause any queries to the database.

        Any overhead is likely to be caused by copies of the list.
        """

        grandchildren = []

        for children in childrens:
            grandson = children.get_children().first()
            if grandson:
                grandchildren.extend([children, grandson])
            else:
                grandchildren.extend([children])

        return grandchildren

    def get_replies(self, obj: Comment) -> dict:
        """
        If the comment is a root comment and children are not disabled,
        get the children up to the second level (see get_grandchildren).
        """

        if obj.level != 0 or self.context.get('show_replies') is False:
            return []

        childrens = obj.get_children()[:2]
        descendants = self.get_grandchildren(childrens)
        return self.__class__(descendants, many=True, context=self.context).data

    def validate_parent_not_references_to_other_post(
        self, parent_id: int, post_id: int
    ) -> None:
        """
        Checks if the parent comment references to the same post.
        """

        if not Comment.objects.filter(id=parent_id, post_id=post_id).exists():
            self.fail('parent_comment_references_to_other_post')

    def validate(self, attrs: dict) -> None:
        request = self.context.get('request')
        images, body = request.FILES.getlist('images'), attrs.get('body')
        parent, post_id = attrs.get('parent'), attrs.get('post').id

        if not any((images, body)):
            self.fail('empty_comment')

        if parent:
            self.validate_parent_not_references_to_other_post(parent.id, post_id)

        validate_images(images)

        return super().validate(attrs)

    def images_create(self, images: Iterable, comment_id: int) -> None:
        """
        Adds images to the comment
        """

        author = self.context.get('request').user
        create_comment_images(images, comment_id, author)

    def create(self, validated_data: dict) -> Comment:
        instance = super().create(validated_data)
        images = self.context.get('request').FILES.getlist('images')

        self.images_create(images, instance.id)
        return instance

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'created_at',
            'updated_at',
            'parent',
            'body',
            'is_user_liked_comment',
            'replies',
            'like_cnt',
            'images',
            'author',
            'replies_cnt',
        ]
        extra_kwargs = {'body': {'required': False}}


class CommentUpdateSerializer(CommentSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    def images_create(self, images: Iterable, comment_id: int) -> None:
        """
        Adds images to the comment
        """

        author = self.context.get('request').user
        create_comment_images(images, comment_id, author, True)

    def update(self, instance: Comment, validated_data: dict) -> Comment:
        instance = super().update(instance, validated_data)
        images = self.context.get('request').FILES.getlist('images')

        self.images_create(images, instance.id)
        return instance
