from django.contrib import admin

from .models import Certificate, Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "quiz", "score", "percentage", "rank", "certificate_generated", "created_at")
    list_filter = ("certificate_generated", "quiz")
    search_fields = ("student__email", "student__full_name", "quiz__quiz_title", "remarks")
    autocomplete_fields = ("student", "quiz", "attempt")
    readonly_fields = ("created_at",)


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ("certificate_id", "student", "course", "issued_date")
    search_fields = ("certificate_id", "student__email", "student__full_name", "course__course_title")
    autocomplete_fields = ("student", "course")
    readonly_fields = ("issued_date",)
