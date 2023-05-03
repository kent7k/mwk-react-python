from django.contrib.auth.models import User
from django.db import transaction

from mwk.modules.authentication.services.setup_user_profile import setup_user_profile


@transaction.atomic
def register_user(user_data: dict, password: str, user_profile_data: dict) -> User:
    user: User = User.objects.create_user(**user_data, password=password, is_active=False)
    profile = setup_user_profile(user_profile_data, user)
    profile.save()
    return user
