from rest_framework import serializers

from mwk.modules.main.models import Comment, Image, Post, PostCategory


class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCategory
        fields = ['id', 'title']
