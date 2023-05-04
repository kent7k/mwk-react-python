from datetime import date
from typing import Union

from django.utils.translation import gettext as _
from drf_extra_fields.fields import HybridImageField
from rest_framework import serializers

from mwk.modules.main.mixins.error_messages_serializers_mixin import ErrorMessagesSerializersMixin

from mwk.modules.authentication.helpers import contains_digits, is_age_at_least
from mwk.modules.authentication.models.profile import Profile


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
            'birthday': {'required': False, 'allow_null': True},
        }
