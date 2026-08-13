"""Create the starter curriculum without overwriting administrator content."""

from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from learning.curriculum import CURRICULUM
from learning.models import Exercise, Lesson


class Command(BaseCommand):
    """Seed the full learning path using stable non-user-facing keys."""

    help = (
        "Create missing Master Python, AI/ML, mathematics, MLOps and backend "
        "curriculum content without overwriting administrator edits."
    )

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--refresh",
            action="store_true",
            help=(
                "Explicitly replace fields on curriculum records with the bundled "
                "content. Never used by automatic container startup."
            ),
        )
        parser.add_argument(
            "--track",
            action="append",
            dest="tracks",
            help="Seed only one curriculum track. May be supplied more than once.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Validate and simulate the operation without committing changes.",
        )

    @staticmethod
    def _copy_defaults(specification: dict[str, Any]) -> dict[str, Any]:
        """Return fields accepted as model defaults apart from the stable key."""
        return {
            name: value
            for name, value in specification.items()
            if name != "curriculum_key"
        }

    @classmethod
    def _apply_refresh(
        cls,
        instance: Lesson | Exercise,
        specification: dict[str, Any],
        *,
        include_lesson: Lesson | None = None,
    ) -> bool:
        """Update a curriculum record only when the operator requested it."""
        changes: list[str] = []
        for field, value in cls._copy_defaults(specification).items():
            if getattr(instance, field) != value:
                setattr(instance, field, value)
                changes.append(field)

        if include_lesson is not None and getattr(instance, "lesson") != include_lesson:
            instance.lesson = include_lesson
            changes.append("lesson")

        if not changes:
            return False

        instance.save(update_fields=changes)
        return True

    @staticmethod
    def _validate_manifest(entries: tuple[dict[str, Any], ...]) -> None:
        """Fail early on duplicate keys or slugs in bundled content."""
        lessons = [entry["lesson"] for entry in entries]
        exercises = [exercise for entry in entries for exercise in entry["exercises"]]
        checks = (
            ("lesson curriculum keys", [lesson["curriculum_key"] for lesson in lessons]),
            ("lesson slugs", [lesson["slug"] for lesson in lessons]),
            (
                "exercise curriculum keys",
                [exercise["curriculum_key"] for exercise in exercises],
            ),
            ("exercise slugs", [exercise["slug"] for exercise in exercises]),
        )
        for label, values in checks:
            if len(values) != len(set(values)):
                raise CommandError(f"Bundled curriculum has duplicate {label}.")

    @staticmethod
    def _raise_if_slug_conflicts(
        model: type[Lesson] | type[Exercise],
        specification: dict[str, Any],
        *,
        refresh: bool,
        label: str,
    ) -> None:
        """Prevent an automatic seed from claiming manual content by slug.

        Existing curriculum records are always found by the immutable key. A
        manual record that happens to use a future bundled slug must be renamed
        explicitly instead of being silently converted into system content.
        """
        key = specification["curriculum_key"]
        current = model.objects.filter(curriculum_key=key).first()
        if current is not None and not refresh:
            return

        conflicts = model.objects.filter(slug=specification["slug"])
        if current is not None:
            conflicts = conflicts.exclude(pk=current.pk)
        conflict = conflicts.first()
        if conflict is not None:
            raise CommandError(
                f"Cannot seed {label} '{specification['slug']}': its slug is "
                "already used by a different record. Rename that record or use a "
                "different bundled slug before continuing."
            )

    @classmethod
    def _preflight(cls, entries: tuple[dict[str, Any], ...], *, refresh: bool) -> None:
        """Validate the catalog and database collisions before any write."""
        cls._validate_manifest(entries)
        for entry in entries:
            cls._raise_if_slug_conflicts(
                Lesson,
                entry["lesson"],
                refresh=refresh,
                label="lesson",
            )
            for exercise in entry["exercises"]:
                cls._raise_if_slug_conflicts(
                    Exercise,
                    exercise,
                    refresh=refresh,
                    label="exercise",
                )

    def _ensure_lesson(
        self,
        specification: dict[str, Any],
        *,
        refresh: bool,
        counters: dict[str, int],
    ) -> Lesson:
        key = specification["curriculum_key"]
        lesson = Lesson.objects.filter(curriculum_key=key).first()
        if lesson is not None:
            if refresh and self._apply_refresh(lesson, specification):
                counters["updated"] += 1
            else:
                counters["kept"] += 1
            return lesson

        lesson = Lesson.objects.create(**specification)
        counters["created"] += 1
        return lesson

    def _ensure_exercise(
        self,
        specification: dict[str, Any],
        *,
        lesson: Lesson,
        refresh: bool,
        counters: dict[str, int],
    ) -> None:
        key = specification["curriculum_key"]
        exercise = Exercise.objects.filter(curriculum_key=key).first()
        if exercise is not None:
            if refresh and self._apply_refresh(
                exercise,
                specification,
                include_lesson=lesson,
            ):
                counters["updated"] += 1
            else:
                counters["kept"] += 1
            return

        Exercise.objects.create(lesson=lesson, **specification)
        counters["created"] += 1

    @transaction.atomic
    def handle(self, *args, **options) -> None:
        refresh = options["refresh"]
        selected_tracks = set(options["tracks"] or ())
        known_tracks = {entry["lesson"]["track"] for entry in CURRICULUM}
        unknown_tracks = selected_tracks - known_tracks
        if unknown_tracks:
            names = ", ".join(sorted(unknown_tracks))
            raise CommandError(f"Unknown curriculum track: {names}.")

        entries = tuple(
            entry
            for entry in CURRICULUM
            if not selected_tracks or entry["lesson"]["track"] in selected_tracks
        )
        self._preflight(entries, refresh=refresh)
        counters = {"created": 0, "kept": 0, "updated": 0}

        for entry in entries:
            lesson = self._ensure_lesson(
                entry["lesson"],
                refresh=refresh,
                counters=counters,
            )
            for exercise in entry["exercises"]:
                self._ensure_exercise(
                    exercise,
                    lesson=lesson,
                    refresh=refresh,
                    counters=counters,
                )

        if options["dry_run"]:
            transaction.set_rollback(True)

        prefix = "Dry run; no changes saved. " if options["dry_run"] else ""
        self.stdout.write(
            self.style.SUCCESS(
                f"{prefix}Curriculum ready: "
                f"{len(entries)} lessons, "
                f"{sum(len(entry['exercises']) for entry in entries)} exercises. "
                f"Created {counters['created']}, updated {counters['updated']}, "
                f"kept {counters['kept']}."
            )
        )
