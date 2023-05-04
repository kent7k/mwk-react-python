from typing import Iterable

from rest_framework import serializers

from mwk.modules.main.models.comment import Comment


from mwk.modules.main.services.add_images_to_comment import add_images_to_comment
from mwk.modules.main.serializers.comment import CommentSerializer


class CommentUpdateSerializer(CommentSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    def images_create(self, images: Iterable, comment_id: int) -> None:
        """
        Adds images to the comment
        """

        author = self.context.get('request').user
        add_images_to_comment(images, comment_id, author, True)

    def update(self, instance: Comment, validated_data: dict) -> Comment:
        instance = super().update(instance, validated_data)
        images = self.context.get('request').FILES.getlist('images')

        self.images_create(images, instance.id)
        return instance
