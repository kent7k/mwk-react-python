from django.contrib.auth.models import User

from mwk.modules.authentication.services.setup_user_profile import setup_user_profile


def register_user(user_data: dict, password: str, user_profile_data: dict) -> User:
    user: User = User.objects.create_user(**user_data)
    user.set_password(password)
    user.is_active = False

    profile = setup_user_profile(user_profile_data, user)

    user.save()
    profile.save()

    return user
