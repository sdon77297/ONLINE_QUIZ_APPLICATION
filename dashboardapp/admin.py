from django.contrib import admin

from .models import DashboardActivity, Notification


@admin.register(DashboardActivity)
class DashboardActivityAdmin(admin.ModelAdmin):
    list_display = ("user", "activity_name", "activity_date")
    search_fields = ("user__email", "user__full_name", "activity_name")
    autocomplete_fields = ("user",)
    readonly_fields = ("activity_date",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "notification_type", "is_read", "created_at")
    list_filter = ("notification_type", "is_read")
    search_fields = ("title", "message", "user__email", "user__full_name")
    autocomplete_fields = ("user",)
    readonly_fields = ("created_at",)
