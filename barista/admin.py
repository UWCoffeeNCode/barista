from django.contrib import admin
from django.contrib.admin import site
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy

from .models import User

DEFAULT_READONLY_FIELDS = ("created_at", "updated_at")


# Customize Admin site
site.site_title = ugettext_lazy("Barista")
site.site_header = ugettext_lazy("Barista")
site.index_title = ugettext_lazy("UWCNC Admin Console")


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    readonly_fields = DEFAULT_READONLY_FIELDS

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_verified",
        "is_staff",
    )
    list_filter = ("is_verified", "is_active", "is_superuser", "is_staff", "groups")

    fieldsets = (
        (
            None,
            {
                "fields": ("username", "password"),
            },
        ),
        (
            "Personal info",
            {
                "fields": ("first_name", "last_name", "email"),
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_verified",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            "Important dates",
            {
                "fields": ("last_login", "date_joined"),
            },
        ),
    )
