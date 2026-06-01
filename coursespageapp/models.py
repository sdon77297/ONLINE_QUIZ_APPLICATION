from decimal import Decimal

from ONLINE_QUIZ_APPLICATION.choices import DifficultyLevel
from ONLINE_QUIZ_APPLICATION.imports import (
    MinValueValidator,
    models,
    settings,
    slugify,
    timezone,
    validate_image_file_extension,
    validate_non_negative,
)


def category_image_path(instance, filename):
    return f"courses/categories/{instance.slug or 'draft'}/{filename}"


def course_thumbnail_path(instance, filename):
    return f"courses/thumbnails/{instance.slug or 'draft'}/{filename}"


class CourseCategory(models.Model):
    category_name = models.CharField(max_length=120, unique=True, verbose_name="Category name")
    slug = models.SlugField(max_length=140, unique=True, blank=True, verbose_name="Slug")
    category_image = models.ImageField(
        upload_to=category_image_path,
        validators=[validate_image_file_extension],
        blank=True,
        verbose_name="Category image",
    )
    description = models.TextField(blank=True, verbose_name="Description")
    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        verbose_name = "Course category"
        verbose_name_plural = "Course categories"
        ordering = ["category_name"]
        indexes = [models.Index(fields=["slug"], name="course_category_slug_idx")]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class PublishedCourseManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)


class Course(models.Model):
    course_title = models.CharField(max_length=180, default="Untitled Course", verbose_name="Course title")
    slug = models.SlugField(max_length=210, unique=True, blank=True, verbose_name="Slug")
    course_description = models.TextField(default="", verbose_name="Course description")
    short_description = models.CharField(max_length=255, blank=True, verbose_name="SEO short description")
    meta_title = models.CharField(max_length=180, blank=True, verbose_name="SEO meta title")
    meta_description = models.CharField(max_length=255, blank=True, verbose_name="SEO meta description")
    thumbnail = models.ImageField(
        upload_to=course_thumbnail_path,
        validators=[validate_image_file_extension],
        blank=True,
        verbose_name="Thumbnail",
    )
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="instructed_courses",
        verbose_name="Instructor",
    )
    category = models.ForeignKey(
        CourseCategory,
        on_delete=models.PROTECT,
        related_name="courses",
        null=True,
        blank=True,
        verbose_name="Category",
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.BEGINNER,
        db_index=True,
        verbose_name="Difficulty level",
    )
    duration = models.DurationField(null=True, blank=True, verbose_name="Course duration")
    total_quizzes = models.PositiveIntegerField(default=0, verbose_name="Total quizzes")
    total_students = models.PositiveIntegerField(default=0, verbose_name="Total students")
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00")), validate_non_negative],
        verbose_name="Price",
    )
    enrolled_students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="enrolled_courses",
        verbose_name="Enrolled students",
    )
    is_published = models.BooleanField(default=False, db_index=True, verbose_name="Published")
    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    objects = models.Manager()
    published = PublishedCourseManager()

    class Meta:
        verbose_name = "Course"
        verbose_name_plural = "Courses"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"], name="course_slug_idx"),
            models.Index(fields=["category", "difficulty_level"], name="course_cat_diff_idx"),
            models.Index(fields=["is_published", "-created_at"], name="course_pub_created_idx"),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.course_title)
        if not self.meta_title:
            self.meta_title = self.course_title[:180]
        if not self.meta_description:
            self.meta_description = (self.short_description or self.course_description[:255])[:255]
        super().save(*args, **kwargs)

    @property
    def is_free(self):
        return self.price == Decimal("0.00")

    def __str__(self):
        return self.course_title
