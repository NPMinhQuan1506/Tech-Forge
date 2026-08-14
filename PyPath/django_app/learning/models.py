"""Database models for the learning platform."""

from __future__ import annotations

import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import slugify


class PublishedQuerySet(models.QuerySet):
    """Reusable queryset for content visible to learners."""

    def published(self) -> "PublishedQuerySet":
        return self.filter(is_published=True)


class Lesson(models.Model):
    """A lesson that can own one or more coding exercises."""

    class Track(models.TextChoices):
        PYTHON = "python", "Python nền tảng"
        PYTHON_PRO = "python_pro", "Python chuyên sâu & Software Engineering"
        ENGINEERING = "engineering", "Nền tảng Software Engineering"
        MATH = "math", "Toán nền tảng cho AI"
        STATISTICS = "statistics", "Xác suất & Thống kê"
        DATA = "data", "Data Engineering & Analytics"
        AI = "ai", "Nền tảng AI & Dữ liệu"
        ML = "ml", "Machine Learning"
        MLOPS = "mlops", "ML Engineering & MLOps"
        DL = "dl", "Deep Learning"
        CV = "cv", "Computer Vision"
        NLP = "nlp", "NLP & Language Models"
        GENAI = "genai", "Generative AI, RAG & Agents"
        RL = "rl", "Reinforcement Learning"
        DJANGO = "django", "Django Web"
        FASTAPI = "fastapi", "FastAPI & Microservices"
        CAPSTONE = "capstone", "Capstone & Portfolio"

    class Level(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        INTERMEDIATE = "intermediate", "Intermediate"
        ADVANCED = "advanced", "Advanced"

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    curriculum_key = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        help_text="Stable key used only by the create-only starter curriculum.",
    )
    track = models.CharField(
        max_length=20,
        choices=Track.choices,
        default=Track.PYTHON,
        db_index=True,
    )
    level = models.CharField(
        max_length=20,
        choices=Level.choices,
        default=Level.BEGINNER,
    )
    summary = models.CharField(max_length=500, blank=True)
    content = models.TextField(
        help_text="Plain-text lesson body; line breaks are displayed to learners."
    )
    order = models.PositiveIntegerField(default=1)
    estimated_minutes = models.PositiveSmallIntegerField(default=25)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PublishedQuerySet.as_manager()

    class Meta:
        ordering = ("order", "title")

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Exercise(models.Model):
    """An executable Python exercise whose answer is graded by FastAPI."""

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="exercises",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=220)
    curriculum_key = models.CharField(
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        help_text="Stable key used only by the create-only starter curriculum.",
    )
    prompt = models.TextField()
    starter_code = models.TextField(blank=True)
    expected_output = models.TextField(
        help_text="Exact output expected from a correct solution."
    )
    test_input = models.TextField(
        blank=True,
        help_text="Optional standard input provided to the submitted program.",
    )
    timeout_seconds = models.PositiveSmallIntegerField(
        default=5,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Maximum sandbox execution time, from 1 to 10 seconds.",
    )
    order = models.PositiveIntegerField(default=1)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PublishedQuerySet.as_manager()

    class Meta:
        ordering = ("lesson__order", "order", "title")

    def __str__(self) -> str:
        return f"{self.lesson.title}: {self.title}"

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


def submission_upload_to(instance: "Submission", filename: str) -> str:
    """Build a traceable, collision-safe path for a submitted code image."""
    content_type = getattr(instance.image.file, "content_type", "")
    safe_suffixes = {
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
    }
    # Never preserve a user-controlled extension such as `.html`; the image
    # validators in the form/serializer ensure the bytes are a real image.
    suffix = safe_suffixes.get(content_type, ".png")
    return (
        f"submissions/user_{instance.user_id}/exercise_{instance.exercise_id}/"
        f"{instance.id}{suffix}"
    )


class Submission(models.Model):
    """A learner's image submission and its OCR/sandbox grading result."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        PASSED = "passed", "Passed"
        FAILED = "failed", "Failed"
        ERROR = "error", "Error"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_submissions",
    )
    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    image = models.ImageField(upload_to=submission_upload_to)
    extracted_code = models.TextField(blank=True)
    ocr_confidence = models.FloatField(null=True, blank=True)
    execution_output = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    grader_response = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=("user", "exercise", "-created_at"),
                name="learn_sub_user_ex_created",
            )
        ]

    def __str__(self) -> str:
        return f"{self.user} - {self.exercise} ({self.get_status_display()})"
