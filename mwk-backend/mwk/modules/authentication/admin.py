from datetime import date
from typing import Union

from dateutil.relativedelta import relativedelta
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.safestring import SafeString, mark_safe
from knox.admin import AuthTokenAdmin
from knox.models import AuthToken

from mwk.modules.authentication.models.contact import Contact
from mwk.modules.authentication.models.custom_auth_token import CustomAuthToken
from mwk.modules.authentication.models.profile import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'created_at',
        'get_status',
        'get_years_old',
        'get_avatar',
    ]
    list_display_links = ['id', 'user']
    search_fields = ['user__username', 'id']
    list_select_related = ['user']
    fields = [
        'id',
        'user',
        'bio',
        'avatar',
        'get_avatar',
        'birthday',
        'created_at',
    ]
    readonly_fields = ['id', 'get_avatar', 'created_at']
    autocomplete_fields = ['user']

    def get_avatar(self, obj: Profile) -> Union[SafeString, str]:
        if obj.avatar:
            return mark_safe(f'<img src="{obj.avatar.url}" height="40" width="40">')

        else:
            return '-'

    get_avatar.short_description = 'Avatar'

    def get_status(self, obj: Profile) -> str:
        return obj.bio if obj.bio else '-'

    get_status.short_description = 'Status'

    def get_years_old(self, obj: Profile) -> Union[int, str]:
        if not obj.birthday:
            return '-'

        today = date.today()
        years_old = relativedelta(today, obj.birthday).years

        return years_old

    get_years_old.short_description = 'Full years'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user_from_get_full_name',
        'user_to_get_full_name',
        'created_at',
    ]
    list_display_links = ['id', 'user_from_get_full_name', 'user_to_get_full_name']
    search_fields = ['id', 'user_from__username', 'user_to__username']
    empty_value_display = '-'
    ordering = ['-created_at']
    fields = ['id', 'user_from', 'user_to', 'created_at']
    readonly_fields = ['id', 'created_at']
    list_select_related = ['user_from', 'user_to']
    autocomplete_fields = ['user_from', 'user_to']

    def get_full_name(self, user: User) -> str:
        return f'{user.first_name} {user.last_name}'

    def user_from_get_full_name(self, obj: Contact) -> str:
        return self.get_full_name(obj.user_from.user)

    user_from_get_full_name.short_description = 'From'

    def user_to_get_full_name(self, obj: Contact):
        return self.get_full_name(obj.user_to.user)

    user_to_get_full_name.short_description = 'To'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('user_from__user', 'user_to__user')


@admin.register(CustomAuthToken)
class TokenAdmin(AuthTokenAdmin):
    pass


admin.site.unregister(AuthToken)
