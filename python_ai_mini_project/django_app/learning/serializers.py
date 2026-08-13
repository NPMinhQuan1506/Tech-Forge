"""REST serializers for public learning content and private submissions."""

from rest_framework import serializers

from .models import Exercise, Lesson, Submission
from .services import grade_submission


class ExerciseSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ("id", "title", "slug", "prompt", "order")


class LessonSerializer(serializers.ModelSerializer):
    exercises = ExerciseSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = (
            "id",
            "title",
            "slug",
            "track",
            "level",
            "summary",
            "content",
            "order",
            "estimated_minutes",
            "exercises",
        )


class ExerciseSerializer(serializers.ModelSerializer):
    lesson = serializers.SlugRelatedField(read_only=True, slug_field="slug")

    class Meta:
        model = Exercise
        fields = (
            "id",
            "lesson",
            "title",
            "slug",
            "prompt",
            "starter_code",
            "test_input",
            "timeout_seconds",
            "order",
        )


class SubmissionSerializer(serializers.ModelSerializer):
    exercise = ExerciseSummarySerializer(read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Submission
        fields = (
            "id",
            "username",
            "exercise",
            "image",
            "extracted_code",
            "ocr_confidence",
            "execution_output",
            "error_message",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = fields


class SubmissionCreateSerializer(serializers.ModelSerializer):
    """Accept a photo and synchronously persist the FastAPI grading outcome."""

    max_image_size = 5 * 1024 * 1024
    allowed_content_types = {"image/jpeg", "image/png", "image/webp"}

    class Meta:
        model = Submission
        fields = ("exercise", "image")

    def validate_exercise(self, exercise: Exercise) -> Exercise:
        if not exercise.is_published or not exercise.lesson.is_published:
            raise serializers.ValidationError(
                "This exercise is not available for submission."
            )
        return exercise

    def validate_image(self, image):
        content_type = getattr(image, "content_type", "")
        if content_type and content_type not in self.allowed_content_types:
            raise serializers.ValidationError(
                "Only PNG, JPEG, and WebP images are supported."
            )
        if image.size > self.max_image_size:
            raise serializers.ValidationError("The image must be 5 MB or smaller.")
        return image

    def create(self, validated_data: dict) -> Submission:
        user = self.context["request"].user
        submission = Submission.objects.create(user=user, **validated_data)
        return grade_submission(submission)


class CodeRunSerializer(serializers.Serializer):
    """Validate browser sandbox input before Django calls FastAPI."""

    code = serializers.CharField(
        allow_blank=False,
        max_length=50_000,
        trim_whitespace=False,
    )
    stdin = serializers.CharField(
        allow_blank=True,
        max_length=64 * 1024,
        required=False,
        trim_whitespace=False,
    )
    timeout_seconds = serializers.IntegerField(min_value=1, max_value=10, default=3)
