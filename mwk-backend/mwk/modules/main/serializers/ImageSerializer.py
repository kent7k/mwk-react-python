from rest_framework import serializers

from mwk.modules.main.models import Comment, Image, Post, PostCategory


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['photo']
