"""Django admin registration for learning content and grading records."""

from django.contrib import admin

from .models import Exercise, Lesson, Submission


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 0
    fields = (
        "title",
        "slug",
        "order",
        "expected_output",
        "timeout_seconds",
        "is_published",
    )
    prepopulated_fields = {"slug": ("title",)}
    show_change_link = True


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "track",
        "level",
        "order",
        "estimated_minutes",
        "is_published",
        "updated_at",
    )
    list_filter = ("track", "level", "is_published")
    search_fields = ("title", "summary", "content")
    ordering = ("order", "title")
    prepopulated_fields = {"slug": ("title",)}
    inlines = (ExerciseInline,)


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "lesson",
        "order",
        "timeout_seconds",
        "is_published",
    )
    list_filter = ("is_published", "lesson")
    search_fields = ("title", "prompt", "expected_output")
    ordering = ("lesson__order", "order", "title")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "exercise", "status", "ocr_confidence", "created_at")
    list_filter = ("status", "exercise")
    search_fields = ("user__username", "exercise__title", "extracted_code")
    readonly_fields = (
        "id",
        "user",
        "exercise",
        "image",
        "extracted_code",
        "ocr_confidence",
        "execution_output",
        "error_message",
        "grader_response",
        "created_at",
        "updated_at",
    )
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    def has_add_permission(self, request) -> bool:
        return False
