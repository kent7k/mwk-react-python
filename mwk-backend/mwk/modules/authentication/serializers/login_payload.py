from django.contrib.auth.models import User
from rest_framework import serializers


class LoginPayloadSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(read_only=True)
    profile_id = serializers.PrimaryKeyRelatedField(source='profile', read_only=True)

    def get_avatar(self, user: User):
        field = serializers.ImageField()
        field.bind('avatar', self)
        return field.to_representation(user.profile.avatar)

    class Meta:
        model = User
        fields = ['profile_id', 'first_name', 'last_name', 'avatar']
        extra_kwargs = {
            'first_name': {'read_only': True},
            'last_name': {'read_only': True},
        }
