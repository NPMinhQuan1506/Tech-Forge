"""Tests for lesson publication, OCR forwarding, and learner submissions."""

from __future__ import annotations

import io
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

import requests
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image
from rest_framework.test import APIClient

from .curriculum import CURRICULUM, CURRICULUM_MANIFEST
from .curriculum_registry import ROADMAP_STAGES, CURRICULUM_TRACKS
from .forms import SubmissionImageForm
from .lesson_content import lesson_sections
from .models import Exercise, Lesson, Submission
from .services import (
    FastAPICodeRunnerClient,
    FastAPIGraderClient,
    GradingServiceError,
    grade_submission,
)


def make_image(name: str = "solution.png") -> SimpleUploadedFile:
    """Return a tiny genuine PNG accepted by Django's ImageField validation."""
    stream = io.BytesIO()
    Image.new("RGB", (40, 20), color="white").save(stream, format="PNG")
    return SimpleUploadedFile(name, stream.getvalue(), content_type="image/png")


class LearningTestCase(TestCase):
    """Base test fixture that puts uploaded images in a disposable folder."""

    def setUp(self) -> None:
        super().setUp()
        self.media_directory = tempfile.TemporaryDirectory()
        self.media_override = override_settings(
            MEDIA_ROOT=Path(self.media_directory.name)
        )
        self.media_override.enable()
        self.user = get_user_model().objects.create_user(
            username="learner", password="safe-test-password"
        )
        self.lesson = Lesson.objects.create(
            title="Print",
            slug="print",
            summary="Learn print.",
            content="Use print().",
            is_published=True,
        )
        self.exercise = Exercise.objects.create(
            lesson=self.lesson,
            title="Hello",
            slug="hello",
            prompt="Print Hello.",
            expected_output="Hello",
            is_published=True,
        )

    def tearDown(self) -> None:
        self.media_override.disable()
        self.media_directory.cleanup()
        super().tearDown()

    def create_submission(self) -> Submission:
        return Submission.objects.create(
            user=self.user,
            exercise=self.exercise,
            image=make_image(),
        )


class ModelAndFormTests(LearningTestCase):
    def test_submission_storage_does_not_keep_a_user_controlled_extension(self) -> None:
        submission = Submission.objects.create(
            user=self.user,
            exercise=self.exercise,
            image=make_image("solution.html"),
        )

        self.assertTrue(submission.image.name.endswith(".png"))

    def test_seed_command_is_idempotent(self) -> None:
        call_command("seed_learning_data")
        starter = Lesson.objects.get(curriculum_key="python-01-print")
        starter.title = "Administrator's custom title"
        starter.slug = "administrator-custom-python-title"
        starter.track = Lesson.Track.AI
        starter.is_published = False
        starter.save(update_fields=("title", "slug", "track", "is_published"))

        exercise = Exercise.objects.get(
            curriculum_key="python-01-print-greeting"
        )
        exercise.title = "Administrator's custom exercise"
        exercise.slug = "administrator-custom-print-exercise"
        exercise.expected_output = "Custom output"
        exercise.save(update_fields=("title", "slug", "expected_output"))

        call_command("seed_learning_data")

        starter.refresh_from_db()
        exercise.refresh_from_db()
        self.assertEqual(
            Lesson.objects.filter(curriculum_key="python-01-print").count(), 1
        )
        self.assertEqual(
            Exercise.objects.filter(
                curriculum_key="python-01-print-greeting"
            ).count(),
            1,
        )
        self.assertEqual(
            starter.title,
            "Administrator's custom title",
        )
        self.assertEqual(starter.slug, "administrator-custom-python-title")
        self.assertEqual(starter.track, Lesson.Track.AI)
        self.assertFalse(starter.is_published)
        self.assertEqual(exercise.title, "Administrator's custom exercise")
        self.assertEqual(exercise.slug, "administrator-custom-print-exercise")
        self.assertEqual(exercise.expected_output, "Custom output")

    def test_seed_command_creates_the_complete_mastery_curriculum(self) -> None:
        call_command("seed_learning_data")

        expected_tracks = {track["key"] for track in CURRICULUM_TRACKS}
        curriculum_lessons = Lesson.objects.filter(curriculum_key__isnull=False)
        curriculum_exercises = Exercise.objects.filter(curriculum_key__isnull=False)

        self.assertEqual(
            curriculum_lessons.count(), CURRICULUM_MANIFEST["lesson_count"]
        )
        self.assertEqual(
            curriculum_exercises.count(), CURRICULUM_MANIFEST["exercise_count"]
        )
        self.assertSetEqual(
            set(curriculum_lessons.values_list("track", flat=True)),
            expected_tracks,
        )
        self.assertTrue(curriculum_lessons.filter(is_published=True).exists())
        self.assertTrue(curriculum_exercises.filter(is_published=True).exists())
        self.assertTrue(
            Exercise.objects.filter(
                curriculum_key="capstone-06-ml-platform-system-design-checkpoint"
            ).exists()
        )
        self.assertTrue(
            Lesson.objects.filter(
                curriculum_key="math-01-sets-logic-notation"
            ).exists()
        )

    def test_bundled_curriculum_has_unique_complete_metadata(self) -> None:
        lessons = [entry["lesson"] for entry in CURRICULUM]
        exercises = [
            exercise for entry in CURRICULUM for exercise in entry["exercises"]
        ]

        self.assertEqual(len(lessons), CURRICULUM_MANIFEST["lesson_count"])
        self.assertEqual(len(exercises), CURRICULUM_MANIFEST["exercise_count"])
        self.assertEqual(CURRICULUM_MANIFEST["lesson_count"], 180)
        self.assertEqual(CURRICULUM_MANIFEST["mastery_extension_count"], 130)
        self.assertEqual(
            len({lesson["curriculum_key"] for lesson in lessons}), len(lessons)
        )
        self.assertEqual(len({lesson["slug"] for lesson in lessons}), len(lessons))
        self.assertEqual(
            len({exercise["curriculum_key"] for exercise in exercises}),
            len(exercises),
        )
        self.assertEqual(
            len({exercise["slug"] for exercise in exercises}), len(exercises)
        )
        self.assertTrue(all(lesson["estimated_minutes"] > 0 for lesson in lessons))
        self.assertTrue(all(exercise["expected_output"] for exercise in exercises))
        self.assertTrue(all(entry["exercises"] for entry in CURRICULUM))
        for exercise in exercises:
            compile(exercise["starter_code"], exercise["slug"], "exec")

    def test_seed_command_rejects_a_manual_slug_collision(self) -> None:
        Lesson.objects.create(
            title="Manual mathematics draft",
            slug="math-sets-logic-notation",
            content="This must remain manual content.",
            is_published=False,
        )

        with self.assertRaisesMessage(CommandError, "already used by a different"):
            call_command("seed_learning_data")

        self.assertTrue(
            Lesson.objects.filter(slug="math-sets-logic-notation").exists()
        )

    def test_seed_command_dry_run_keeps_the_database_unchanged(self) -> None:
        call_command("seed_learning_data", "--track", "math", "--dry-run")

        self.assertFalse(
            Lesson.objects.filter(curriculum_key__startswith="math-").exists()
        )

    def test_seed_command_refreshes_only_when_explicitly_requested(self) -> None:
        call_command("seed_learning_data")
        starter = Lesson.objects.get(curriculum_key="python-01-print")
        starter.title = "Temporary custom title"
        starter.save(update_fields=("title",))

        call_command("seed_learning_data", "--refresh")

        starter.refresh_from_db()
        self.assertEqual(starter.title, CURRICULUM[0]["lesson"]["title"])

    def test_exercise_timeout_cannot_exceed_fastapi_limit(self) -> None:
        too_slow = Exercise(
            lesson=self.lesson,
            title="Slow",
            slug="slow",
            prompt="x",
            expected_output="x",
            timeout_seconds=11,
        )
        with self.assertRaisesMessage(
            Exception,
            "Ensure this value is less than or equal to 10",
        ):
            too_slow.full_clean()

    def test_submission_form_rejects_oversized_upload(self) -> None:
        upload = make_image()
        upload.size = SubmissionImageForm.max_image_size + 1
        form = SubmissionImageForm(data={}, files={"image": upload})
        self.assertFalse(form.is_valid())
        self.assertIn("5 MB or smaller", form.errors["image"][0])


class FastAPIClientTests(LearningTestCase):
    @patch("learning.services.requests.post")
    def test_client_sends_contract_and_normalizes_passed_response(
        self, mock_post: Mock
    ) -> None:
        submission = self.create_submission()
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "passed",
            "extracted_code": "print('Hello')",
            "ocr_confidence": 97.5,
            "execution_output": "Hello\n",
            "error_message": None,
        }
        mock_post.return_value = mock_response

        result = FastAPIGraderClient(
            url="http://grader/grade-image",
            timeout=7,
        ).grade(submission)

        self.assertEqual(result.status, Submission.Status.PASSED)
        self.assertEqual(result.extracted_code, "print('Hello')")
        self.assertEqual(result.ocr_confidence, 97.5)
        self.assertEqual(result.error_message, "")
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["data"]["expected_output"], "Hello")
        self.assertEqual(kwargs["data"]["timeout_seconds"], "5")
        self.assertEqual(kwargs["timeout"], 7)

    @patch("learning.services.requests.post")
    def test_client_keeps_structured_fastapi_ocr_error(self, mock_post: Mock) -> None:
        submission = self.create_submission()
        mock_response = Mock()
        mock_response.status_code = 422
        mock_response.json.return_value = {
            "status": "error",
            "extracted_code": "",
            "ocr_confidence": None,
            "execution_output": "",
            "error_message": "No Python code could be detected.",
        }
        mock_post.return_value = mock_response

        result = FastAPIGraderClient().grade(submission)

        self.assertEqual(result.status, Submission.Status.ERROR)
        self.assertEqual(result.error_message, "No Python code could be detected.")
        mock_response.raise_for_status.assert_not_called()

    @patch("learning.services.requests.post", side_effect=requests.ConnectionError)
    def test_grade_submission_stores_safe_transport_error(
        self, mock_post: Mock
    ) -> None:
        submission = self.create_submission()

        grade_submission(submission)
        submission.refresh_from_db()

        self.assertEqual(submission.status, Submission.Status.ERROR)
        self.assertIn("unavailable", submission.error_message)

    @patch("learning.services.requests.post")
    def test_code_runner_sends_json_contract(self, mock_post: Mock) -> None:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "status": "passed",
            "execution_output": "Hello\n",
            "error_message": None,
            "exit_code": 0,
            "timed_out": False,
            "output_truncated": False,
        }
        mock_post.return_value = mock_response

        result = FastAPICodeRunnerClient(
            url="http://grader/run-code",
            timeout=4,
        ).run(code="print('Hello')", stdin="", timeout_seconds=2)

        self.assertEqual(result.status, Submission.Status.PASSED)
        self.assertEqual(result.execution_output, "Hello\n")
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["code"], "print('Hello')")
        self.assertEqual(kwargs["json"]["timeout_seconds"], 2)
        self.assertEqual(kwargs["timeout"], 4)


class BrowserAndAPITests(LearningTestCase):
    def test_home_uses_the_learning_platform_stylesheet(self) -> None:
        """Keep the redesigned shell wired to its progressive UI assets."""
        response = self.client.get(reverse("learning:home"))

        self.assertContains(response, "learning/css/app.css")
        self.assertContains(response, "learning/js/app.js")
        self.assertContains(response, "data-three-hero")
        self.assertContains(response, "data-curriculum-search")
        self.assertContains(response, "data-track-section")
        self.assertContains(response, "roadmap-overview")
        self.assertContains(response, 'data-roadmap-track="python"')
        self.assertContains(response, "Master Python")
        self.assertContains(response, "Học sâu.")

    def test_lesson_detail_renders_deep_learning_map(self) -> None:
        response = self.client.get(
            reverse("learning:lesson-detail", args=(self.lesson.slug,))
        )

        self.assertContains(response, "Bản đồ tư duy của bài này")
        self.assertContains(response, "Mô hình trong đầu")
        self.assertContains(response, "Trường hợp biên")

    def test_exercise_detail_renders_code_sandbox(self) -> None:
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("learning:exercise-detail", args=(self.exercise.slug,))
        )

        self.assertContains(response, "data-code-sandbox")
        self.assertContains(response, "learning/js/sandbox.js")
        self.assertContains(response, "Chạy thử trước khi nộp OCR")

    def test_registration_creates_an_authenticated_learner(self) -> None:
        response = self.client.post(
            reverse("register"),
            {
                "username": "new-learner",
                "password1": "new-learner-strong-password",
                "password2": "new-learner-strong-password",
            },
        )

        self.assertRedirects(response, reverse("learning:home"))
        self.assertTrue(
            get_user_model().objects.filter(username="new-learner").exists()
        )
        self.assertEqual(
            self.client.get(
                reverse("learning:home")
            ).wsgi_request.user.username,
            "new-learner",
        )

    def test_login_uses_the_styled_authentication_form(self) -> None:
        """The visual login form must retain Django's secure authentication flow."""
        response = self.client.post(
            reverse("login"),
            {"username": self.user.username, "password": "safe-test-password"},
        )

        self.assertRedirects(response, reverse("learning:home"))
        self.assertEqual(
            self.client.get(reverse("learning:home")).wsgi_request.user,
            self.user,
        )

    def test_home_only_shows_published_content(self) -> None:
        private_lesson = Lesson.objects.create(
            title="Private",
            slug="private",
            content="Private lesson",
            is_published=False,
        )
        Exercise.objects.create(
            lesson=private_lesson,
            title="Private exercise",
            slug="private-exercise",
            prompt="Nope",
            expected_output="Nope",
            is_published=True,
        )

        response = self.client.get(reverse("learning:home"))

        self.assertContains(response, "Print")
        self.assertNotContains(response, "Private")

    def test_home_groups_seeded_lessons_by_track(self) -> None:
        call_command("seed_learning_data")

        response = self.client.get(reverse("learning:home"))

        sections = response.context["curriculum_sections"]
        stages = response.context["roadmap_stages"]
        math_section = next(section for section in sections if section["key"] == "math")
        math_stage = next(
            stage for stage in stages if stage["key"] == "math-data"
        )

        self.assertEqual(len(sections), len(CURRICULUM_TRACKS))
        self.assertEqual(len(stages), len(ROADMAP_STAGES))
        self.assertEqual(response.context["lesson_total"], len(CURRICULUM) + 1)
        self.assertEqual(
            sum(stage["lesson_count"] for stage in stages),
            response.context["lesson_total"],
        )
        self.assertEqual(math_section["lesson_count"], 12)
        self.assertEqual(math_section["practice_count"], 12)
        self.assertGreater(math_section["estimated_minutes"], 0)
        self.assertEqual(math_stage["track_count"], 3)
        self.assertEqual(math_stage["lesson_count"], 32)
        self.assertContains(response, "Python nền tảng")
        self.assertContains(response, "Generative AI, RAG &amp; Agents")
        self.assertContains(response, "Bản đồ năng lực tổng quan")

    def test_html_submission_requires_login(self) -> None:
        url = reverse("learning:submission-create", args=(self.exercise.slug,))

        response = self.client.post(url, {"image": make_image()})

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response.url)
        self.assertEqual(Submission.objects.count(), 0)

    @patch("learning.serializers.grade_submission")
    def test_api_submission_forwards_authenticated_image(
        self, mock_grade: Mock
    ) -> None:
        mock_grade.side_effect = lambda submission: submission
        client = APIClient()
        client.force_authenticate(user=self.user)

        response = client.post(
            reverse("learning:api-submission-create"),
            {"exercise": self.exercise.id, "image": make_image()},
            format="multipart",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["status"], Submission.Status.PENDING)
        self.assertEqual(Submission.objects.count(), 1)
        mock_grade.assert_called_once()

    def test_api_submission_rejects_anonymous_request(self) -> None:
        client = APIClient()

        response = client.post(
            reverse("learning:api-submission-create"),
            {"exercise": self.exercise.id, "image": make_image()},
            format="multipart",
        )

        self.assertEqual(response.status_code, 403)

    @patch("learning.views.FastAPICodeRunnerClient.run")
    def test_api_sandbox_run_requires_login(self, mock_run: Mock) -> None:
        response = self.client.post(
            reverse("learning:api-sandbox-run"),
            {"code": "print('x')"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 403)
        mock_run.assert_not_called()

    @patch("learning.views.FastAPICodeRunnerClient.run")
    def test_api_sandbox_run_returns_fastapi_result(self, mock_run: Mock) -> None:
        self.client.force_login(self.user)
        mock_run.return_value = Mock(
            status=Submission.Status.PASSED,
            execution_output="Hello\n",
            error_message="",
            exit_code=0,
            timed_out=False,
            output_truncated=False,
        )

        response = self.client.post(
            reverse("learning:api-sandbox-run"),
            {"code": "print('Hello')", "stdin": "", "timeout_seconds": 2},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["execution_output"], "Hello\n")
        mock_run.assert_called_once_with(
            code="print('Hello')",
            stdin="",
            timeout_seconds=2,
        )


class InterfaceLanguageTests(TestCase):
    """The language selector must be session-scoped and redirect-safe."""

    def test_switching_to_english_updates_template_context(self) -> None:
        response = self.client.post(
            reverse("learning:set-interface-language"),
            {"language": "en", "next": "/"},
        )

        self.assertRedirects(response, "/")
        homepage = self.client.get(reverse("learning:home"))
        self.assertEqual(homepage.context["ui_language"], "en")
        self.assertEqual(homepage.context["ui"]["roadmap_eyebrow"], "Capability roadmap")

    def test_language_switch_rejects_external_redirect(self) -> None:
        response = self.client.post(
            reverse("learning:set-interface-language"),
            {"language": "en", "next": "https://unsafe.example"},
        )

        self.assertRedirects(response, reverse("learning:home"))


class CurriculumLanguagePresentationTests(LearningTestCase):
    """English mode must not leak the Vietnamese seeded presentation fields."""

    def test_english_home_uses_localized_track_and_card_copy(self) -> None:
        self.lesson.title = "Bài Python bằng tiếng Việt"
        self.lesson.summary = "Tóm tắt tiếng Việt"
        self.lesson.track = Lesson.Track.PYTHON
        self.lesson.save(update_fields=("title", "summary", "track"))
        session = self.client.session
        session["learning_ui_language"] = "en"
        session.save()

        response = self.client.get(reverse("learning:home"))

        self.assertContains(response, "Python foundations")
        self.assertContains(response, "Python · Lesson 01")
        self.assertNotContains(response, "Bài Python bằng tiếng Việt")
        self.assertNotContains(response, "Tóm tắt tiếng Việt")


class LessonContentPresentationTests(TestCase):
    """Localized lesson sections preserve code while translating study guidance."""

    def test_english_sections_translate_headings_and_keep_example(self) -> None:
        content = (
            "Mục tiêu\nHiểu hàm.\n\nKhái niệm chính\n- Hàm nhận input.\n\n"
            "Ví dụ tối thiểu\nprint('hello')\n\nCách học hiệu quả\n1. Chạy code.\n\n"
            "Lỗi thường gặp\n- Quên return.\n\nTóm tắt\nThử lại."
        )

        sections = lesson_sections(content, "en")

        self.assertEqual(sections[0]["title"], "Learning goal")
        self.assertEqual(sections[2]["body"], "print('hello')")
        self.assertIn("boundary case", sections[1]["body"])

    def test_english_learning_map_has_no_vietnamese_card_content(self) -> None:
        from .pedagogy import get_learning_map

        learning_map = get_learning_map("python", "en")

        self.assertIn("Python transforms", learning_map.mental_model)
        self.assertTrue(all("Đ" not in item for item in learning_map.pipeline))
