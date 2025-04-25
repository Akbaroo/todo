from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(_UserAdmin):
    fieldsets = _UserAdmin.fieldsets

    fieldsets[2][1]["fields"] = (
        "is_active",
        "is_staff",
        "is_superuser",
        "is_verified",
        "verification_token",
    )


admin.site.unregister(Group)
