from typing import Collection, TypeVar, Dict

from django.contrib.auth.models import User

from mwk.modules.main.models.image import Image

QuerySetType = TypeVar('QuerySetType', bound='QuerySet')


def save_images(images: Collection, author: User, is_updated: bool = False, **filters: Dict) -> None:
    """
    Save a collection of images to the database.

    Args:
        images (Collection): The images to be saved.
        author (User): The user who uploaded the images.
        is_updated (bool): Whether the images are being updated or not.
        filters (dict): Filters to apply when querying the images to be updated.
    """

    if is_updated:
        Image.objects.filter(**filters).delete()

    image_objects = [Image(photo=image, author=author, **filters) for image in images]

    Image.objects.bulk_create(image_objects)
