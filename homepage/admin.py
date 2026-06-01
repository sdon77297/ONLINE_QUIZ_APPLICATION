from django.contrib import admin

from .models import ContactFeedback, HomePage


@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin):
    list_display = ("site_title", "is_active", "total_courses", "total_quizzes", "total_students", "created_at")
    list_filter = ("is_active",)
    search_fields = ("site_title", "hero_title", "hero_subtitle")
    readonly_fields = ("created_at", "updated_at")


@admin.register(ContactFeedback)
class ContactFeedbackAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("created_at",)
