import uuid

from ONLINE_QUIZ_APPLICATION.choices import (
    AttemptStatus,
    DifficultyLevel,
    QuestionType,
    QuizType,
)
from ONLINE_QUIZ_APPLICATION.imports import (
    MaxValueValidator,
    MinValueValidator,
    models,
    settings,
    validate_image_file_extension,
)


def question_image_path(instance, filename):
    return f"quizzes/questions/{instance.quiz_id}/{filename}"


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(
        "coursespageapp.Course",
        on_delete=models.CASCADE,
        related_name="quizzes",
        null=True,
        blank=True,
        verbose_name="Course",
    )
    quiz_title = models.CharField(max_length=180, default="Untitled Quiz", verbose_name="Quiz title")
    quiz_description = models.TextField(blank=True, verbose_name="Quiz description")
    total_questions = models.PositiveIntegerField(default=0, verbose_name="Total questions")
    total_marks = models.PositiveIntegerField(default=0, verbose_name="Total marks")
    passing_marks = models.PositiveIntegerField(default=0, verbose_name="Passing marks")
    duration_minutes = models.PositiveIntegerField(default=30, verbose_name="Duration in minutes")
    start_time = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name="Start time")
    end_time = models.DateTimeField(null=True, blank=True, db_index=True, verbose_name="End time")
    quiz_type = models.CharField(
        max_length=20,
        choices=QuizType.choices,
        default=QuizType.PRACTICE,
        db_index=True,
        verbose_name="Quiz type",
    )
    difficulty_level = models.CharField(
        max_length=20,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.BEGINNER,
        db_index=True,
        verbose_name="Difficulty level",
    )
    randomize_questions = models.BooleanField(default=False, verbose_name="Randomize questions")
    is_active = models.BooleanField(default=True, db_index=True, verbose_name="Active")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_quizzes",
        verbose_name="Created by",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["course", "is_active"], name="quiz_course_active_idx"),
            models.Index(fields=["quiz_type", "difficulty_level"], name="quiz_type_diff_idx"),
        ]

    @property
    def title(self):
        return self.quiz_title

    @property
    def description(self):
        return self.quiz_description

    @property
    def duration(self):
        return self.duration_minutes

    def __str__(self):
        return self.quiz_title


class Question(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Quiz",
    )
    question_text = models.TextField(verbose_name="Question text")
    question_image = models.ImageField(
        upload_to=question_image_path,
        validators=[validate_image_file_extension],
        blank=True,
        verbose_name="Question image",
    )
    question_type = models.CharField(
        max_length=25,
        choices=QuestionType.choices,
        default=QuestionType.SINGLE_CHOICE,
        verbose_name="Question type",
    )
    marks = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)], verbose_name="Marks")
    difficulty = models.CharField(
        max_length=20,
        choices=DifficultyLevel.choices,
        default=DifficultyLevel.BEGINNER,
        db_index=True,
        verbose_name="Difficulty",
    )
    explanation = models.TextField(blank=True, verbose_name="Explanation")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["quiz", "difficulty"], name="question_quiz_diff_idx"),
        ]

    def __str__(self):
        return self.question_text[:80]


class Option(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name="Question",
    )
    option_text = models.CharField(max_length=500, verbose_name="Option text")
    is_correct = models.BooleanField(default=False, db_index=True, verbose_name="Correct option")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")

    class Meta:
        verbose_name = "Option"
        verbose_name_plural = "Options"
        ordering = ["id"]
        indexes = [models.Index(fields=["question", "is_correct"], name="option_question_correct_idx")]

    def __str__(self):
        return self.option_text[:80]


class QuizAttempt(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
        verbose_name="Student",
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Quiz",
    )
    score = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name="Score")
    total_correct = models.PositiveIntegerField(default=0, verbose_name="Total correct")
    total_wrong = models.PositiveIntegerField(default=0, verbose_name="Total wrong")
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Percentage",
    )
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Started at")
    submitted_at = models.DateTimeField(null=True, blank=True, verbose_name="Submitted at")
    time_taken = models.DurationField(null=True, blank=True, verbose_name="Time taken")
    status = models.CharField(
        max_length=20,
        choices=AttemptStatus.choices,
        default=AttemptStatus.IN_PROGRESS,
        db_index=True,
        verbose_name="Status",
    )

    class Meta:
        verbose_name = "Quiz attempt"
        verbose_name_plural = "Quiz attempts"
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["student", "quiz", "-started_at"], name="attempt_student_quiz_idx"),
            models.Index(fields=["status"], name="attempt_status_idx"),
        ]

    def calculate_percentage(self):
        if not self.quiz or not self.quiz.total_marks:
            return 0
        return round((float(self.score) / self.quiz.total_marks) * 100, 2)

    def save(self, *args, **kwargs):
        self.percentage = self.calculate_percentage()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student} - {self.quiz} ({self.percentage}%)"


class StudentAnswer(models.Model):
    attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Attempt",
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name="student_answers",
        verbose_name="Question",
    )
    selected_option = models.ForeignKey(
        Option,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_answers",
        verbose_name="Selected option",
    )
    is_correct = models.BooleanField(default=False, db_index=True, verbose_name="Correct")
    answered_at = models.DateTimeField(auto_now_add=True, verbose_name="Answered at")

    class Meta:
        verbose_name = "Student answer"
        verbose_name_plural = "Student answers"
        ordering = ["answered_at"]
        constraints = [
            models.UniqueConstraint(fields=["attempt", "question"], name="unique_answer_per_attempt_question"),
        ]
        indexes = [models.Index(fields=["attempt", "is_correct"], name="answer_attempt_correct_idx")]

    def save(self, *args, **kwargs):
        self.is_correct = bool(self.selected_option and self.selected_option.is_correct)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.attempt} - {self.question}"
