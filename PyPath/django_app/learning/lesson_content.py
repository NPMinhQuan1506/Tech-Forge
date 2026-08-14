"""Presentation-safe lesson sections for Vietnamese and English learners."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any


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


TRACK_BOOK_PROFILES: dict[str, dict[str, str]] = {
    "python": {
        "vi": "Python nền tảng",
        "en": "Python foundations",
        "system": "input -> type -> transform -> output",
        "lab": "Viết 3 biến thể chương trình: dữ liệu hợp lệ, dữ liệu rỗng, dữ liệu sai kiểu.",
    },
    "python_pro": {
        "vi": "Python production",
        "en": "Production Python",
        "system": "pure logic -> boundary -> tests -> package/API",
        "lab": "Tách logic thành function/module, thêm type hints, logging và pytest.",
    },
    "engineering": {
        "vi": "Software Engineering",
        "en": "Software Engineering",
        "system": "change -> test -> review -> release -> rollback",
        "lab": "Đóng gói thay đổi bằng branch, test, Docker command và ghi lại rollback note.",
    },
    "math": {
        "vi": "Toán cho AI",
        "en": "Math for AI",
        "system": "quantity -> shape -> formula -> gradient/decision",
        "lab": "Tự tính bằng Python list trước, sau đó đối chiếu với NumPy trong notebook riêng.",
    },
    "statistics": {
        "vi": "Xác suất thống kê",
        "en": "Probability and statistics",
        "system": "population -> sample -> estimate -> uncertainty -> decision",
        "lab": "Mô phỏng dữ liệu nhỏ, đo mean/variance, rồi giải thích độ bất định bằng chữ.",
    },
    "data": {
        "vi": "Data Engineering",
        "en": "Data Engineering",
        "system": "raw data -> validate -> clean -> transform -> feature table",
        "lab": "Tạo data quality report: schema, missing values, duplicates, leakage checks.",
    },
    "ai": {
        "vi": "AI Foundation",
        "en": "AI Foundation",
        "system": "user need -> task -> metric -> baseline -> guardrail",
        "lab": "Viết một AI design brief có objective, metric, risk, fallback và human review.",
    },
    "ml": {
        "vi": "Machine Learning",
        "en": "Machine Learning",
        "system": "features -> model -> prediction -> loss -> validation",
        "lab": "Xây baseline, split dữ liệu, chọn metric, phân tích lỗi theo từng lát dữ liệu.",
    },
    "mlops": {
        "vi": "MLOps",
        "en": "MLOps",
        "system": "data + code + config -> train -> registry -> deploy -> monitor",
        "lab": "Thêm config, model card, contract test, health check và monitoring checklist.",
    },
    "dl": {
        "vi": "Deep Learning",
        "en": "Deep Learning",
        "system": "tensor -> layer -> loss -> backward -> optimizer",
        "lab": "Viết training-loop checklist: seed, device, batch, loss, metric, checkpoint.",
    },
    "cv": {
        "vi": "Computer Vision",
        "en": "Computer Vision",
        "system": "image -> preprocess -> feature/model -> prediction -> visual error",
        "lab": "Lập bảng lỗi theo ánh sáng, góc chụp, blur, class imbalance và annotation noise.",
    },
    "nlp": {
        "vi": "NLP",
        "en": "NLP",
        "system": "text -> token -> embedding -> context -> answer/label",
        "lab": "Kiểm tra Unicode, tiếng Việt có dấu, câu dài, câu mơ hồ và dữ liệu nhạy cảm.",
    },
    "genai": {
        "vi": "Generative AI",
        "en": "Generative AI",
        "system": "prompt -> retrieval/tools -> model -> evaluation -> guardrail",
        "lab": "Tạo eval set, citation rule, refusal rule và test prompt injection cơ bản.",
    },
    "rl": {
        "vi": "Reinforcement Learning",
        "en": "Reinforcement Learning",
        "system": "state -> action -> reward -> policy/value -> exploration",
        "lab": "Mô tả state/action/reward, chạy mô phỏng nhỏ và ghi lại reward curve.",
    },
    "django": {
        "vi": "Django product engineering",
        "en": "Django product engineering",
        "system": "request -> URL -> view/service -> ORM -> template/API",
        "lab": "Thêm test cho view, permission, form validation, query count và admin workflow.",
    },
    "fastapi": {
        "vi": "FastAPI service engineering",
        "en": "FastAPI service engineering",
        "system": "schema -> dependency -> endpoint -> service -> response contract",
        "lab": "Viết contract test, timeout/error case, OpenAPI check và health endpoint.",
    },
    "capstone": {
        "vi": "Capstone portfolio",
        "en": "Capstone portfolio",
        "system": "problem -> repo -> model/service -> evidence -> demo",
        "lab": "Hoàn thiện README, architecture diagram, tests, demo script và retrospective.",
    },
}


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


def _profile_for(lesson: Any) -> dict[str, str]:
    track = getattr(lesson, "track", "python")
    return TRACK_BOOK_PROFILES.get(track, TRACK_BOOK_PROFILES["python"])


def _lesson_text(lesson: Any, attribute: str, fallback: str) -> str:
    value = getattr(lesson, attribute, "")
    return str(value or fallback).strip()


def _book_sections_vi(source_blocks: list[str], lesson: Any) -> list[dict[str, str]]:
    profile = _profile_for(lesson)
    title = _lesson_text(lesson, "title", "bài học này")
    summary = _lesson_text(lesson, "summary", source_blocks[5] or title)
    minutes = _lesson_text(lesson, "estimated_minutes", "45")
    level = _lesson_text(lesson, "level", "intermediate")
    goal, concepts, example, practice, pitfalls, takeaway = source_blocks

    return [
        {
            "title": "Mục tiêu năng lực",
            "body": (
                f"Sau bài này bạn không chỉ nhớ khái niệm của {title}. Bạn cần giải thích được "
                f"vấn đề bằng ngôn ngữ đời thường, viết được ví dụ chạy được, chỉ ra được trường hợp "
                f"hỏng, và biết đặt nó vào workflow của một ML Engineer.\n\n"
                f"Mục tiêu gốc: {goal}\n\n"
                f"Thời lượng gợi ý: {minutes} phút. Mức độ: {level}."
            ),
            "is_example": False,
        },
        {
            "title": "Bức tranh lớn",
            "body": (
                f"{title} nằm trong mảng {profile['vi']}. Ý chính của bài: {summary}\n\n"
                "Một người học vẹt thường hỏi: dùng lệnh nào? Một engineer giỏi hỏi thêm: dữ liệu đi "
                "vào là gì, giả định nào đang được dùng, output đúng được đo bằng gì, khi scale lên thì "
                "điểm nào vỡ trước, và làm sao kiểm chứng lại bằng test hoặc metric."
            ),
            "is_example": False,
        },
        {
            "title": "Mô hình trong đầu",
            "body": (
                "Hãy giữ sơ đồ này trong đầu khi đọc code:\n\n"
                f"{profile['system']}\n\n"
                "Mỗi mũi tên là một quyết định kỹ thuật. Nếu không mô tả được mũi tên đó, bạn đang "
                "dùng thư viện như một hộp đen. Mục tiêu master-level là nhìn thấy cả dữ liệu, phép "
                "biến đổi, lỗi có thể xảy ra và tín hiệu phản hồi."
            ),
            "is_example": False,
        },
        {
            "title": "Khái niệm cốt lõi",
            "body": (
                f"{concepts}\n\n"
                "Cách đọc phần này: với mỗi bullet, hãy tự viết một câu theo mẫu "
                "'nó tồn tại để giải quyết vấn đề gì'. Nếu không trả lời được, hãy quay lại ví dụ "
                "tối thiểu và đổi input để quan sát hành vi."
            ),
            "is_example": False,
        },
        {
            "title": "Ví dụ tối thiểu chạy được",
            "body": example,
            "is_example": True,
        },
        {
            "title": "Giải phẫu ví dụ",
            "body": (
                "Đừng chạy code rồi đi tiếp ngay. Hãy đọc ví dụ theo 5 lớp:\n\n"
                "1. Input: dữ liệu ban đầu là gì, type/shape ra sao.\n"
                "2. Transformation: dòng nào thật sự biến đổi dữ liệu.\n"
                "3. Output: format chính xác là gì, có khoảng trắng/dòng mới không.\n"
                "4. Invariant: điều gì vẫn phải đúng nếu input thay đổi.\n"
                "5. Failure mode: input nào khiến chương trình sai, chậm hoặc gây hiểu nhầm."
            ),
            "is_example": False,
        },
        {
            "title": "Trường hợp biên phải thử",
            "body": (
                "Checklist bắt buộc trước khi xem là hiểu bài:\n\n"
                "- Input rỗng hoặc thiếu trường.\n"
                "- Input sai kiểu, sai shape hoặc sai encoding.\n"
                "- Giá trị rất nhỏ, rất lớn, 0, None hoặc duplicate.\n"
                "- Output đúng nội dung nhưng sai format.\n"
                "- Code chạy được một ví dụ nhưng không tổng quát.\n\n"
                f"Lỗi thường gặp từ bài gốc:\n{pitfalls}"
            ),
            "is_example": False,
        },
        {
            "title": "Bài tập sandbox",
            "body": (
                f"{practice}\n\n"
                "Làm thêm 3 cấp độ:\n\n"
                "Cấp 1: hoàn thành checkpoint để output khớp tuyệt đối.\n"
                "Cấp 2: thêm một edge case và giải thích vì sao code vẫn đúng.\n"
                "Cấp 3: refactor thành function nhỏ, đặt tên rõ và tránh side effect không cần thiết."
            ),
            "is_example": False,
        },
        {
            "title": "Lab portfolio ngoài sandbox",
            "body": (
                f"{profile['lab']}\n\n"
                "Sandbox OCR chỉ nên dùng để kiểm tra lõi Python an toàn. Với bài master-level, "
                "bạn cần lưu evidence vào portfolio: notebook, test file, README ngắn, ảnh kết quả, "
                "và đoạn giải thích quyết định kỹ thuật. Đây là phần biến kiến thức thành năng lực."
            ),
            "is_example": False,
        },
        {
            "title": "Câu hỏi phỏng vấn",
            "body": (
                f"1. Nếu phải giải thích {title} cho người mới trong 60 giây, bạn nói gì?\n"
                "2. Khi input thay đổi, giả định nào trong lời giải dễ sai nhất?\n"
                "3. Bạn sẽ test happy path, edge case và failure case như thế nào?\n"
                "4. Nếu đưa phần này vào service thật, cần log/metric/alert gì?\n"
                "5. Khi nào không nên dùng kỹ thuật này?"
            ),
            "is_example": False,
        },
        {
            "title": "Rubric đạt chuẩn master",
            "body": (
                "Bạn đạt bài này khi có đủ 5 bằng chứng:\n\n"
                "- Code chạy đúng checkpoint.\n"
                "- Giải thích được bản chất mà không đọc lại định nghĩa.\n"
                "- Nêu được ít nhất 3 edge cases.\n"
                "- Có một test hoặc notebook nhỏ chứng minh hiểu biết.\n"
                "- Biết liên hệ bài học với Python/ML Engineering production workflow.\n\n"
                f"Tóm tắt gốc: {takeaway}"
            ),
            "is_example": False,
        },
    ]


def _book_sections_en(source_blocks: list[str], lesson: Any) -> list[dict[str, str]]:
    profile = _profile_for(lesson)
    title = _lesson_text(lesson, "title", "this lesson")
    summary = _lesson_text(lesson, "summary", source_blocks[5] or title)
    example = source_blocks[2]

    return [
        {
            "title": "Mastery target",
            "body": (
                f"This chapter is about {title}. By the end, you should explain the idea, "
                "write a runnable minimal example, name failure cases, and connect it to an "
                "ML Engineering workflow.\n\n"
                f"Why it matters: {summary}"
            ),
            "is_example": False,
        },
        {
            "title": "Mental model",
            "body": (
                f"Track: {profile['en']}\n\n"
                f"{profile['system']}\n\n"
                "Read every arrow as an engineering decision: what enters, what changes, what leaves, "
                "what can fail, and what signal tells you the result is trustworthy."
            ),
            "is_example": False,
        },
        {
            "title": "Core ideas",
            "body": _english_blocks(source_blocks)[1],
            "is_example": False,
        },
        {
            "title": "Runnable minimal example",
            "body": example,
            "is_example": True,
        },
        {
            "title": "Dissect the example",
            "body": (
                "Inspect the example in five passes: input type/shape, transformation, output format, "
                "invariant, and failure mode. Change one value and predict the output before running it."
            ),
            "is_example": False,
        },
        {
            "title": "Boundary cases",
            "body": (
                "- Empty or missing input.\n"
                "- Wrong type, wrong shape, or wrong encoding.\n"
                "- Very small, very large, zero, None, or duplicate values.\n"
                "- Correct-looking content with incorrect output formatting.\n"
                "- A solution that passes one example but does not generalize."
            ),
            "is_example": False,
        },
        {
            "title": "Sandbox practice",
            "body": (
                "Level 1: pass the checkpoint exactly.\n"
                "Level 2: add one edge case and explain why the code still works.\n"
                "Level 3: refactor into a small function with a clear name and minimal side effects."
            ),
            "is_example": False,
        },
        {
            "title": "Portfolio lab",
            "body": (
                f"{profile['lab']}\n\n"
                "The OCR sandbox checks a safe Python core. Mastery needs evidence: a notebook or test file, "
                "a short README, and a written explanation of the engineering tradeoffs."
            ),
            "is_example": False,
        },
        {
            "title": "Interview checks",
            "body": (
                f"1. Explain {title} in 60 seconds.\n"
                "2. Which assumption fails first when input changes?\n"
                "3. What would you test for happy path, edge case, and failure case?\n"
                "4. What logs, metrics, or alerts would production need?\n"
                "5. When should this technique not be used?"
            ),
            "is_example": False,
        },
        {
            "title": "Mastery rubric",
            "body": (
                "- The checkpoint passes.\n"
                "- You can explain the concept without reading a definition.\n"
                "- You can name at least three edge cases.\n"
                "- You have a tiny test or notebook as evidence.\n"
                "- You can connect the lesson to production Python or ML Engineering."
            ),
            "is_example": False,
        },
    ]


def book_lesson_sections(content: str, language: str, lesson: Any | None = None) -> list[dict[str, str]]:
    """Return book-like chapter sections for lesson pages."""
    if lesson is None:
        return lesson_sections(content, language)

    source_blocks = _split_source_content(content)
    if language == "en":
        return _book_sections_en(source_blocks, lesson)
    return _book_sections_vi(source_blocks, lesson)
