from typing import Collection

from django.contrib.auth.models import User
from mwk.modules.main.services.save_images import save_images


def add_images_to_post(images: Collection, post_id: int, author: User, is_updated: bool = False):
    save_images(images, author, is_updated, post_id=post_id)
