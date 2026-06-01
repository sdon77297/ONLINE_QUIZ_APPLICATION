from ONLINE_QUIZ_APPLICATION.imports import models


class HomePage(models.Model):
    site_title = models.CharField(max_length=200, verbose_name="Site title")
    hero_title = models.CharField(max_length=255, verbose_name="Hero title")
    hero_subtitle = models.TextField(verbose_name="Hero subtitle")
    total_courses = models.PositiveIntegerField(default=0, verbose_name="Total courses")
    total_quizzes = models.PositiveIntegerField(default=0, verbose_name="Total quizzes")
    total_students = models.PositiveIntegerField(default=0, verbose_name="Total students")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Active")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        verbose_name = "Homepage content"
        verbose_name_plural = "Homepage content"
        ordering = ["-created_at"]

    def __str__(self):
        return self.site_title


class ContactFeedback(models.Model):
    name = models.CharField(max_length=120, verbose_name="Name")
    email = models.EmailField(db_index=True, verbose_name="Email")
    subject = models.CharField(max_length=180, verbose_name="Subject")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Contact feedback"
        verbose_name_plural = "Contact feedback"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["email", "-created_at"], name="feedback_email_created_idx")]

    def __str__(self):
        return f"{self.name} - {self.subject}"
