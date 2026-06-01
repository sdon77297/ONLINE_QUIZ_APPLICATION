import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import URLValidator

from ONLINE_QUIZ_APPLICATION.choices import Gender, UserRole
from ONLINE_QUIZ_APPLICATION.imports import models
from ONLINE_QUIZ_APPLICATION.validators import (
    mobile_number_validator,
    validate_image_file_extension,
)


def user_profile_image_path(instance, filename):
    return f"users/{instance.id}/profile/{filename}"


class CustomUserManager(BaseUserManager):
    """Manager that authenticates primarily with email while keeping username support."""

    use_in_migrations = True

    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address.")
        if not username:
            username = self.normalize_email(email).split("@")[0]
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        email = email or f"{username}@example.com"
        extra_fields.setdefault("role", UserRole.ADMIN)
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_verified", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=150, verbose_name="Full name")
    email = models.EmailField(unique=True, db_index=True, verbose_name="Email address")
    mobile_number = models.CharField(
        max_length=10,
        unique=True,
        validators=[mobile_number_validator],
        verbose_name="Mobile number",
    )
    profile_image = models.ImageField(
        upload_to=user_profile_image_path,
        validators=[validate_image_file_extension],
        blank=True,
        verbose_name="Profile image",
    )
    bio = models.TextField(blank=True, verbose_name="Bio")
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.STUDENT,
        db_index=True,
        verbose_name="Role",
    )
    is_verified = models.BooleanField(default=False, db_index=True, verbose_name="Verified")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    objects = CustomUserManager()

    REQUIRED_FIELDS = ["email", "full_name", "mobile_number"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-date_joined"]
        indexes = [
            models.Index(fields=["email"], name="user_email_idx"),
            models.Index(fields=["role", "is_verified"], name="user_role_verified_idx"),
        ]

    def save(self, *args, **kwargs):
        if not self.full_name:
            self.full_name = self.get_full_name() or self.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} ({self.email})"


class UserProfile(models.Model):
    user = models.OneToOneField(
        "registerpageapp.CustomUser",
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="User",
    )
    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
        blank=True,
        verbose_name="Gender",
    )
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Date of birth")
    college_name = models.CharField(max_length=180, blank=True, verbose_name="College name")
    course_name = models.CharField(max_length=120, blank=True, verbose_name="Course name")
    year_of_study = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Year of study")
    address = models.TextField(blank=True, verbose_name="Address")
    city = models.CharField(max_length=80, blank=True, db_index=True, verbose_name="City")
    state = models.CharField(max_length=80, blank=True, db_index=True, verbose_name="State")
    country = models.CharField(max_length=80, default="India", verbose_name="Country")
    linkedin_url = models.URLField(blank=True, validators=[URLValidator()], verbose_name="LinkedIn URL")
    github_url = models.URLField(blank=True, validators=[URLValidator()], verbose_name="GitHub URL")
    skills = models.JSONField(default=list, blank=True, verbose_name="Skills")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        verbose_name = "User profile"
        verbose_name_plural = "User profiles"
        ordering = ["user__full_name"]
        indexes = [
            models.Index(fields=["city", "state"], name="profile_city_state_idx"),
        ]

    def __str__(self):
        return f"Profile: {self.user.full_name}"
