# Generated manually for the initial learning-platform schema.

import uuid

import django.core.validators
import django.db.models.deletion
import learning.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Lesson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=220, unique=True)),
                ("summary", models.CharField(blank=True, max_length=500)),
                (
                    "content",
                    models.TextField(
                        help_text="Plain-text lesson body; line breaks are displayed to learners."
                    ),
                ),
                ("order", models.PositiveIntegerField(default=1)),
                ("is_published", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ("order", "title")},
        ),
        migrations.CreateModel(
            name="Exercise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=220, unique=True)),
                ("prompt", models.TextField()),
                ("starter_code", models.TextField(blank=True)),
                (
                    "expected_output",
                    models.TextField(help_text="Exact output expected from a correct solution."),
                ),
                (
                    "test_input",
                    models.TextField(
                        blank=True,
                        help_text="Optional standard input provided to the submitted program.",
                    ),
                ),
                (
                    "timeout_seconds",
                    models.PositiveSmallIntegerField(
                        default=5,
                        help_text="Maximum sandbox execution time, from 1 to 10 seconds.",
                        validators=[
                            django.core.validators.MinValueValidator(1),
                            django.core.validators.MaxValueValidator(10),
                        ],
                    ),
                ),
                ("order", models.PositiveIntegerField(default=1)),
                ("is_published", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "lesson",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exercises",
                        to="learning.lesson",
                    ),
                ),
            ],
            options={"ordering": ("lesson__order", "order", "title")},
        ),
        migrations.CreateModel(
            name="Submission",
            fields=[
                (
                    "id",
                    models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
                ),
                (
                    "image",
                    models.ImageField(upload_to=learning.models.submission_upload_to),
                ),
                ("extracted_code", models.TextField(blank=True)),
                ("ocr_confidence", models.FloatField(blank=True, null=True)),
                ("execution_output", models.TextField(blank=True)),
                ("error_message", models.TextField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "Pending"),
                            ("processing", "Processing"),
                            ("passed", "Passed"),
                            ("failed", "Failed"),
                            ("error", "Error"),
                        ],
                        db_index=True,
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("grader_response", models.JSONField(blank=True, default=dict)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "exercise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="submissions",
                        to="learning.exercise",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="learning_submissions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("-created_at",),
                "indexes": [
                    models.Index(
                        fields=["user", "exercise", "-created_at"],
                        name="learn_sub_user_ex_created",
                    )
                ],
            },
        ),
    ]
