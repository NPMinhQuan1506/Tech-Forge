"""Add curriculum metadata while preserving existing seeded content."""

from django.db import migrations, models


def assign_legacy_curriculum_keys(apps, schema_editor) -> None:
    """Associate the first starter records with their stable curriculum keys."""
    Lesson = apps.get_model("learning", "Lesson")
    Exercise = apps.get_model("learning", "Exercise")

    Lesson.objects.filter(
        curriculum_key__isnull=True,
        slug="python-print",
    ).update(curriculum_key="python-01-print")
    Exercise.objects.filter(
        curriculum_key__isnull=True,
        slug="print-hello-python",
    ).update(curriculum_key="python-01-print-greeting")


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="lesson",
            name="curriculum_key",
            field=models.CharField(
                blank=True,
                help_text="Stable key used only by the create-only starter curriculum.",
                max_length=100,
                null=True,
                unique=True,
            ),
        ),
        migrations.AddField(
            model_name="lesson",
            name="estimated_minutes",
            field=models.PositiveSmallIntegerField(default=25),
        ),
        migrations.AddField(
            model_name="lesson",
            name="level",
            field=models.CharField(
                choices=[
                    ("beginner", "Beginner"),
                    ("intermediate", "Intermediate"),
                    ("advanced", "Advanced"),
                ],
                default="beginner",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="lesson",
            name="track",
            field=models.CharField(
                choices=[
                    ("python", "Python nền tảng"),
                    ("ai", "Nền tảng AI & Dữ liệu"),
                    ("ml", "Machine Learning"),
                    ("dl", "Deep Learning"),
                    ("django", "Django Web"),
                    ("fastapi", "FastAPI & Microservices"),
                ],
                db_index=True,
                default="python",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="exercise",
            name="curriculum_key",
            field=models.CharField(
                blank=True,
                help_text="Stable key used only by the create-only starter curriculum.",
                max_length=100,
                null=True,
                unique=True,
            ),
        ),
        migrations.RunPython(
            assign_legacy_curriculum_keys,
            migrations.RunPython.noop,
        ),
    ]
