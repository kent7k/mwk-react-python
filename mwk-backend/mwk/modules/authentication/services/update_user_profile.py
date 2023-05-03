from django.contrib.auth import get_user_model

from mwk.modules.authentication.models.profile import Profile


def update_user_profile(attrs: dict, user: get_user_model()) -> Profile:
    profile = user.profile

    for key, value in attrs.items():
        if value is not None:
            setattr(profile, key, value)

    profile.save()
    return profile

