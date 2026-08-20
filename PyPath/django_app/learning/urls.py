"""URLs for both the browser UI and JSON API."""

from django.urls import path

from . import views


app_name = "learning"

urlpatterns = [
    path("language/", views.set_interface_language, name="set-interface-language"),
    path("", views.HomeView.as_view(), name="home"),
    path(
        "lessons/<slug:slug>/",
        views.LessonDetailView.as_view(),
        name="lesson-detail",
    ),
    path(
        "exercises/<slug:slug>/",
        views.ExerciseDetailView.as_view(),
        name="exercise-detail",
    ),
    path(
        "exercises/<slug:slug>/submit/",
        views.SubmissionCreateView.as_view(),
        name="submission-create",
    ),
    path(
        "submissions/<uuid:submission_id>/",
        views.SubmissionDetailView.as_view(),
        name="submission-detail",
    ),
    path("api/v1/lessons/", views.LessonListAPIView.as_view(), name="api-lesson-list"),
    path(
        "api/v1/lessons/<slug:slug>/",
        views.LessonDetailAPIView.as_view(),
        name="api-lesson-detail",
    ),
    path(
        "api/v1/exercises/<slug:slug>/",
        views.ExerciseDetailAPIView.as_view(),
        name="api-exercise-detail",
    ),
    path(
        "api/v1/submissions/",
        views.SubmissionCreateAPIView.as_view(),
        name="api-submission-create",
    ),
    path(
        "api/v1/submissions/<uuid:id>/",
        views.SubmissionDetailAPIView.as_view(),
        name="api-submission-detail",
    ),
    path(
        "api/v1/sandbox/run/",
        views.CodeSandboxRunAPIView.as_view(),
        name="api-sandbox-run",
    ),
]
