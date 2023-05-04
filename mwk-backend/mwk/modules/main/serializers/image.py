from rest_framework import serializers

from mwk.modules.main.models.image import Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['photo']
