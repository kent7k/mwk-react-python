from django.contrib.auth.models import User
from django.db import transaction

from mwk.modules.authentication.services.update_user_profile import update_user_profile


@transaction.atomic
def register_user(user_data: dict, password: str, profile_data: dict) -> User:
    user = User.objects.create_user(**user_data, password=password, is_active=True)
    if profile_data is not None:
        update_user_profile(profile_data, user)
    return user
