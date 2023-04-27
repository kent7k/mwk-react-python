from rest_framework import serializers

from mwk.modules.authentication.models.profile import Profile
from mwk.modules.profiles.serializers.followers import FollowersSerializer
from mwk.modules.profiles.serializers.user import UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    followers = FollowersSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            'avatar',
            'created_at',
            'bio',
            'followers',
            'birthday',
        ]
