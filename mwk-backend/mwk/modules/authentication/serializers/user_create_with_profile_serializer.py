from collections import OrderedDict
from typing import Union

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db.utils import IntegrityError
from django.utils.translation import gettext as _
from rest_framework import serializers

from mwk.modules.main.mixins import ErrorMessagesSerializersMixin

from mwk.modules.authentication.helpers import contains_digits, is_age_at_least
from mwk.modules.authentication.services import register_user
from mwk.modules.authentication.serializers.profile_create_serializer import ProfileCreateSerializer


class UserCreateWithProfileSerializer(ErrorMessagesSerializersMixin, serializers.ModelSerializer):
    email = serializers.EmailField(
        label='Email address', required=True, write_only=True
    )
    profile = ProfileCreateSerializer(required=True)

    default_error_messages = {
        'cannot_create_user': _(
            'Failed to create user, please try again.'
        ),
        'username_contains_only_digits': {
            'username': _('Login cannot consist only of digits.')
        },
        'first_name_contains_digits': {
            'first_name': _('First name cannot contain digits.'),
        },
        'last_name_contains_digits': {
            'last_name': _('Last name cannot contain digits.'),
        },
    }

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_active',
            'profile',
        )
        extra_kwargs = {
            'password': {'write_only': True, 'validators': [validate_password]},
            'is_active': {'read_only': True},
            'username': {'max_length': 50, 'min_length': 4},
            'first_name': {'required': True, 'allow_blank': False, 'max_length': 30},
            'last_name': {'required': True, 'allow_blank': False, 'max_length': 30},
        }

    def validate_names(self, username: str, first_name: str, last_name: str) -> None:
        if username.isdigit():
            self.fail('username_contains_only_digits')
        if contains_digits(first_name):
            self.fail('first_name_contains_digits')
        if contains_digits(last_name):
            self.fail('last_name_contains_digits')

    def validate(self, attrs: dict):
        username, first_name, last_name = (
            attrs.get('username'),
            attrs.get('first_name'),
            attrs.get('last_name'),
        )
        self.validate_names(username, first_name, last_name)
        return super().validate(attrs)

    def create(self, validated_data: OrderedDict) -> Union[User, None]:
        try:
            user = self.perform_create(validated_data)
            return user
        except IntegrityError:
            self.fail('cannot_create_user')

    def perform_create(self, validated_data: OrderedDict) -> User:
        password = validated_data.pop('password')
        profile_data: dict = validated_data.pop('profile', None)

        return register_user(validated_data, password, profile_data)
