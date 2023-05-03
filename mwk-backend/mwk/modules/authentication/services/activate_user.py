from django.contrib.auth.models import User


def activate_user(user: User) -> None:
    user.is_active = True
    user.save(update_fields=['is_active'])
