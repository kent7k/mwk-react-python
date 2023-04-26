from rest_framework import serializers

from mwk.modules.authentication.models import Profile
from mwk.modules.profiles.serializers.UserSerializer import UserSerializer


class FollowersSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'avatar']

