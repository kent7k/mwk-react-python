from collections import OrderedDict
from datetime import date
from typing import Union

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.db.utils import IntegrityError
from django.utils.translation import gettext as _
from djoser.serializers import ActivationSerializer as DjoserActivationSerializer
from drf_extra_fields.fields import HybridImageField
from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer

from mwk.modules.main.mixins import ErrorMessagesSerializersMixin

from .helpers import contains_digits, is_age_at_least
from .models import Profile
from .services import register_user


class ProfileCreateSerializer(
    ErrorMessagesSerializersMixin, serializers.ModelSerializer
):
    avatar = HybridImageField(required=False, allow_null=True)

    default_error_messages = {
        'invalid_image': serializers.ImageField.default_error_messages.get(
            'invalid_image',
            _('The file you uploaded is corrupted or not an image.'),
        ),
        'age_less_than_fourteen': _('You are under the age of fourteen.'),
        'age_more_than_onehundred_forty': _(
            'You cannot specify an age greater than 140 years old.'
        ),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['avatar'].error_messages[
            'invalid'
        ] = self.default_error_messages.get('invalid_image')

    def validate_birthday(self, birthday: date) -> Union[date, None]:
        """Validate age greater than 14 and less than 140"""

        if not is_age_at_least(birthday, 14):
            self.fail('age_less_than_fourteen')

        if is_age_at_least(birthday, 140):
            self.fail('age_more_than_onehundred_forty')

        return birthday

    class Meta:
        model = Profile
        fields = ['avatar', 'birthday']
        extra_kwargs = {
            'birthday': {'required': True, 'allow_null': False},
        }


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


class KnoxTokenSerializer(AuthTokenSerializer):
    expiry = serializers.DateTimeField(read_only=True, label=_('Expiry'))


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


class ActivationSerializer(DjoserActivationSerializer):
    default_error_messages = {
        'stale_token': _('The token has expired.'),
        'invalid_token': _('Invalid or corrupted token.'),
        'invalid_uid': _('Invalid or corrupted UID.')
    }
