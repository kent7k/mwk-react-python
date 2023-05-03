from typing import Collection

from django.contrib.auth.models import User
from mwk.modules.main.services.save_images_to_database import save_images_to_database


def add_images_to_comment(
    images: Collection, comment_id: int, author: User, is_updated: bool = False
) -> None:
    """
    Adds images to the comment
    """

    save_images_to_database(images, author, is_updated, comment_id=comment_id)
