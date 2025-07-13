from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields to be used in displaying the User model
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_staff",
        "date_joined",
    )
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "date_joined")

    # Fields to be used in forms
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "email")}),
        (
            "Role & Permissions",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields to be used when creating a user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("username",)
    filter_horizontal = (
        "groups",
        "user_permissions",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related()
