import os
from datetime import datetime
from typing import Any, Collection, Iterable
from uuid import uuid4

from django.forms.fields import ImageField as ImageFieldValidator
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _
from rest_framework import serializers


@deconstructible
class PathWithDateAndUUID:
    """
    A class used to add the current year and month to the source path and rename the file to a uuid4.
    """

    def __init__(self, sub_path: str) -> None:
        self.path = sub_path

    def __call__(self, instance: Any, filename: str) -> str:
        ext = filename.split('.')[-1]
        filename = f'{uuid4().hex}.{ext}'

        date_path = os.path.join(self.path, f'{datetime.now().year}/{datetime.now().month}')
        full_path = os.path.join(date_path, filename)

        return full_path


def validate_images(images: Collection[bytes]):
    if not any(images):
        return

    if len(images) > 10:
        raise serializers.ValidationError(
            detail={'max_file_length': _('The number of files is invalid, maximum number of files allowed: 10')},
            code='max_file_length',
        )

    for image in images:
        if image.size / 1024 / 1024 > 8:
            raise serializers.ValidationError({'file_too_large': _('The file you uploaded is too large.')}, code='file_too_large')
        ImageFieldValidator().to_python(image)
