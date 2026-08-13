"""Bilingual UI vocabulary for the learner-facing interface."""

from __future__ import annotations

from typing import Final
from copy import deepcopy


LANGUAGE_SESSION_KEY: Final = "learning_ui_language"
SUPPORTED_LANGUAGES: Final = {"vi", "en"}

UI_COPY: Final = {
    "vi": {
        "site_title": "PyPath · Học Python thực chiến",
        "learning_path": "Lộ trình học",
        "login": "Đăng nhập",
        "start_free": "Bắt đầu miễn phí",
        "logout": "Đăng xuất",
        "roadmap_eyebrow": "Bản đồ năng lực tổng quan",
        "roadmap_title": "Từ Python căn bản đến",
        "roadmap_emphasis": "ML Engineer có portfolio.",
        "roadmap_description": "Sáu chặng năng lực dẫn bạn từ nền tảng code và toán đến xây dựng, triển khai và vận hành sản phẩm AI.",
        "browse_lessons": "Duyệt toàn bộ",
        "lesson_word": "bài",
        "lesson_content": "NỘI DUNG BÀI HỌC",
        "quick_visual": "MINH HỌA NHANH",
        "mental_map": "Bản đồ tư duy của bài này",
        "understand_why": "Hiểu bản chất",
        "practice_now": "Thực hành ngay",
        "footer_tagline": "Học Python từng dòng lệnh, tiến bộ từng bài tập.",
        "language": "Ngôn ngữ",
        "language_vi": "Tiếng Việt",
        "language_en": "English",
        "language_current": "Tiếng Việt",
        "quick_menu": "Mở menu nhanh",
        "profile_menu": "Mở menu tài khoản",
        "signed_in_as": "Đang đăng nhập với",
        "theme": "Giao diện",
        "theme_light": "Sáng",
        "theme_dark": "Tối",
        "phase": "Chặng",
        "minutes": "phút",
        "roadmap_phase_summary": "chặng năng lực",
        "roadmap_track_summary": "track chuyên sâu",
        "roadmap_checkpoint_summary": "bài học & checkpoint",
        "hero_title": "Học sâu.",
        "hero_emphasis": "Xây thật.",
        "hero_description": "Lộ trình Master Python & ML Engineering: từ code, toán cho AI và dữ liệu đến ML/DL, MLOps, LLM/RAG, Django và FastAPI. Mỗi bài có checkpoint OCR an toàn cùng lab thực chiến định hướng portfolio.",
        "hero_roadmap_cta": "Xem bản đồ lộ trình",
        "hero_register_cta": "Tạo tài khoản miễn phí",
        "hero_lessons": "bài học có cấu trúc",
        "hero_tracks": "chặng năng lực",
        "hero_ocr": "checkpoint code an toàn",
        "concept_intro": "Đừng chỉ đọc lý thuyết. Hãy nhìn topic như một hệ thống có dữ liệu vào, phép biến đổi, lỗi biên và vòng phản hồi.",
        "concept_mental_model": "Mô hình trong đầu",
        "concept_pipeline": "Pipeline xử lý",
        "concept_edge_cases": "Trường hợp biên",
        "concept_mistakes": "Lỗi hay gặp",
        "concept_practice_loop": "Vòng thực hành",
        "library_eyebrow": "Đi sâu theo track hoặc chủ đề bạn cần",
        "library_title": "Thư viện học theo từng chặng",
        "lessons_open": "bài học đang mở",
        "search_lessons": "Tìm bài học",
        "search_placeholder": "Tìm Python, đạo hàm, MLOps, RAG…",
        "filter_tracks": "Lọc theo chặng học",
        "all": "Tất cả",
        "no_matching_lessons": "Không có bài phù hợp. Hãy thử từ khóa khác.",
        "checkpoint": "checkpoint",
        "practice": "thực hành",
        "open_lesson": "Mở bài học",
        "no_public_lessons": "Chưa có bài học công khai",
        "admin_can_add": "Quản trị viên có thể thêm nội dung trong",
        "lesson": "Bài",
        "challenge": "Thử thách",
        "practice_exercises": "bài thực hành",
        "apply_lesson": "Áp dụng nội dung vừa học vào các thử thách nhỏ.",
        "no_exercises": "Bài học này chưa có thử thách.",
        "back_to_path": "Quay về lộ trình",
        "programming_challenge": "Thử thách lập trình",
        "exercise_intro": "Hoàn thành lời giải, chụp ảnh phần code rồi gửi để nhận kết quả tức thì.",
        "code_timeout": "Tối đa {seconds} giây chạy code",
        "requirements": "Yêu cầu",
        "starter_code": "MẪU KHỞI ĐẦU",
        "tip": "Mẹo",
        "photo_tip": "Chụp ảnh rõ nét, không che phần code và đảm bảo toàn bộ lời giải nằm trong khung hình.",
        "sandbox_title": "Chạy thử trước khi nộp OCR",
        "optional_stdin": "stdin tùy chọn",
        "stdin_placeholder": "Dữ liệu nhập mô phỏng input(), mỗi dòng là một lần nhập",
        "run_code": "Chạy code",
        "restore_sample": "Khôi phục mẫu",
        "sandbox_ready": "Sẵn sàng chạy trong sandbox FastAPI.",
        "result": "Kết quả",
        "login_to_run": "Đăng nhập để chạy sandbox",
        "submit": "Nộp bài",
        "submit_code": "Gửi code của bạn",
        "choose_photo": "Chọn ảnh chụp code",
        "submit_for_grading": "Gửi để chấm bài",
        "back_to_exercise": "Quay lại bài tập",
        "try_again": "Thử lại ngay",
        "upload_intro": "Ảnh của bạn sẽ được OCR đọc code và chạy trong môi trường sandbox an toàn.",
        "image_formats": "PNG, JPG hoặc WebP · tối đa 5 MB",
        "privacy_note": "Code chỉ được chạy trong sandbox cô lập",
        "login_to_submit_intro": "Đăng nhập để lưu lời giải, nhận kết quả từ OCR và xem lại lịch sử nộp bài.",
        "login_to_submit": "Đăng nhập để nộp bài",
        "no_account": "Chưa có tài khoản?",
        "create_free": "Tạo miễn phí",
        "submission_result": "Kết quả bài nộp",
        "submission_passed": "Xuất sắc, bạn đã đúng!",
        "submission_failed": "Sắp đúng rồi, thử lại nhé",
        "submission_review": "Bài nộp cần được kiểm tra",
        "sent_at": "Gửi lúc",
        "ocr_confidence": "Độ tin cậy OCR",
        "processing_status": "Trạng thái xử lý",
        "exercise": "Bài tập",
        "ocr_code": "Code được OCR nhận diện",
        "program_output": "Kết quả chạy chương trình",
        "grader_note": "Nhận xét từ trình chấm",
        "welcome_back": "Chào mừng trở lại",
        "login_heading": "Tiếp tục hành trình viết code của bạn.",
        "login_description": "Mở lại bài học, nộp lời giải và xem kết quả chấm OCR ở một nơi.",
        "sign_in": "Đăng nhập",
        "username": "Tên đăng nhập",
        "password": "Mật khẩu",
        "no_account_yet": "Chưa có tài khoản?",
        "begin_free": "Bắt đầu miễn phí",
        "start_free_eyebrow": "Bắt đầu miễn phí",
        "register_heading": "Học bằng cách tự tay viết code.",
        "register_description": "Chọn một bài học, hoàn thành thử thách nhỏ và nhận phản hồi nhanh cho từng lời giải.",
        "create_account": "Tạo tài khoản",
        "confirm_password": "Xác nhận mật khẩu",
        "already_account": "Đã có tài khoản?",
    },
    "en": {
        "site_title": "PyPath · Practical Python Learning",
        "learning_path": "Learning path",
        "login": "Sign in",
        "start_free": "Start free",
        "logout": "Sign out",
        "roadmap_eyebrow": "Capability roadmap",
        "roadmap_title": "From Python foundations to an",
        "roadmap_emphasis": "ML Engineer portfolio.",
        "roadmap_description": "Six capability stages take you from code and math foundations to building, deploying, and operating AI products.",
        "browse_lessons": "Browse all",
        "lesson_word": "lessons",
        "lesson_content": "LESSON CONTENT",
        "quick_visual": "QUICK VISUAL",
        "mental_map": "The mental model for this lesson",
        "understand_why": "Understand the why",
        "practice_now": "Practice now",
        "footer_tagline": "Learn Python line by line, improve exercise by exercise.",
        "language": "Language",
        "language_vi": "Vietnamese",
        "language_en": "English",
        "language_current": "English",
        "quick_menu": "Open quick menu",
        "profile_menu": "Open account menu",
        "signed_in_as": "Signed in as",
        "theme": "Theme",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "phase": "Phase",
        "minutes": "min",
        "roadmap_phase_summary": "capability stages",
        "roadmap_track_summary": "specialist tracks",
        "roadmap_checkpoint_summary": "lessons & checkpoints",
        "hero_title": "Learn deeply.",
        "hero_emphasis": "Build for real.",
        "hero_description": "A Master Python & ML Engineering path: from code, AI math, and data to ML/DL, MLOps, LLM/RAG, Django, and FastAPI. Every lesson includes a safe OCR checkpoint and a practical portfolio-oriented lab.",
        "hero_roadmap_cta": "View the roadmap",
        "hero_register_cta": "Create a free account",
        "hero_lessons": "structured lessons",
        "hero_tracks": "capability tracks",
        "hero_ocr": "safe code checkpoint",
        "concept_intro": "Do not only read theory. Treat the topic as a system with input data, a transformation, boundary cases, and a feedback loop.",
        "concept_mental_model": "Mental model",
        "concept_pipeline": "Processing pipeline",
        "concept_edge_cases": "Boundary cases",
        "concept_mistakes": "Common mistakes",
        "concept_practice_loop": "Practice loop",
        "library_eyebrow": "Go deeper by track or by the topic you need",
        "library_title": "Learning library by stage",
        "lessons_open": "lessons available",
        "search_lessons": "Search lessons",
        "search_placeholder": "Search Python, calculus, MLOps, RAG…",
        "filter_tracks": "Filter learning stages",
        "all": "All",
        "no_matching_lessons": "No matching lessons. Try another keyword.",
        "checkpoint": "checkpoints",
        "practice": "practice",
        "open_lesson": "Open lesson",
        "no_public_lessons": "No public lessons yet",
        "admin_can_add": "An administrator can add content in",
        "lesson": "Lesson",
        "challenge": "Challenge",
        "practice_exercises": "practice exercises",
        "apply_lesson": "Apply what you just learned in short challenges.",
        "no_exercises": "This lesson has no challenges yet.",
        "back_to_path": "Back to learning path",
        "programming_challenge": "Programming challenge",
        "exercise_intro": "Complete your solution, capture the code, and submit it for immediate feedback.",
        "code_timeout": "Up to {seconds} seconds to run code",
        "requirements": "Requirements",
        "starter_code": "STARTER CODE",
        "tip": "Tip",
        "photo_tip": "Use a sharp photo, keep code unobstructed, and include the whole solution in frame.",
        "sandbox_title": "Run it before OCR submission",
        "optional_stdin": "optional stdin",
        "stdin_placeholder": "Input to simulate input(); one value per line",
        "run_code": "Run code",
        "restore_sample": "Restore sample",
        "sandbox_ready": "Ready to run in the FastAPI sandbox.",
        "result": "Result",
        "login_to_run": "Sign in to run the sandbox",
        "submit": "Submit",
        "submit_code": "Send your code",
        "choose_photo": "Choose a code photo",
        "submit_for_grading": "Submit for grading",
        "back_to_exercise": "Back to exercise",
        "try_again": "Try again",
        "upload_intro": "Your image is read by OCR and executed in an isolated, safe sandbox.",
        "image_formats": "PNG, JPG, or WebP · 5 MB maximum",
        "privacy_note": "Code runs only in an isolated sandbox",
        "login_to_submit_intro": "Sign in to save your solution, receive OCR feedback, and review submission history.",
        "login_to_submit": "Sign in to submit",
        "no_account": "No account yet?",
        "create_free": "Create one free",
        "submission_result": "Submission result",
        "submission_passed": "Excellent — your answer is correct!",
        "submission_failed": "Almost there — try again.",
        "submission_review": "Your submission needs review",
        "sent_at": "Submitted",
        "ocr_confidence": "OCR confidence",
        "processing_status": "Processing status",
        "exercise": "Exercise",
        "ocr_code": "Code recognized by OCR",
        "program_output": "Program output",
        "grader_note": "Grader feedback",
        "welcome_back": "Welcome back",
        "login_heading": "Continue your coding journey.",
        "login_description": "Resume lessons, submit solutions, and review OCR grading in one place.",
        "sign_in": "Sign in",
        "username": "Username",
        "password": "Password",
        "no_account_yet": "No account yet?",
        "begin_free": "Start free",
        "start_free_eyebrow": "Start free",
        "register_heading": "Learn by writing code yourself.",
        "register_description": "Choose a lesson, complete a small challenge, and get fast feedback on every solution.",
        "create_account": "Create account",
        "confirm_password": "Confirm password",
        "already_account": "Already have an account?",
    },
}

ROADMAP_ENGLISH: Final = {
    "foundation": {"title": "Programming foundations", "description": "Clean Python, algorithmic thinking, and an engineering workflow.", "outcome": "Write, test, and package production-ready Python with confidence."},
    "math-data": {"title": "Math & Data", "description": "The language of representations, gradients, uncertainty, and data.", "outcome": "Build intuition for loss, gradients, probability, and data pipelines."},
    "core-ml": {"title": "AI & Machine Learning", "description": "Problem framing, training, validation, and classical model operations.", "outcome": "Take an ML baseline from the right metric to an observable service."},
    "deep-learning": {"title": "Deep Learning", "description": "PyTorch, backpropagation, and effective training loops.", "outcome": "Design, debug, and optimize deep-learning pipelines intentionally."},
    "specialization": {"title": "AI specialization", "description": "Vision, NLP, GenAI/RAG, and reinforcement learning.", "outcome": "Choose the right technique for a concrete AI problem instead of following hype."},
    "ship": {"title": "Build & Ship", "description": "Django, FastAPI, and capstones that bring ML capabilities to users.", "outcome": "Ship an evaluated, deployed ML system with a clear technical story."},
}

TRACK_ENGLISH: Final = {
    "python": "Python", "python_pro": "Python Pro", "engineering": "Engineering",
    "math": "AI Math", "statistics": "Probability", "data": "Data",
    "ai": "AI", "ml": "Machine Learning", "mlops": "MLOps", "dl": "Deep Learning",
    "cv": "Computer Vision", "nlp": "NLP", "genai": "GenAI", "rl": "Reinforcement Learning",
    "django": "Django", "fastapi": "FastAPI", "capstone": "Capstone",
}

TRACK_ENGLISH_PRESENTATION: Final = {
    "python": ("Programming foundations", "Python foundations", "Syntax, data, algorithms, tests, JSON, and HTTP."),
    "python_pro": ("Programming foundations", "Professional Python", "Async code, typing, packages, performance, security, and architecture."),
    "engineering": ("Programming foundations", "Engineering workflow", "Git, SQL, testing, Docker, CI/CD, and application safety."),
    "math": ("AI mathematics", "Linear algebra & calculus", "Vectors, matrices, derivatives, gradients, and optimization."),
    "statistics": ("AI mathematics", "Probability & statistics", "Distributions, Bayes, estimation, testing, and information."),
    "data": ("Data foundations", "Data engineering & analytics", "NumPy, pandas, SQL, EDA, data quality, and pipelines."),
    "ai": ("AI foundations", "Artificial intelligence", "Problem framing, data, evaluation, safety, privacy, and governance."),
    "ml": ("Machine learning", "Machine learning", "Tabular models, validation, metrics, features, and system design."),
    "mlops": ("Machine learning", "ML Engineering & MLOps", "Reproducibility, serving, CI/CD, monitoring, drift, and SLOs."),
    "dl": ("Deep learning", "Deep learning", "Autograd, training loops, CNNs, Transformers, and optimized inference."),
    "cv": ("AI specialization", "Computer vision", "Images, detection, segmentation, OCR, vision transformers, and edge deployment."),
    "nlp": ("AI specialization", "NLP & language models", "Tokenization, embeddings, retrieval, multilingual NLP, and Document AI."),
    "genai": ("AI specialization", "Generative AI, RAG & agents", "Prompts, RAG, tool use, evaluation, safety, and LLM observability."),
    "rl": ("AI specialization", "Reinforcement learning", "MDPs, Bellman equations, Q-learning, policy gradients, and safe offline RL."),
    "django": ("Building AI products", "Django web development", "MVT, ORM, auth, DRF, background jobs, and deployment."),
    "fastapi": ("Building AI products", "FastAPI & microservices", "Pydantic, async APIs, OAuth, queues, resilience, and observability."),
    "capstone": ("Portfolio & career", "Capstone & portfolio", "End-to-end projects, evaluation reports, deployment, and system design."),
}


def current_language(request) -> str:
    """Return the supported language selected for this browser session."""
    language = request.session.get(LANGUAGE_SESSION_KEY, "vi")
    return language if language in SUPPORTED_LANGUAGES else "vi"


def learner_ui(request):
    """Expose selected vocabulary to every Django template."""
    language = current_language(request)
    return {"ui_language": language, "ui": UI_COPY[language]}


def localize_roadmap(language: str, stages: list[dict]) -> list[dict]:
    """Translate roadmap presentation data without mutating curriculum records."""
    if language != "en":
        return stages

    localized = deepcopy(stages)
    for stage in localized:
        stage.update(ROADMAP_ENGLISH.get(stage["key"], {}))
        for track in stage["tracks"]:
            track["short_title"] = TRACK_ENGLISH.get(track["key"], track["short_title"])
    return localized


def localize_curriculum(language: str, sections: list[dict]) -> list[dict]:
    """Attach safe display copy for every curriculum card without changing data."""
    for section in sections:
        phase, title, description = TRACK_ENGLISH_PRESENTATION.get(
            section["key"], (section["phase"], section["title"], section["description"])
        )
        if language == "en":
            section["display_phase"] = phase
            section["display_title"] = title
            section["display_short_title"] = TRACK_ENGLISH.get(
                section["key"], section["short_title"]
            )
            section["display_description"] = description
        else:
            section["display_phase"] = section["phase"]
            section["display_title"] = section["title"]
            section["display_short_title"] = section["short_title"]
            section["display_description"] = section["description"]

        for position, lesson in enumerate(section["lessons"], start=1):
            if language == "en":
                lesson.display_title = f"{section['display_short_title']} · Lesson {position:02d}"
                lesson.display_summary = (
                    f"A structured {section['display_title'].lower()} practice lesson."
                )
                for exercise_position, exercise in enumerate(lesson.exercises.all(), start=1):
                    exercise.display_title = (
                        f"{section['display_short_title']} · Practice {exercise_position:02d}"
                    )
            else:
                lesson.display_title = lesson.title
                lesson.display_summary = lesson.summary
                for exercise in lesson.exercises.all():
                    exercise.display_title = exercise.title
    return sections


def lesson_display(language: str, lesson) -> dict:
    """Return language-safe lesson labels for detail pages."""
    track = TRACK_ENGLISH_PRESENTATION.get(lesson.track)
    if language != "en" or not track:
        return {"title": lesson.title, "summary": lesson.summary, "track": lesson.get_track_display()}
    return {
        "title": f"{TRACK_ENGLISH.get(lesson.track, 'Learning')} · Lesson {lesson.order:02d}",
        "summary": f"A structured practice lesson in {track[1].lower()}.",
        "track": track[1],
    }


def exercise_display(language: str, exercise) -> dict:
    """Return safe challenge presentation when the source curriculum is Vietnamese."""
    if language != "en":
        return {"title": exercise.title, "prompt": exercise.prompt}
    track_name = TRACK_ENGLISH.get(exercise.lesson.track, "Learning")
    return {
        "title": f"{track_name} · Practice {exercise.order:02d}",
        "prompt": (
            "Use Python's standard library to complete this checkpoint. "
            "Run your code in the sandbox and verify its output before submitting OCR."
        ),
    }
