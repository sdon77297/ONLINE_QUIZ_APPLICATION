from django.contrib import admin

from .models import LoginHistory


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "login_time", "ip_address", "was_successful")
    list_filter = ("was_successful", "login_time")
    search_fields = ("user__email", "user__full_name", "ip_address")
    autocomplete_fields = ("user",)
    readonly_fields = ("login_time",)
