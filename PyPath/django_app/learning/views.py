"""Server-rendered and REST views for the learning platform."""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework import generics, permissions, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from .curriculum_registry import ROADMAP_STAGES, CURRICULUM_TRACKS
from .forms import RegistrationForm, SubmissionImageForm
from .i18n import (
    LANGUAGE_SESSION_KEY,
    SUPPORTED_LANGUAGES,
    current_language,
    exercise_display,
    lesson_display,
    localize_curriculum,
    localize_roadmap,
)
from .lesson_content import book_lesson_sections
from .models import Exercise, Lesson, Submission
from .pedagogy import get_learning_map, get_learning_visual
from .serializers import (
    CodeRunSerializer,
    ExerciseSerializer,
    LessonSerializer,
    SubmissionCreateSerializer,
    SubmissionSerializer,
)
from .services import FastAPICodeRunnerClient, GradingServiceError, grade_submission


def register_view(request):
    """Register a learner, then start an authenticated browser session."""
    if request.user.is_authenticated:
        return redirect("learning:home")

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Your account has been created. You can submit a solution now.",
            )
            return redirect("learning:home")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})


def set_interface_language(request):
    """Persist a safe VI/EN UI preference and return to the current page."""
    if request.method != "POST":
        return redirect("learning:home")

    language = request.POST.get("language", "vi")
    if language in SUPPORTED_LANGUAGES:
        request.session[LANGUAGE_SESSION_KEY] = language

    destination = request.POST.get("next", "")
    if not url_has_allowed_host_and_scheme(
        url=destination,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        destination = "learning:home"
    return redirect(destination)


class HomeView(ListView):
    """Show all published lessons and their published exercises."""

    model = Lesson
    context_object_name = "lessons"
    template_name = "learning/home.html"

    def get_queryset(self):
        exercises = Exercise.objects.published().only(
            "id", "lesson_id", "title", "slug", "order"
        )
        return Lesson.objects.published().prefetch_related(
            Prefetch("exercises", queryset=exercises)
        )

    def get_context_data(self, **kwargs):
        """Group the flat lesson model into an easy-to-scan learning path."""
        context = super().get_context_data(**kwargs)
        lessons = list(context["lessons"])
        lessons_by_track = {track["key"]: [] for track in CURRICULUM_TRACKS}

        for lesson in lessons:
            lessons_by_track.setdefault(lesson.track, []).append(lesson)

        curriculum_sections = [
            {
                **track,
                "lessons": lessons_by_track.get(track["key"], []),
                "lesson_count": len(lessons_by_track.get(track["key"], [])),
                "practice_count": sum(
                    len(lesson.exercises.all())
                    for lesson in lessons_by_track.get(track["key"], [])
                ),
                "estimated_minutes": sum(
                    lesson.estimated_minutes
                    for lesson in lessons_by_track.get(track["key"], [])
                ),
            }
            for track in CURRICULUM_TRACKS
            if lessons_by_track.get(track["key"])
        ]
        sections_by_key = {
            section["key"]: section for section in curriculum_sections
        }

        language = current_language(self.request)
        context["curriculum_sections"] = localize_curriculum(
            language, curriculum_sections
        )
        roadmap_stages = [
            {
                **stage,
                "tracks": [
                    sections_by_key[track_key]
                    for track_key in stage["track_keys"]
                    if track_key in sections_by_key
                ],
                "track_count": sum(
                    track_key in sections_by_key
                    for track_key in stage["track_keys"]
                ),
                "lesson_count": sum(
                    sections_by_key[track_key]["lesson_count"]
                    for track_key in stage["track_keys"]
                    if track_key in sections_by_key
                ),
                "practice_count": sum(
                    sections_by_key[track_key]["practice_count"]
                    for track_key in stage["track_keys"]
                    if track_key in sections_by_key
                ),
                "estimated_minutes": sum(
                    sections_by_key[track_key]["estimated_minutes"]
                    for track_key in stage["track_keys"]
                    if track_key in sections_by_key
                ),
            }
            for stage in ROADMAP_STAGES
            if any(track_key in sections_by_key for track_key in stage["track_keys"])
        ]
        context["roadmap_stages"] = localize_roadmap(
            language, roadmap_stages
        )
        context["lesson_total"] = len(lessons)
        return context


class LessonDetailView(DetailView):
    """Display one published lesson and the exercises attached to it."""

    model = Lesson
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "lesson"
    template_name = "learning/lesson_detail.html"

    def get_queryset(self):
        return Lesson.objects.published().prefetch_related(
            Prefetch("exercises", queryset=Exercise.objects.published())
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = current_language(self.request)
        context["learning_map"] = get_learning_map(self.object.track, language)
        context["learning_visual"] = get_learning_visual(self.object.track, language)
        context["lesson_sections"] = book_lesson_sections(
            self.object.content, language, self.object
        )
        context["lesson_display"] = lesson_display(language, self.object)
        for exercise in self.object.exercises.all():
            exercise.display_title = exercise_display(language, exercise)["title"]
        return context


class ExerciseDetailView(DetailView):
    """Display an exercise and the image-upload form for authenticated users."""

    model = Exercise
    slug_field = "slug"
    slug_url_kwarg = "slug"
    context_object_name = "exercise"
    template_name = "learning/exercise_detail.html"

    def get_queryset(self):
        return Exercise.objects.published().filter(
            lesson__is_published=True
        ).select_related("lesson")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SubmissionImageForm()
        context["exercise_display"] = exercise_display(
            current_language(self.request), self.object
        )
        context["lesson_display"] = lesson_display(
            current_language(self.request), self.object.lesson
        )
        return context


class SubmissionCreateView(LoginRequiredMixin, TemplateView):
    """Receive an image from the HTML form and forward it to FastAPI."""

    template_name = "learning/exercise_detail.html"

    def post(self, request, *args, **kwargs):
        exercise = get_object_or_404(
            Exercise.objects.published()
            .filter(lesson__is_published=True)
            .select_related("lesson"),
            slug=kwargs["slug"],
        )
        form = SubmissionImageForm(request.POST, request.FILES)
        if not form.is_valid():
            return self.render_to_response(
                {"exercise": exercise, "form": form},
                status=400,
            )

        submission = form.save(commit=False)
        submission.user = request.user
        submission.exercise = exercise
        submission.save()
        grade_submission(submission)

        if submission.status == Submission.Status.PASSED:
            messages.success(
                request,
                "Correct! Your code passed the expected-output check.",
            )
        elif submission.status == Submission.Status.FAILED:
            messages.error(request, "The code ran, but its output did not match yet.")
        else:
            messages.warning(
                request,
                "The submission was saved, but grading could not complete.",
            )
        return redirect("learning:submission-detail", submission_id=submission.id)


class SubmissionDetailView(LoginRequiredMixin, DetailView):
    """Let a learner inspect only their own submission result."""

    model = Submission
    pk_url_kwarg = "submission_id"
    context_object_name = "submission"
    template_name = "learning/submission_detail.html"

    def get_queryset(self):
        return Submission.objects.filter(
            user=self.request.user
        ).select_related("exercise", "user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["exercise_display"] = exercise_display(
            current_language(self.request), self.object.exercise
        )
        return context


class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.published().prefetch_related(
        Prefetch("exercises", queryset=Exercise.objects.published())
    )
    serializer_class = LessonSerializer


class LessonDetailAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.published().prefetch_related(
        Prefetch("exercises", queryset=Exercise.objects.published())
    )
    serializer_class = LessonSerializer
    lookup_field = "slug"


class ExerciseDetailAPIView(generics.RetrieveAPIView):
    queryset = (
        Exercise.objects.published()
        .filter(lesson__is_published=True)
        .select_related("lesson")
    )
    serializer_class = ExerciseSerializer
    lookup_field = "slug"


class SubmissionCreateAPIView(generics.CreateAPIView):
    """Authenticated multipart API endpoint for an OCR submission."""

    serializer_class = SubmissionCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()
        output = SubmissionSerializer(submission, context={"request": request})
        headers = self.get_success_headers(output.data)
        return Response(output.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class SubmissionDetailAPIView(generics.RetrieveAPIView):
    serializer_class = SubmissionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"

    def get_queryset(self):
        return Submission.objects.filter(
            user=self.request.user
        ).select_related("exercise", "user")


class CodeSandboxRunAPIView(APIView):
    """Authenticated JSON endpoint that proxies typed code to FastAPI."""

    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (JSONParser,)

    def post(self, request, *args, **kwargs):
        serializer = CodeRunSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            result = FastAPICodeRunnerClient().run(
                code=data["code"],
                stdin=data.get("stdin", ""),
                timeout_seconds=data["timeout_seconds"],
            )
        except GradingServiceError as exc:
            return Response(
                {
                    "status": Submission.Status.ERROR,
                    "execution_output": "",
                    "error_message": str(exc),
                    "exit_code": None,
                    "timed_out": False,
                    "output_truncated": False,
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            {
                "status": result.status,
                "execution_output": result.execution_output,
                "error_message": result.error_message,
                "exit_code": result.exit_code,
                "timed_out": result.timed_out,
                "output_truncated": result.output_truncated,
            }
        )
