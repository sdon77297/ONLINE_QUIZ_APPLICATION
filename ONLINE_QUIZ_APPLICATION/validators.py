from pathlib import Path

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


mobile_number_validator = RegexValidator(
    regex=r"^[6-9]\d{9}$",
    message="Enter a valid 10 digit Indian mobile number.",
)


def validate_image_file_extension(value):
    extension = Path(value.name).suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp"}:
        raise ValidationError("Only JPG, PNG, JPEG, and WEBP images are allowed.")


def validate_pdf_file_extension(value):
    extension = Path(value.name).suffix.lower()
    if extension != ".pdf":
        raise ValidationError("Only PDF files are allowed.")


def validate_non_negative(value):
    if value < 0:
        raise ValidationError("This value cannot be negative.")
