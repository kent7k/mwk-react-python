from typing import Collection, TypeVar

from django.contrib.auth.models import User

from mwk.modules.main.services.create_images import create_images


def create_post_images(
    images: Collection, post_id: int, author: User, is_update: bool = False
) -> None:
    """
    Adds images to the post
    """

    create_images(images, author, is_update, post_id=post_id)
