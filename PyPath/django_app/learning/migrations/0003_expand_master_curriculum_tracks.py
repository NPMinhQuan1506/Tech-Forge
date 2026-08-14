"""Record the expanded Master Python and AI curriculum track choices."""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("learning", "0002_curriculum_metadata"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lesson",
            name="track",
            field=models.CharField(
                choices=[
                    ("python", "Python nền tảng"),
                    ("python_pro", "Python chuyên sâu & Software Engineering"),
                    ("engineering", "Nền tảng Software Engineering"),
                    ("math", "Toán nền tảng cho AI"),
                    ("statistics", "Xác suất & Thống kê"),
                    ("data", "Data Engineering & Analytics"),
                    ("ai", "Nền tảng AI & Dữ liệu"),
                    ("ml", "Machine Learning"),
                    ("mlops", "ML Engineering & MLOps"),
                    ("dl", "Deep Learning"),
                    ("cv", "Computer Vision"),
                    ("nlp", "NLP & Language Models"),
                    ("genai", "Generative AI, RAG & Agents"),
                    ("rl", "Reinforcement Learning"),
                    ("django", "Django Web"),
                    ("fastapi", "FastAPI & Microservices"),
                    ("capstone", "Capstone & Portfolio"),
                ],
                db_index=True,
                default="python",
                max_length=20,
            ),
        ),
    ]
