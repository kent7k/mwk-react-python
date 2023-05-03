from rest_framework import serializers

from mwk.modules.main.models.post_category import PostCategory


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id', 'title']
