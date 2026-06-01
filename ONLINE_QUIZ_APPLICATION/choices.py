from django.db import models


class UserRole(models.TextChoices):
    STUDENT = "student", "Student"
    ADMIN = "admin", "Admin"
    INSTRUCTOR = "instructor", "Instructor"


class Gender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"
    OTHER = "other", "Other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say", "Prefer not to say"


class DifficultyLevel(models.TextChoices):
    BEGINNER = "beginner", "Beginner"
    INTERMEDIATE = "intermediate", "Intermediate"
    ADVANCED = "advanced", "Advanced"


class QuizType(models.TextChoices):
    PRACTICE = "practice", "Practice"
    MOCK_TEST = "mock_test", "Mock Test"
    SCHEDULED = "scheduled", "Scheduled"
    RANDOM = "random", "Random"


class QuestionType(models.TextChoices):
    SINGLE_CHOICE = "single_choice", "Single Choice"
    MULTIPLE_CHOICE = "multiple_choice", "Multiple Choice"
    TRUE_FALSE = "true_false", "True / False"
    IMAGE_BASED = "image_based", "Image Based"


class AttemptStatus(models.TextChoices):
    IN_PROGRESS = "in_progress", "In Progress"
    SUBMITTED = "submitted", "Submitted"
    EXPIRED = "expired", "Expired"
    CANCELLED = "cancelled", "Cancelled"


class NotificationType(models.TextChoices):
    INFO = "info", "Info"
    SUCCESS = "success", "Success"
    WARNING = "warning", "Warning"
    QUIZ = "quiz", "Quiz"
    RESULT = "result", "Result"
