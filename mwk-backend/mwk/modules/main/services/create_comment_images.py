from typing import Collection

from django.contrib.auth.models import User
from mwk.modules.main.services.create_images import create_images


def create_comment_images(
    images: Collection, comment_id: int, author: User, is_update: bool = False
) -> None:
    """
    Adds images to the comment
    """

    create_images(images, author, is_update, comment_id=comment_id)
