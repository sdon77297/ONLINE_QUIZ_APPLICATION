import uuid

from ONLINE_QUIZ_APPLICATION.imports import (
    MaxValueValidator,
    MinValueValidator,
    models,
    settings,
    timezone,
    validate_pdf_file_extension,
)


def certificate_file_path(instance, filename):
    return f"certificates/{instance.student_id}/{instance.certificate_id}/{filename}"


class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name="Student",
    )
    quiz = models.ForeignKey(
        "quizpageapp.Quiz",
        on_delete=models.CASCADE,
        related_name="results",
        verbose_name="Quiz",
    )
    attempt = models.OneToOneField(
        "quizpageapp.QuizAttempt",
        on_delete=models.CASCADE,
        related_name="result",
        null=True,
        blank=True,
        verbose_name="Attempt",
    )
    rank = models.PositiveIntegerField(null=True, blank=True, db_index=True, verbose_name="Rank")
    score = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Score")
    total_marks = models.PositiveIntegerField(default=0, verbose_name="Total marks")
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Percentage",
    )
    remarks = models.CharField(max_length=255, blank=True, verbose_name="Remarks")
    certificate_generated = models.BooleanField(default=False, verbose_name="Certificate generated")
    created_at = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Created at")

    class Meta:
        verbose_name = "Result"
        verbose_name_plural = "Results"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["student", "-created_at"], name="result_student_created_idx"),
            models.Index(fields=["quiz", "rank"], name="result_quiz_rank_idx"),
        ]

    @property
    def submitted_at(self):
        return self.created_at

    @property
    def status(self):
        return "Pass" if self.percentage >= 40 else "Needs Improvement"

    def save(self, *args, **kwargs):
        if self.attempt:
            self.score = self.attempt.score
            self.percentage = self.attempt.percentage
            self.total_marks = self.attempt.quiz.total_marks
        elif self.total_marks:
            self.percentage = round((float(self.score) / self.total_marks) * 100, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.quiz} - {self.percentage}%"


class Certificate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="certificates",
        verbose_name="Student",
    )
    course = models.ForeignKey(
        "coursespageapp.Course",
        on_delete=models.CASCADE,
        related_name="certificates",
        verbose_name="Course",
    )
    certificate_id = models.CharField(max_length=40, unique=True, db_index=True, verbose_name="Certificate ID")
    issued_date = models.DateTimeField(auto_now_add=True, verbose_name="Issued date")
    certificate_file = models.FileField(
        upload_to=certificate_file_path,
        validators=[validate_pdf_file_extension],
        blank=True,
        verbose_name="Certificate PDF",
    )

    class Meta:
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"
        ordering = ["-issued_date"]
        constraints = [
            models.UniqueConstraint(fields=["student", "course"], name="unique_certificate_per_student_course"),
        ]
        indexes = [models.Index(fields=["student", "-issued_date"], name="cert_student_issued_idx")]

    def save(self, *args, **kwargs):
        if not self.certificate_id:
            short_uuid = uuid.uuid4().hex[:10].upper()
            self.certificate_id = f"QC-{short_uuid}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.certificate_id} - {self.student}"
