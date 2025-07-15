from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "assigned_to",
        "status",
        "deadline",
        "created_at",
        "is_overdue",
    ]
    list_filter = ["status", "assigned_to", "deadline", "created_at"]
    search_fields = [
        "title",
        "description",
        "assigned_to__username",
    ]
    readonly_fields = ["created_at"]

    fieldsets = (
        ("Task Information", {"fields": ("title", "description", "status")}),
        ("Assignment", {"fields": ("assigned_to", "deadline")}),
        (
            "Timestamps",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        elif request.user.is_admin:
            return qs.filter(created_by=request.user)
        else:
            return qs.filter(assigned_to=request.user)

    def has_add_permission(self, request):
        return request.user.is_superuser or request.user.is_admin

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_admin:
            return obj is None
        return False

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        if request.user.is_admin:
            return obj is None
        return False
