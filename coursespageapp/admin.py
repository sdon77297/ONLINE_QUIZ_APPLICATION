from django.contrib import admin

from .models import Course, CourseCategory


@admin.register(CourseCategory)
class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ("category_name", "slug", "created_at")
    search_fields = ("category_name", "description")
    prepopulated_fields = {"slug": ("category_name",)}
    readonly_fields = ("created_at", "updated_at")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_title", "category", "instructor", "difficulty_level", "price", "is_published")
    list_filter = ("category", "difficulty_level", "is_published")
    search_fields = ("course_title", "course_description", "instructor__email")
    prepopulated_fields = {"slug": ("course_title",)}
    autocomplete_fields = ("instructor", "category", "enrolled_students")
    readonly_fields = ("created_at", "updated_at", "total_quizzes", "total_students")
