from django.contrib import admin
from django.contrib.admin import site, ModelAdmin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import ugettext_lazy

from .models import User, Member

DEFAULT_READONLY_FIELDS = ("created_at", "updated_at")


# Customize Admin site
site.site_title = ugettext_lazy("UWCNC Admin")
site.site_header = ugettext_lazy("UWCNC Administration")
site.index_title = ugettext_lazy("Backend administration console")


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    readonly_fields = DEFAULT_READONLY_FIELDS


@admin.register(Member)
class MemberAdmin(ModelAdmin):
    readonly_fields = DEFAULT_READONLY_FIELDS
