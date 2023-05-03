from typing import Collection, TypeVar

from django.contrib.auth.models import User

from mwk.modules.main.models.image import Image

T = TypeVar('T')


def create_images(
    images: Collection, author: User, is_update: bool = False, **filters: dict
) -> None:
    """Helper function for adding images to instance (must be obtained by filtering with **filters)"""

    if is_update and any(images):
        Image.objects.filter(**filters).delete()

    images = [Image(photo=image, author=author, **filters) for image in images]

    Image.objects.bulk_create(images)


