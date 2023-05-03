from typing import Collection, Iterable

from django.utils.translation import gettext as _
from mptt.models import MPTTModel
from rest_framework import serializers

from mwk.modules.main.fields import CurrentAuthorField, DateTimeTimezoneField, PostCategoryField
from mwk.modules.main.helpers.helpers import validate_images
from mwk.modules.main.mixins.error_messages_serializers_mixin import ErrorMessagesSerializersMixin
from mwk.modules.main.models.comment import Comment


from mwk.modules.main.services.add_images_to_comment import add_images_to_comment
from mwk.modules.main.serializers.image import ImageSerializer


class CommentSerializer(ErrorMessagesSerializersMixin, serializers.ModelSerializer):
    is_user_liked_comment = serializers.BooleanField(read_only=True)
    liked_count = serializers.IntegerField(read_only=True, default=0)
    replies_count = serializers.IntegerField(read_only=True)
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
        This method is designed to form a flat list of node descendants up to the second level
        thereby greatly facilitating the work of the frontend.

        Because it does not have to go through a complex tree structure of descendants
        provided that we give only 3 nodes to each page and also output only descendants of level 2 inclusive.

        This does not cause a strong overhead,
        but this has not been tested on a large number of nodes and levels.

        Provided that the QuerySet in the view was cached in advance via mptt.utils.get_cached_trees()
        this will not cause any queries to the database.

        The entire overhead can occur only because of copies of the list.
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
        if the comment is root comment and children are not disabled,
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
        """Checks if the parent comment links to another post"""

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
        add_images_to_comment(images, comment_id, author)

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
            'liked_count',
            'images',
            'author',
            'replies_count',
        ]
        extra_kwargs = {'body': {'required': False}}
