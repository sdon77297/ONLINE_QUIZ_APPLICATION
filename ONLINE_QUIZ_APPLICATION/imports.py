from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator, URLValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from .choices import (
    AttemptStatus,
    DifficultyLevel,
    Gender,
    NotificationType,
    QuestionType,
    QuizType,
    UserRole,
)
from .validators import (
    mobile_number_validator,
    validate_image_file_extension,
    validate_non_negative,
    validate_pdf_file_extension,
)

__all__ = [
    "settings",
    "models",
    "reverse",
    "timezone",
    "slugify",
    "MaxValueValidator",
    "MinValueValidator",
    "URLValidator",
    "AttemptStatus",
    "DifficultyLevel",
    "Gender",
    "NotificationType",
    "QuestionType",
    "QuizType",
    "UserRole",
    "mobile_number_validator",
    "validate_image_file_extension",
    "validate_non_negative",
    "validate_pdf_file_extension",
]
