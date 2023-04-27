from rest_framework import serializers

from mwk.modules.main.models.comment import Comment
from mwk.modules.main.models.image import Image
from mwk.modules.main.models.post_category import PostCategory
from mwk.modules.main.models.post import Post


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['photo']
