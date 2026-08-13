"""Presentation-safe lesson sections for Vietnamese and English learners."""

from __future__ import annotations

from collections.abc import Iterable


VI_SECTION_TITLES = (
    "Mục tiêu",
    "Khái niệm chính",
    "Ví dụ tối thiểu",
    "Cách học hiệu quả",
    "Lỗi thường gặp",
    "Tóm tắt",
)

EN_SECTION_TITLES = (
    "Learning goal",
    "Core ideas",
    "Minimal example",
    "Practice method",
    "Common pitfalls",
    "Summary",
)


def _split_source_content(content: str) -> list[str]:
    """Extract the six authored blocks from the stable seed-content format."""
    blocks: list[str] = []
    current: list[str] = []
    titles = set(VI_SECTION_TITLES)

    for line in content.splitlines():
        if line.strip() in titles:
            if current:
                blocks.append("\n".join(current).strip())
            current = []
            continue
        current.append(line)
    if current:
        blocks.append("\n".join(current).strip())

    return (blocks + [""] * len(VI_SECTION_TITLES))[: len(VI_SECTION_TITLES)]


def _english_blocks(source_blocks: Iterable[str]) -> list[str]:
    """Provide a readable English study path while preserving the code example."""
    blocks = list(source_blocks)
    example = blocks[2]
    return [
        "Build a working mental model for this topic, then verify it with a small runnable program.",
        "- Identify the input, the transformation, and the expected output.\n"
        "- State the invariant that should remain true as input size or shape changes.\n"
        "- Check the result against one normal case and one boundary case.",
        example,
        "1. Read the example and predict the output before running it.\n"
        "2. Change one value, then explain why the output changes.\n"
        "3. Complete the sandbox checkpoint with your own code and test an edge case.",
        "- Avoid relying on one happy-path input.\n"
        "- Keep data types, output formatting, and assumptions explicit.\n"
        "- Separate a correct-looking output from a correct general solution.",
        "Mastery comes from connecting the concept to a runnable example, a boundary case, and a short explanation in your own words.",
    ]


def lesson_sections(content: str, language: str) -> list[dict[str, str]]:
    """Return localized section labels and body text without altering source data."""
    source_blocks = _split_source_content(content)
    titles = EN_SECTION_TITLES if language == "en" else VI_SECTION_TITLES
    blocks = _english_blocks(source_blocks) if language == "en" else source_blocks
    return [
        {"title": title, "body": body, "is_example": index == 2}
        for index, (title, body) in enumerate(zip(titles, blocks, strict=True))
    ]
