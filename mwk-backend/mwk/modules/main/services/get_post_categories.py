from typing import List

from mwk.modules.main.models.post_category import PostCategory


def get_post_categories() -> List[PostCategory]:
    return list(PostCategory.objects.all())
