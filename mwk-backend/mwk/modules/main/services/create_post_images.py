from typing import Collection, TypeVar

from django.contrib.auth.models import User

from mwk.modules.main.services.save_images_to_database import save_images_to_database


def create_post_images(
    images: Collection, post_id: int, author: User, is_updated: bool = False
) -> None:
    """
    Adds images to the post
    """

    save_images_to_database(images, author, is_updated, post_id=post_id)
