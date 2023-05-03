from django.contrib.auth.models import User

from mwk.modules.authentication.models.profile import Profile


def setup_user_profile(attrs: dict, user: User) -> Profile:
    """
    Helper function for the 'register_user' service
    Set attrs to the user.profile if attr not None
    """

    for key in attrs:
        if not attrs.get(key) is None:
            setattr(user.profile, key, attrs.get(key))
    return user.profile
