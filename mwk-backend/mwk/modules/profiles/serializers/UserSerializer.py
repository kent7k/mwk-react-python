from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'groups']
