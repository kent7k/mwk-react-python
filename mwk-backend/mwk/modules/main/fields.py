from typing import TypeVar

from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for representing the author's data"""

    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        return serializers.ImageField(source='profile.avatar').to_representation(obj)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar']


@extend_schema_field(
    {
        'type': 'string',
        'format': 'string',
        'read_only': True,
        'example': {
            'first_name': 'string',
            'last_name': 'string',
            'avatar': 'string',
        },
    }
)
class CurrentAuthorField(serializers.Field):
    """
    Field for representing the author's data, requires the User object as input and returns the data for it.
    Ignores any input value, focusing only on the default value.
    """

    T = TypeVar('T')

    def get_value(self, dictionary: dict) -> serializers.empty:
        return serializers.empty

    def to_representation(self, value: User) -> dict:
        """To JSON"""

        return AuthorSerializer(
            instance=value, context={'request': self.context.get('request')}
        ).data

    def to_internal_value(self, data: T) -> T:
        """From JSON"""

        return data


class DateTimeTimezoneField(serializers.DateTimeField):
    """DateTime field that includes the current user timezone"""

    def default_timezone(self):
        request = self.context.get('request')

        if request:
            return request.timezone
        return super().default_timezone()


@extend_schema_field(
    {
        'type': 'string',
        'format': 'string',
    }
)
class PostCategoryField(serializers.PrimaryKeyRelatedField):
    """Read-write field for PostCategory.
    Provides the str_representation of the PostCategory object as output and accepts a category PK as input"""

    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        """To JSON"""

        return str(value)
