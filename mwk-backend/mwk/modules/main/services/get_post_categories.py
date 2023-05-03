from mwk.modules.main.models.post_category import PostCategory


def get_post_categories() -> list[PostCategory]:
    """Get post categories"""

    categories = PostCategory.objects.all()

    return categories
