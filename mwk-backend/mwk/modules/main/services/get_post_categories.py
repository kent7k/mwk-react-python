from mwk.modules.main.models.post_category import PostCategory


def get_post_categories() -> list[PostCategory]:
    return PostCategory.objects.all()
