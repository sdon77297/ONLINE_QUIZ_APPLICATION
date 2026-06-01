from django.contrib import admin

from .models import Option, Question, Quiz, QuizAttempt, StudentAnswer


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("quiz_title", "course", "quiz_type", "difficulty_level", "total_marks", "duration_minutes", "is_active")
    list_filter = ("quiz_type", "difficulty_level", "is_active", "course")
    search_fields = ("quiz_title", "quiz_description", "course__course_title")
    autocomplete_fields = ("course", "created_by")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "quiz", "question_type", "difficulty", "marks")
    list_filter = ("question_type", "difficulty", "quiz")
    search_fields = ("question_text", "explanation", "quiz__quiz_title")
    autocomplete_fields = ("quiz",)
    inlines = [OptionInline]
    readonly_fields = ("created_at", "updated_at")


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("option_text", "question", "is_correct")
    list_filter = ("is_correct",)
    search_fields = ("option_text", "question__question_text")
    autocomplete_fields = ("question",)


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("student", "quiz", "score", "percentage", "status", "started_at", "submitted_at")
    list_filter = ("status", "quiz")
    search_fields = ("student__email", "student__full_name", "quiz__quiz_title")
    autocomplete_fields = ("student", "quiz")
    readonly_fields = ("percentage", "started_at")


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ("attempt", "question", "selected_option", "is_correct", "answered_at")
    list_filter = ("is_correct",)
    search_fields = ("attempt__student__email", "question__question_text")
    autocomplete_fields = ("attempt", "question", "selected_option")
