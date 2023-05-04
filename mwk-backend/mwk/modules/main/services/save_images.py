from typing import Iterable

from django.contrib.auth.models import User

from mwk.modules.main.models.image import Image


def save_images(images: Iterable[bytes], author: User, is_update: bool = False, **filters) -> None:
    """Helper function for adding images to Image model based on provided filters"""

    # Delete images if update flag is set to True
    if is_update:
        Image.objects.filter(**filters).delete()

    # Create Image instances for each image and save to database
    image_instances = [Image(photo=image, author=author, **filters) for image in images]
    Image.objects.bulk_create(image_instances)
