from django.contrib.auth.models import User

from mwk.modules.authentication.models.profile import Profile


def update_user_profile(attrs: dict, user: User) -> Profile:
    for key, value in attrs.items():
        if value is not None:
            setattr(user.profile, key, value)
    user.profile.save()
    return user.profile
