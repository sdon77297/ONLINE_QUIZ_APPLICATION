from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "username", "full_name", "mobile_number", "role", "is_verified", "is_staff")
    list_filter = ("role", "is_verified", "is_staff", "is_active")
    search_fields = ("email", "username", "full_name", "mobile_number")
    ordering = ("-date_joined",)
    readonly_fields = ("created_at", "updated_at", "date_joined", "last_login")
    fieldsets = UserAdmin.fieldsets + (
        ("QuizCraft profile", {"fields": ("full_name", "mobile_number", "profile_image", "bio", "role", "is_verified")}),
        ("Timestamps", {"fields": ("created_at", "updated_at")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Required details", {"fields": ("full_name", "email", "mobile_number", "role")}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "college_name", "course_name", "city", "state", "country")
    search_fields = ("user__email", "user__full_name", "college_name", "city", "skills")
    list_filter = ("gender", "city", "state", "country")
    autocomplete_fields = ("user",)
