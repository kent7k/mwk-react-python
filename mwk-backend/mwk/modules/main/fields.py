from typing import TypeVar

from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for representing the author's data"""

    avatar = serializers.ImageField(source='profile.avatar')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar']


@extend_schema_field(AuthorSerializer)
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
        return AuthorSerializer(instance=value, context=self.context).data

    def to_internal_value(self, data: T) -> T:
        """From JSON"""
        return data


class DateTimeTimezoneField(serializers.DateTimeField):
    """DateTime field that includes the current user timezone"""

    def default_timezone(self):
        request = self.context.get('request')
        return request.timezone if request else super().default_timezone()


@extend_schema_field(serializers.PrimaryKeyRelatedField)
class PostCategoryField(serializers.PrimaryKeyRelatedField):
    """Read-write field for PostCategory.
    Provides the str_representation of the PostCategory object as output and accepts a category PK as input"""

    def to_representation(self, value):
        """To JSON"""
        return str(value)

    def use_pk_only_optimization(self):
        return False

