from django.contrib.auth import get_user_model

from mwk.modules.authentication.models.profile import Profile


def update_user_profile(profile_attrs: dict, user: get_user_model()) -> Profile:
    profile = user.profile

    for attr, value in profile_attrs.items():
        if value is not None:
            setattr(profile, attr, value)

    profile.save()
    return profile

