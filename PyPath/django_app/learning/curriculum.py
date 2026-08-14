"""Declarative, create-only curriculum content for the learning platform.

The OCR sandbox intentionally runs only Python's standard library. Lessons can
teach framework and ML-library concepts, while their image-submission exercises
remain executable in the isolated grading environment.
"""

from __future__ import annotations

import re
from textwrap import dedent
from typing import Any

from .curriculum_content.mastery import build_master_curriculum


def _bullet_list(items: tuple[str, ...]) -> str:
    """Format a concise learner-facing bulleted list."""
    return "\n".join(f"- {item}" for item in items)


def _lesson_content(
    *,
    objective: str,
    concepts: tuple[str, ...],
    example: str,
    pitfalls: tuple[str, ...],
    takeaway: str,
) -> str:
    """Build consistent, readable plain-text lesson content."""
    return dedent(
        f"""\
        Mục tiêu
        {objective}

        Khái niệm chính
        {_bullet_list(concepts)}

        Ví dụ tối thiểu
        {example}

        Cách học hiệu quả
        1. Đọc ví dụ và tự dự đoán output trước khi chạy.
        2. Thay đổi một giá trị nhỏ để quan sát chương trình phản hồi.
        3. Hoàn thành thử thách bằng code của chính bạn, rồi chụp rõ phần code.

        Lỗi thường gặp
        {_bullet_list(pitfalls)}

        Tóm tắt
        {takeaway}
        """
    ).strip()


def _exercise(
    *,
    key: str,
    slug: str,
    title: str,
    prompt: str,
    starter_code: str,
    expected_output: str,
    test_input: str = "",
) -> dict[str, Any]:
    """Create a sandbox-compatible exercise specification."""
    return {
        "curriculum_key": key,
        "slug": slug,
        "title": title,
        "prompt": (
            f"{prompt}\n\n"
            "Viết lời giải bằng Python standard library, chạy thử rồi chụp rõ "
            "toàn bộ phần code để nộp cho OCR grader."
        ),
        "starter_code": dedent(starter_code).strip() + "\n",
        "expected_output": expected_output,
        "test_input": test_input,
        "timeout_seconds": 3,
        "order": 1,
        "is_published": True,
    }


def _lesson_slug(key: str) -> str:
    """Derive a readable slug by removing the sequence segment from a key."""
    return re.sub(r"-\d{2}-", "-", key, count=1)


def _lesson(
    *,
    key: str,
    track: str,
    level: str,
    order: int,
    minutes: int,
    title: str,
    summary: str,
    objective: str,
    concepts: tuple[str, ...],
    example: str,
    pitfalls: tuple[str, ...],
    takeaway: str,
    exercise: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Create one lesson and its first OCR-submittable practice exercise."""
    return {
        "lesson": {
            "curriculum_key": key,
            "track": track,
            "level": level,
            "order": order,
            "estimated_minutes": minutes,
            "title": title,
            "slug": _lesson_slug(key),
            "summary": summary,
            "content": _lesson_content(
                objective=objective,
                concepts=concepts,
                example=example,
                pitfalls=pitfalls,
                takeaway=takeaway,
            ),
            "is_published": True,
        },
        "exercises": (exercise,) if exercise is not None else (),
    }


# The keys are stable identifiers. They are never displayed to learners and
# let the seed command preserve admin-edited titles, slugs, and content.
BASE_CURRICULUM: tuple[dict[str, Any], ...] = (
    _lesson(
        key="python-01-print",
        track="python",
        level="beginner",
        order=1,
        minutes=20,
        title="Python 01 · print() và chương trình đầu tiên",
        summary="In văn bản, số và kết quả biểu thức để làm quen với luồng chạy Python.",
        objective="Biết cách chạy một file Python và đưa dữ liệu ra màn hình bằng print().",
        concepts=(
            "Python chạy câu lệnh từ trên xuống dưới.",
            "print() hiển thị string, số hoặc kết quả của biểu thức.",
            "Comment bắt đầu bằng # để giải thích code mà không thực thi.",
        ),
        example='print("Hello, Python!")\nprint(2 + 3)',
        pitfalls=(
            "Quên dấu nháy khi in string.",
            "Viết Print thay vì print vì Python phân biệt chữ hoa/chữ thường.",
        ),
        takeaway="Mọi chương trình Python bắt đầu từ các câu lệnh nhỏ, rõ ràng và có thể chạy được.",
        exercise=_exercise(
            key="python-01-print-greeting",
            slug="print-hello-python",
            title="In lời chào Python",
            prompt="In chính xác một dòng: Hello, Python!",
            starter_code="""
            # TODO: in lời chào chính xác
            """,
            expected_output="Hello, Python!",
        ),
    ),
    _lesson(
        key="python-02-variables-input",
        track="python",
        level="beginner",
        order=2,
        minutes=28,
        title="Python 02 · Biến, kiểu dữ liệu và input()",
        summary="Lưu dữ liệu và đọc giá trị từ bàn phím một cách an toàn.",
        objective="Lưu giá trị vào biến, nhận biết kiểu cơ bản và dùng input() để đọc dữ liệu.",
        concepts=(
            "str, int, float và bool mô tả các kiểu dữ liệu thường gặp.",
            "input() luôn trả về string; dùng int() hoặc float() khi cần tính toán.",
            "strip() loại bỏ khoảng trắng thừa ở đầu và cuối dữ liệu nhập.",
        ),
        example='name = input().strip()\nprint(f"Hello, {name}!")',
        pitfalls=(
            "Cộng trực tiếp input() với số trước khi ép kiểu.",
            "Đặt tên biến là list, str hoặc sum làm che built-in hữu ích.",
        ),
        takeaway="Biến biến dữ liệu đầu vào thành giá trị mà chương trình có thể xử lý.",
        exercise=_exercise(
            key="python-02-variables-input-greeting",
            slug="python-input-greeting",
            title="Chào người dùng từ input",
            prompt="Đọc một tên từ stdin và in Hello, <tên>!", 
            starter_code="""
            name = input().strip()
            # TODO: in lời chào
            """,
            expected_output="Hello, Ada!",
            test_input="Ada\n",
        ),
    ),
    _lesson(
        key="python-03-operators-casting",
        track="python",
        level="beginner",
        order=3,
        minutes=25,
        title="Python 03 · Toán tử và chuyển đổi kiểu",
        summary="Tính toán, so sánh và ép kiểu dữ liệu đúng thời điểm.",
        objective="Dùng toán tử số học, so sánh và logic để tạo biểu thức chính xác.",
        concepts=(
            "+, -, *, /, //, % và ** phục vụ các phép toán khác nhau.",
            "== so sánh giá trị, còn = dùng để gán giá trị.",
            "int(), float() và str() chuyển đổi kiểu có chủ đích.",
        ),
        example='age = int("18")\nprint(age >= 18 and age < 65)',
        pitfalls=(
            "Nhầm / với // khi cần chia lấy phần nguyên.",
            "So sánh float bằng == trong các bài toán cần độ chính xác cao.",
        ),
        takeaway="Một biểu thức rõ kiểu dữ liệu sẽ ít gây lỗi hơn và dễ đọc hơn.",
        exercise=_exercise(
            key="python-03-operators-casting-sum-product",
            slug="python-operators-sum-product",
            title="Tính tổng và tích",
            prompt="Dùng left = 7 và right = 3, in tổng ở dòng đầu và tích ở dòng thứ hai.",
            starter_code="""
            left = 7
            right = 3
            # TODO: in tổng rồi tích
            """,
            expected_output="10\n21",
        ),
    ),
    _lesson(
        key="python-04-strings-fstrings",
        track="python",
        level="beginner",
        order=4,
        minutes=30,
        title="Python 04 · Chuỗi và f-string",
        summary="Xử lý, cắt và định dạng text rõ ràng với f-string.",
        objective="Thao tác với string mà không tạo code khó đọc hoặc ghép chuỗi lỗi.",
        concepts=(
            "String là immutable; mỗi phép biến đổi thường tạo giá trị mới.",
            "Index và slice giúp lấy phần mong muốn của text.",
            "f-string là cách dễ đọc để chèn biến vào câu thông báo.",
        ),
        example='language = "Python"\nprint(f"I learn {language.lower()}")',
        pitfalls=(
            "Truy cập index vượt quá độ dài chuỗi.",
            "Quên ký tự f trước dấu nháy của f-string.",
        ),
        takeaway="String tốt không chỉ đúng mà còn giúp thông báo với người dùng dễ hiểu.",
        exercise=_exercise(
            key="python-04-strings-fstrings-version",
            slug="python-fstring-version",
            title="Định dạng phiên bản Python",
            prompt="Dùng f-string để in Python 3.12 từ hai biến đã cho.",
            starter_code="""
            language = "Python"
            version = 3.12
            # TODO: dùng f-string
            """,
            expected_output="Python 3.12",
        ),
    ),
    _lesson(
        key="python-05-collections",
        track="python",
        level="beginner",
        order=5,
        minutes=35,
        title="Python 05 · List, tuple, set và dict",
        summary="Chọn cấu trúc dữ liệu phù hợp để lưu, tra cứu và lặp dữ liệu.",
        objective="Phân biệt bốn collection cốt lõi và biết trường hợp nên dùng mỗi loại.",
        concepts=(
            "list có thứ tự và có thể thay đổi.",
            "tuple phù hợp dữ liệu cố định, set tối ưu membership không trùng.",
            "dict ánh xạ key sang value để tra cứu rõ ràng.",
        ),
        example='profile = {"name": "Ada", "skills": ["Python", "AI"]}\nprint(profile["name"])',
        pitfalls=(
            "Dùng index với dict thay vì key.",
            "Tin rằng set luôn giữ thứ tự ổn định.",
        ),
        takeaway="Collection phù hợp làm code đơn giản hơn trước khi cần thuật toán phức tạp.",
        exercise=_exercise(
            key="python-05-collections-score-summary",
            slug="python-collections-score-summary",
            title="Tóm tắt danh sách điểm",
            prompt="In số lượng phần tử, sau đó in điểm cuối cùng trong scores.",
            starter_code="""
            scores = [8, 9, 10]
            # TODO: in số phần tử rồi phần tử cuối
            """,
            expected_output="3\n10",
        ),
    ),
    _lesson(
        key="python-06-conditionals",
        track="python",
        level="beginner",
        order=6,
        minutes=25,
        title="Python 06 · Rẽ nhánh với if/elif/else",
        summary="Điều khiển luồng chương trình theo điều kiện một cách dễ đọc.",
        objective="Viết branch logic rõ ràng với điều kiện boolean và các trường hợp biên.",
        concepts=(
            "if kiểm tra điều kiện đầu tiên đúng, elif thêm nhánh, else là fallback.",
            "So sánh chuỗi và số cần đúng kiểu dữ liệu.",
            "Guard clause giúp giảm số tầng thụt lề.",
        ),
        example='score = 72\nif score >= 50:\n    print("Passed")\nelse:\n    print("Try again")',
        pitfalls=(
            "Thụt lề không nhất quán.",
            "Dùng nhiều if riêng lẻ khi các điều kiện loại trừ lẫn nhau.",
        ),
        takeaway="Điều kiện tốt diễn đạt quy tắc nghiệp vụ thay vì che giấu nó trong nhiều nhánh.",
        exercise=_exercise(
            key="python-06-conditionals-passed",
            slug="python-conditionals-passed",
            title="Xác định trạng thái đạt",
            prompt="In Passed nếu score lớn hơn hoặc bằng 50, nếu không in Try again.",
            starter_code="""
            score = 72
            # TODO: viết điều kiện
            """,
            expected_output="Passed",
        ),
    ),
    _lesson(
        key="python-07-loops",
        track="python",
        level="beginner",
        order=7,
        minutes=30,
        title="Python 07 · Vòng lặp for, while và range",
        summary="Lặp có kiểm soát, xử lý dãy dữ liệu và tránh vòng lặp vô hạn.",
        objective="Chọn for hoặc while đúng bài toán và theo dõi biến lặp rõ ràng.",
        concepts=(
            "for duyệt collection hoặc range; while lặp khi điều kiện còn đúng.",
            "range(start, stop) không bao gồm stop.",
            "break và continue hữu ích nhưng không nên che logic chính.",
        ),
        example='for number in range(1, 4):\n    print(number * number)',
        pitfalls=(
            "Quên cập nhật biến điều kiện trong while.",
            "Nhầm range(1, 4) sẽ có số 4.",
        ),
        takeaway="Vòng lặp đáng tin cậy luôn có điều kiện dừng và một mục đích rõ ràng.",
        exercise=_exercise(
            key="python-07-loops-squares",
            slug="python-loops-squares",
            title="In bình phương",
            prompt="Dùng vòng lặp để in bình phương các số 1, 2, 3; mỗi kết quả một dòng.",
            starter_code="""
            for number in range(1, 4):
                # TODO: in bình phương
                pass
            """,
            expected_output="1\n4\n9",
        ),
    ),
    _lesson(
        key="python-08-functions",
        track="python",
        level="beginner",
        order=8,
        minutes=35,
        title="Python 08 · Hàm, return và docstring",
        summary="Đóng gói logic thành các hàm có thể tái sử dụng và kiểm thử.",
        objective="Phân biệt print với return và thiết kế hàm có input/output rõ ràng.",
        concepts=(
            "Hàm nhận tham số, thực hiện một trách nhiệm và trả kết quả bằng return.",
            "Docstring giải thích mục đích, input và output của hàm.",
            "Hàm thuần dễ unit test vì không phụ thuộc trạng thái bên ngoài.",
        ),
        example='def double(value):\n    """Return value multiplied by two."""\n    return value * 2\n\nprint(double(6))',
        pitfalls=(
            "In giá trị khi caller cần kết quả để dùng tiếp.",
            "Tạo hàm quá dài, làm nhiều trách nhiệm cùng lúc.",
        ),
        takeaway="Hàm nhỏ, có tên tốt là nền tảng cho code AI và web có thể bảo trì.",
        exercise=_exercise(
            key="python-08-functions-double",
            slug="python-functions-double",
            title="Viết hàm double",
            prompt="Hoàn thành hàm double(value) và in double(6).",
            starter_code="""
            def double(value):
                # TODO: trả về gấp đôi value
                pass

            print(double(6))
            """,
            expected_output="12",
        ),
    ),
    _lesson(
        key="python-09-parameters-scope",
        track="python",
        level="intermediate",
        order=9,
        minutes=28,
        title="Python 09 · Tham số, scope và hàm dùng lại",
        summary="Dùng default parameter và hiểu phạm vi biến để tránh side effect.",
        objective="Thiết kế API hàm dễ gọi với tham số mặc định và keyword argument.",
        concepts=(
            "Biến local chỉ tồn tại trong thân hàm.",
            "Default parameter giúp lời gọi phổ biến ngắn hơn.",
            "Không dùng list/dict mutable làm default argument.",
        ),
        example='def welcome(name="Learner"):\n    return f"Hello, {name}!"\n\nprint(welcome())',
        pitfalls=(
            "Sửa biến global từ trong hàm khi có thể return giá trị mới.",
            "Dùng [] làm default rồi bị chia sẻ trạng thái giữa các lần gọi.",
        ),
        takeaway="Scope đúng giúp hàm dự đoán được và dễ tái sử dụng trong project lớn.",
        exercise=_exercise(
            key="python-09-parameters-scope-welcome",
            slug="python-parameters-welcome",
            title="Lời chào có mặc định",
            prompt="Hoàn thành hàm welcome để in hai lời chào theo output mong đợi.",
            starter_code="""
            def welcome(name="Learner"):
                # TODO
                pass

            print(welcome())
            print(welcome("Ada"))
            """,
            expected_output="Hello, Learner!\nHello, Ada!",
        ),
    ),
    _lesson(
        key="python-10-comprehensions",
        track="python",
        level="intermediate",
        order=10,
        minutes=30,
        title="Python 10 · Comprehension, unpacking và biểu thức gọn",
        summary="Viết thao tác dữ liệu ngắn gọn mà vẫn dễ đọc.",
        objective="Dùng list/dict comprehension khi nó làm ý định code rõ hơn vòng lặp dài.",
        concepts=(
            "Comprehension tạo collection mới từ iterable có thể kèm điều kiện.",
            "Unpacking tách cấu trúc thành biến có tên.",
            "Dừng tối ưu cú pháp khi expression trở nên khó đọc.",
        ),
        example='numbers = [1, 2, 3, 4]\neven_squares = [n * n for n in numbers if n % 2 == 0]\nprint(even_squares)',
        pitfalls=(
            "Nhét nhiều điều kiện và side effect vào một comprehension.",
            "Đặt tên n chung chung khi logic phức tạp.",
        ),
        takeaway="Cú pháp ngắn chỉ tốt khi người đọc vẫn hiểu dữ liệu đang biến đổi như thế nào.",
        exercise=_exercise(
            key="python-10-comprehensions-even-squares",
            slug="python-comprehensions-even-squares",
            title="Bình phương số chẵn",
            prompt="Tạo even_squares gồm bình phương các số chẵn và in list đó.",
            starter_code="""
            numbers = [1, 2, 3, 4]
            # TODO: tạo even_squares
            print(even_squares)
            """,
            expected_output="[4, 16]",
        ),
    ),
    _lesson(
        key="python-11-exceptions",
        track="python",
        level="intermediate",
        order=11,
        minutes=32,
        title="Python 11 · Ngoại lệ và xử lý lỗi an toàn",
        summary="Phục hồi từ input không hợp lệ mà không làm chương trình dừng đột ngột.",
        objective="Bắt exception cụ thể, giữ thông báo hữu ích và tránh che lỗi lập trình.",
        concepts=(
            "try chứa thao tác có thể lỗi; except xử lý lỗi mong đợi.",
            "Bắt ValueError thay vì except Exception quá rộng.",
            "else/finally phù hợp khi tách xử lý thành công và dọn dẹp tài nguyên.",
        ),
        example='try:\n    age = int("not-a-number")\nexcept ValueError:\n    print("Invalid age")',
        pitfalls=(
            "Nuốt exception mà không log hay trả thông báo phù hợp.",
            "Dùng exception để thay thế if/else bình thường.",
        ),
        takeaway="Xử lý lỗi tốt bảo vệ trải nghiệm người dùng và giúp debug nhanh hơn.",
        exercise=_exercise(
            key="python-11-exceptions-safe-sum",
            slug="python-exceptions-safe-sum",
            title="Cộng dữ liệu hợp lệ",
            prompt="Cộng các phần tử đổi được sang int trong raw và bỏ qua phần tử lỗi.",
            starter_code="""
            raw = ["4", "bad", "6"]
            total = 0
            # TODO: dùng try/except để cộng giá trị hợp lệ
            print(total)
            """,
            expected_output="10",
        ),
    ),
    _lesson(
        key="python-12-json-files",
        track="python",
        level="intermediate",
        order=12,
        minutes=35,
        title="Python 12 · Tệp, JSON và dữ liệu có cấu trúc",
        summary="Đọc/ghi dữ liệu có cấu trúc bằng standard library.",
        objective="Dùng context manager và json module để xử lý dữ liệu bền vững.",
        concepts=(
            "with mở tài nguyên và bảo đảm đóng file.",
            "json.loads() chuyển JSON string thành dict/list; dumps() làm chiều ngược lại.",
            "Dữ liệu input từ file/API cần được validate trước khi tin dùng.",
        ),
        example='import json\npayload = json.loads("{\\"name\\": \\"Ada\\"}")\nprint(payload["name"])',
        pitfalls=(
            "Dùng eval() để parse dữ liệu không tin cậy.",
            "Giả định key luôn tồn tại mà không có fallback.",
        ),
        takeaway="JSON là cầu nối phổ biến giữa Python, API, Django và FastAPI.",
        exercise=_exercise(
            key="python-12-json-files-profile",
            slug="python-json-profile",
            title="Đọc profile JSON",
            prompt="Parse payload và in theo định dạng name: score.",
            starter_code="""
            import json

            payload = '{"name": "Ada", "score": 10}'
            # TODO: parse payload và in name: score
            """,
            expected_output="Ada: 10",
        ),
    ),
    _lesson(
        key="python-13-modules-venv",
        track="python",
        level="intermediate",
        order=13,
        minutes=25,
        title="Python 13 · Module, package và môi trường ảo",
        summary="Tái sử dụng code và cô lập dependency theo từng project.",
        objective="Hiểu import, package layout, venv và requirements trước khi dùng framework.",
        concepts=(
            "Module là file Python; package là thư mục tổ chức module.",
            "venv cô lập package cho mỗi project.",
            "requirements.txt giúp tái lập môi trường làm việc.",
        ),
        example='from math import ceil\nprint(ceil(9.1))',
        pitfalls=(
            "Đặt tên file trùng json.py, random.py hoặc django.py.",
            "Cài package global rồi quên ghi dependency của project.",
        ),
        takeaway="Môi trường lặp lại được là nền tảng để project Django/FastAPI triển khai ổn định.",
        exercise=_exercise(
            key="python-13-modules-venv-ceil",
            slug="python-modules-ceil",
            title="Dùng module math",
            prompt="Import ceil từ math và in số giờ làm tròn lên của 9.1.",
            starter_code="""
            from math import ceil

            hours = 9.1
            # TODO: in số giờ làm tròn lên
            """,
            expected_output="10",
        ),
    ),
    _lesson(
        key="python-14-oop",
        track="python",
        level="intermediate",
        order=14,
        minutes=40,
        title="Python 14 · Lập trình hướng đối tượng",
        summary="Mô hình hóa dữ liệu bằng class, instance và method.",
        objective="Tạo class có trạng thái và hành vi, nhưng không lạm dụng OOP cho logic đơn giản.",
        concepts=(
            "Class là blueprint; instance là đối tượng cụ thể.",
            "__init__ khởi tạo state, self truy cập state của instance.",
            "Method nên thể hiện hành vi gắn với dữ liệu của đối tượng.",
        ),
        example='class Book:\n    def __init__(self, title):\n        self.title = title\n\nprint(Book("Python").title)',
        pitfalls=(
            "Quên self trong method instance.",
            "Đưa mọi hàm vào class dù chúng không dùng state.",
        ),
        takeaway="OOP hữu ích khi dữ liệu và hành vi đi cùng nhau, ví dụ model nghiệp vụ Django.",
        exercise=_exercise(
            key="python-14-oop-book",
            slug="python-oop-book",
            title="Tạo class Book",
            prompt="Hoàn thành Book để describe() trả về title: pages.",
            starter_code="""
            class Book:
                # TODO: nhận title và pages
                pass

            book = Book("Python", 300)
            print(book.describe())
            """,
            expected_output="Python: 300",
        ),
    ),
    _lesson(
        key="python-15-types-dataclasses",
        track="python",
        level="intermediate",
        order=15,
        minutes=30,
        title="Python 15 · Type hints, dataclass và mã dễ bảo trì",
        summary="Mô tả dữ liệu rõ ràng để giảm lỗi khi project lớn dần.",
        objective="Dùng type hint và dataclass để làm contract trong code Python dễ đọc.",
        concepts=(
            "Type hint giúp IDE, linter và người đọc hiểu contract.",
            "dataclass tự tạo __init__, repr và equality cho data container.",
            "Type hint không tự ép kiểu khi chạy runtime.",
        ),
        example='from dataclasses import dataclass\n\n@dataclass\nclass Profile:\n    name: str\n    stars: int',
        pitfalls=(
            "Tin rằng type hint thay thế validation input runtime.",
            "Dùng dataclass mutable làm default field mà không dùng default_factory.",
        ),
        takeaway="Contract rõ ràng giúp API schema và model dữ liệu AI ít mơ hồ hơn.",
        exercise=_exercise(
            key="python-15-types-dataclasses-profile",
            slug="python-dataclasses-profile",
            title="Mô tả profile",
            prompt="Tạo dataclass Profile và in mô tả Ada has 3 stars.",
            starter_code="""
            from dataclasses import dataclass

            @dataclass
            class Profile:
                name: str
                stars: int

            # TODO: tạo profile và in mô tả
            """,
            expected_output="Ada has 3 stars",
        ),
    ),
    _lesson(
        key="python-16-algorithms-complexity",
        track="python",
        level="intermediate",
        order=16,
        minutes=40,
        title="Python 16 · Thuật toán, sắp xếp và Big-O",
        summary="Chọn cách xử lý dữ liệu phù hợp khi kích thước tăng lên.",
        objective="Nhận biết chi phí thời gian cơ bản và dùng built-in hiệu quả trước khi tự tối ưu.",
        concepts=(
            "Big-O mô tả tốc độ tăng chi phí khi input lớn hơn.",
            "sorted() tạo list mới; list.sort() sắp xếp tại chỗ.",
            "set/dict lookup trung bình O(1), list membership thường O(n).",
        ),
        example='numbers = [3, 1, 2]\nprint(sorted(numbers))',
        pitfalls=(
            "Tối ưu quá sớm khi chưa đo bottleneck.",
            "Sửa list gốc khi caller vẫn cần thứ tự ban đầu.",
        ),
        takeaway="Hiểu độ phức tạp giúp pipeline dữ liệu và API phản hồi ổn định khi quy mô tăng.",
        exercise=_exercise(
            key="python-16-algorithms-complexity-sort",
            slug="python-algorithms-sort",
            title="Sắp xếp dãy số",
            prompt="Sắp xếp numbers tăng dần và in các số cách nhau một khoảng trắng.",
            starter_code="""
            numbers = [3, 1, 2]
            # TODO: sắp xếp và in bằng join
            """,
            expected_output="1 2 3",
        ),
    ),
    _lesson(
        key="python-17-testing-debugging",
        track="python",
        level="intermediate",
        order=17,
        minutes=35,
        title="Python 17 · Test, debug và logging",
        summary="Tìm lỗi có hệ thống và tự tin thay đổi code.",
        objective="Biết cách viết assertion, tái hiện lỗi và dùng log có mục đích.",
        concepts=(
            "Unit test kiểm tra một hành vi nhỏ, độc lập.",
            "Assertion mô tả kết quả mong đợi rõ hơn print debug tạm thời.",
            "Logging có level giúp quan sát production mà không lộ dữ liệu nhạy cảm.",
        ),
        example='def is_even(value):\n    return value % 2 == 0\n\nassert is_even(8) is True',
        pitfalls=(
            "Chỉ test happy path mà bỏ case biên.",
            "Log mật khẩu, token hoặc dữ liệu riêng tư.",
        ),
        takeaway="Test là lưới an toàn để bạn refactor Django, FastAPI và pipeline ML.",
        exercise=_exercise(
            key="python-17-testing-debugging-is-even",
            slug="python-testing-is-even",
            title="Kiểm tra số chẵn",
            prompt="Hoàn thành is_even và in kết quả cho 8 rồi 7.",
            starter_code="""
            def is_even(value):
                # TODO
                pass

            print(is_even(8))
            print(is_even(7))
            """,
            expected_output="True\nFalse",
        ),
    ),
    _lesson(
        key="python-18-http-urls",
        track="python",
        level="intermediate",
        order=18,
        minutes=35,
        title="Python 18 · HTTP, URL và dữ liệu web",
        summary="Hiểu request/response trước khi xây API với Django hoặc FastAPI.",
        objective="Đọc HTTP method, status code, header, query string và JSON API.",
        concepts=(
            "GET đọc dữ liệu; POST tạo/xử lý dữ liệu; PUT/PATCH cập nhật; DELETE xóa.",
            "2xx thành công, 4xx lỗi phía client, 5xx lỗi phía server.",
            "URL query cần được encode thay vì nối string thủ công.",
        ),
        example='from urllib.parse import urlencode\nprint(urlencode({"topic": "python", "page": 2}))',
        pitfalls=(
            "Gửi dữ liệu nhạy cảm qua query string.",
            "Coi mọi HTTP 200 là dữ liệu hợp lệ mà không validate JSON.",
        ),
        takeaway="HTTP là contract chung để Django UI gọi FastAPI OCR service trong dự án này.",
        exercise=_exercise(
            key="python-18-http-urls-query",
            slug="python-http-query-string",
            title="Tạo query string",
            prompt="Dùng urlencode để in query theo đúng thứ tự topic rồi page.",
            starter_code="""
            from urllib.parse import urlencode

            query = urlencode({"topic": "python", "page": 2})
            print(query)
            """,
            expected_output="topic=python&page=2",
        ),
    ),
    _lesson(
        key="ai-01-overview-responsibility",
        track="ai",
        level="beginner",
        order=19,
        minutes=30,
        title="AI 01 · Bản đồ AI và AI có trách nhiệm",
        summary="Phân biệt AI, ML, DL, Generative AI và các rủi ro triển khai.",
        objective="Chọn đúng thuật ngữ AI và nhận diện lúc cần human review.",
        concepts=(
            "AI là khái niệm rộng; ML học từ dữ liệu; DL là ML dùng neural network sâu.",
            "Generative AI sinh nội dung nhưng có thể hallucinate.",
            "Bias, privacy, consent và explainability là yêu cầu sản phẩm, không phải phần phụ.",
        ),
        example='risk = "high"\nif risk == "high":\n    print("human-review")',
        pitfalls=(
            "Đánh đồng output tự tin với output đúng.",
            "Đưa dữ liệu nhạy cảm vào dịch vụ AI mà không có chính sách và quyền phù hợp.",
        ),
        takeaway="AI tốt cần dữ liệu tốt, đánh giá rõ ràng và con người chịu trách nhiệm ở điểm quan trọng.",
        exercise=_exercise(
            key="ai-01-overview-responsibility-review",
            slug="ai-responsibility-human-review",
            title="Kích hoạt human review",
            prompt="In human-review nếu risk là high, nếu không in automated-check.",
            starter_code="""
            risk = "high"
            # TODO: kiểm tra rủi ro
            """,
            expected_output="human-review",
        ),
    ),
    _lesson(
        key="ai-02-math-foundations",
        track="ai",
        level="beginner",
        order=20,
        minutes=45,
        title="AI 02 · Toán cho AI: vector, ma trận và xác suất",
        summary="Xây nền tảng tính toán cho Machine Learning và Deep Learning.",
        objective="Hiểu vector, dot product, trung bình và xác suất như các công cụ trực giác.",
        concepts=(
            "Vector biểu diễn một tập feature; ma trận biểu diễn nhiều sample/feature.",
            "Dot product kết hợp input với trọng số của mô hình.",
            "Mean và variance mô tả trung tâm và độ phân tán của dữ liệu.",
        ),
        example='left = [1, 2, 3]\nright = [4, 5, 6]\nprint(sum(a * b for a, b in zip(left, right)))',
        pitfalls=(
            "Cộng vector có độ dài khác nhau mà không kiểm tra.",
            "Dùng xác suất như sự chắc chắn tuyệt đối.",
        ),
        takeaway="Trực giác toán tốt giúp bạn hiểu model thay vì chỉ gọi thư viện như hộp đen.",
        exercise=_exercise(
            key="ai-02-math-foundations-dot-product",
            slug="ai-math-dot-product",
            title="Tính dot product",
            prompt="Tính dot product của left và right rồi in kết quả.",
            starter_code="""
            left = [1, 2, 3]
            right = [4, 5, 6]
            # TODO: in dot product
            """,
            expected_output="32",
        ),
    ),
    _lesson(
        key="ai-03-data-preparation",
        track="ai",
        level="beginner",
        order=21,
        minutes=40,
        title="AI 03 · Làm sạch và chia dữ liệu",
        summary="Chuẩn bị dữ liệu đáng tin cậy trước khi huấn luyện mô hình.",
        objective="Nhận biết missing value, data leakage và cách chia train/validation/test.",
        concepts=(
            "Dữ liệu thiếu cần chính sách: bỏ, điền, hoặc yêu cầu thu thập lại.",
            "Train/validation/test có vai trò khác nhau và không được trộn lẫn.",
            "Data leakage tạo metric đẹp giả tạo nhưng thất bại khi production.",
        ),
        example='raw = [1, None, 2, "3", ""]\nvalid = [int(value) for value in raw if str(value).isdigit()]\nprint(sum(valid))',
        pitfalls=(
            "Chuẩn hóa toàn bộ dữ liệu trước khi chia test, làm rò rỉ thống kê.",
            "Impute dữ liệu mà không ghi lại chiến lược.",
        ),
        takeaway="Chất lượng dữ liệu thường quyết định chất lượng AI nhiều hơn việc đổi model.",
        exercise=_exercise(
            key="ai-03-data-preparation-clean-sum",
            slug="ai-data-clean-sum",
            title="Làm sạch dữ liệu nhỏ",
            prompt="Cộng các giá trị hợp lệ trong raw: int và chuỗi số được chấp nhận.",
            starter_code="""
            raw = [1, None, 2, "3", ""]
            total = 0
            # TODO: cộng các giá trị hợp lệ
            print(total)
            """,
            expected_output="6",
        ),
    ),
    _lesson(
        key="ai-04-search-heuristics",
        track="ai",
        level="intermediate",
        order=22,
        minutes=35,
        title="AI 04 · Tìm kiếm, luật và heuristic",
        summary="Hiểu AI cổ điển trước khi dựa vào mô hình học máy.",
        objective="Mô hình hóa state space và chọn chiến lược tìm kiếm phù hợp.",
        concepts=(
            "BFS ưu tiên số bước ít hơn trong graph không trọng số.",
            "DFS dùng ít bộ nhớ hơn nhưng có thể đi sâu sai hướng.",
            "A* kết hợp chi phí đã đi và heuristic ước lượng phần còn lại.",
        ),
        example='graph = {"A": ["B"], "B": ["D"], "D": []}\nprint("A->B->D")',
        pitfalls=(
            "Dùng heuristic không phù hợp mà tin output luôn tối ưu.",
            "Không theo dõi node đã thăm trong graph có chu trình.",
        ),
        takeaway="Nhiều bài toán tự động hóa có thể giải bằng rule/search rõ ràng trước khi cần ML.",
        exercise=_exercise(
            key="ai-04-search-heuristics-path",
            slug="ai-search-path",
            title="Biểu diễn đường đi",
            prompt="In chính xác đường đi A->B->D cho graph đã cho.",
            starter_code="""
            graph = {"A": ["B", "C"], "B": ["D"], "C": [], "D": []}
            # TODO: in đường đi đã tìm được
            """,
            expected_output="A->B->D",
        ),
    ),
    _lesson(
        key="ai-05-llm-prompts-context",
        track="ai",
        level="intermediate",
        order=23,
        minutes=40,
        title="AI 05 · Prompt, LLM và context window",
        summary="Viết input có cấu trúc và đánh giá đầu ra LLM cẩn trọng.",
        objective="Tạo prompt rõ nhiệm vụ, dữ liệu ngữ cảnh và tiêu chí output.",
        concepts=(
            "System instruction định hướng hành vi, user prompt nêu tác vụ cụ thể.",
            "Grounding/RAG đưa nguồn tin liên quan vào context thay vì yêu cầu model đoán.",
            "Context window hữu hạn; đưa ít thông tin nhưng có liên quan nhất.",
        ),
        example='task = "Summarize"\ncontext = "Python is readable."\nprint(f"Task: {task}\\nContext: {context}")',
        pitfalls=(
            "Dùng prompt mơ hồ rồi đánh giá model thất thường.",
            "Bỏ qua prompt injection khi lấy context từ tài liệu không tin cậy.",
        ),
        takeaway="Prompt tốt là một contract: mục tiêu, dữ liệu, ràng buộc và định dạng output.",
        exercise=_exercise(
            key="ai-05-llm-prompts-context-build",
            slug="ai-llm-build-prompt",
            title="Tạo prompt có context",
            prompt="In hai dòng Task: Summarize và Context: Python is readable.",
            starter_code="""
            task = "Summarize"
            context = "Python is readable."
            # TODO: tạo output hai dòng
            """,
            expected_output="Task: Summarize\nContext: Python is readable.",
        ),
    ),
    _lesson(
        key="ai-06-evaluation-governance",
        track="ai",
        level="intermediate",
        order=24,
        minutes=35,
        title="AI 06 · Đánh giá, giám sát và governance",
        summary="Đo chất lượng AI trước và sau phát hành thay vì chỉ demo đẹp.",
        objective="Tạo tư duy evaluation, monitoring và rollback cho sản phẩm AI.",
        concepts=(
            "Offline evaluation dùng bộ test đại diện trước khi release.",
            "Online monitoring theo dõi drift, lỗi, latency và feedback thực tế.",
            "Policy xác định dữ liệu nào được dùng, ai phê duyệt và khi nào dừng hệ thống.",
        ),
        example='results = [True, True, False, True]\nprint(f"{sum(results) / len(results) * 100:.0f}%")',
        pitfalls=(
            "Chỉ theo dõi một metric tổng hợp.",
            "Không lưu version model/prompt/dataset đi kèm từng đánh giá.",
        ),
        takeaway="Một AI system đáng tin cần khả năng đo, giải thích, cảnh báo và can thiệp.",
        exercise=_exercise(
            key="ai-06-evaluation-governance-pass-rate",
            slug="ai-evaluation-pass-rate",
            title="Tính pass rate",
            prompt="Tính phần trăm True trong results và in không có chữ số thập phân.",
            starter_code="""
            results = [True, True, False, True]
            # TODO: in pass rate
            """,
            expected_output="75%",
        ),
    ),
    _lesson(
        key="ml-01-workflow",
        track="ml",
        level="beginner",
        order=25,
        minutes=35,
        title="ML 01 · Bài toán ML và pipeline huấn luyện",
        summary="Chuyển bài toán thực tế thành feature, label, metric và baseline.",
        objective="Xác định đúng bài toán supervised/unsupervised trước khi chọn model.",
        concepts=(
            "Feature là input, label/target là giá trị cần dự đoán.",
            "Baseline đơn giản giúp biết model phức tạp có thực sự tốt hơn không.",
            "Reproducibility cần seed, dataset version và pipeline rõ ràng.",
        ),
        example='features = [[1], [2], [3]]\nlabels = [2, 4, 6]\nprint("ready" if len(features) == len(labels) else "invalid")',
        pitfalls=(
            "Chọn thuật toán trước khi định nghĩa target và metric.",
            "Đánh giá trên chính tập dùng để training.",
        ),
        takeaway="ML workflow tốt bắt đầu từ data contract và metric, không phải từ notebook model.",
        exercise=_exercise(
            key="ml-01-workflow-ready",
            slug="ml-workflow-ready",
            title="Kiểm tra dataset sẵn sàng",
            prompt="In ready nếu features và labels có cùng số sample.",
            starter_code="""
            features = [[1], [2], [3]]
            labels = [2, 4, 6]
            # TODO: kiểm tra số sample
            """,
            expected_output="ready",
        ),
    ),
    _lesson(
        key="ml-02-linear-regression",
        track="ml",
        level="beginner",
        order=26,
        minutes=40,
        title="ML 02 · Linear Regression",
        summary="Dự báo giá trị liên tục bằng đường hồi quy và residual.",
        objective="Hiểu quan hệ y = slope * x + intercept và MSE ở mức trực giác.",
        concepts=(
            "Linear regression dự đoán số liên tục như giá, thời gian hoặc doanh thu.",
            "Residual là sai khác giữa dự đoán và giá trị thật.",
            "MSE phạt mạnh lỗi lớn nên nhạy với outlier.",
        ),
        example='slope = 2\nintercept = 0\nx = 4\nprint(slope * x + intercept)',
        pitfalls=(
            "Suy ra quan hệ nhân quả chỉ từ correlation.",
            "Bỏ qua data scale/outlier và giả định tuyến tính không kiểm chứng.",
        ),
        takeaway="Regression là baseline mạnh khi hiểu rõ dữ liệu và sai số của nó.",
        exercise=_exercise(
            key="ml-02-linear-regression-predict",
            slug="ml-linear-predict",
            title="Dự đoán tuyến tính",
            prompt="Tính y từ slope, intercept và x rồi in kết quả.",
            starter_code="""
            slope = 2
            intercept = 0
            x = 4
            # TODO: dự đoán y
            """,
            expected_output="8",
        ),
    ),
    _lesson(
        key="ml-03-logistic-classification",
        track="ml",
        level="beginner",
        order=27,
        minutes=40,
        title="ML 03 · Logistic Regression và phân loại",
        summary="Dự đoán nhãn từ xác suất với threshold được cân nhắc theo bài toán.",
        objective="Hiểu binary classification, probability và quyết định threshold.",
        concepts=(
            "Logistic regression trả xác suất, không phải certainty.",
            "Threshold 0.5 chỉ là điểm khởi đầu; cost false positive/negative có thể khác nhau.",
            "Nhiều lớp có thể xử lý bằng one-vs-rest hoặc softmax.",
        ),
        example='probability = 0.81\nprint("positive" if probability >= 0.5 else "negative")',
        pitfalls=(
            "Dùng accuracy khi class mất cân bằng.",
            "Không calibrate probability trước khi dùng cho quyết định rủi ro.",
        ),
        takeaway="Classifier tốt cần threshold và metric phản ánh đúng hậu quả của lỗi.",
        exercise=_exercise(
            key="ml-03-logistic-classification-threshold",
            slug="ml-classification-threshold",
            title="Phân loại theo threshold",
            prompt="In positive nếu probability >= 0.5, ngược lại in negative.",
            starter_code="""
            probability = 0.81
            # TODO: phân loại theo threshold
            """,
            expected_output="positive",
        ),
    ),
    _lesson(
        key="ml-04-knn",
        track="ml",
        level="beginner",
        order=28,
        minutes=35,
        title="ML 04 · K-Nearest Neighbors",
        summary="Phân loại từ các điểm dữ liệu gần nhất và hiểu vai trò của scale.",
        objective="Hiểu distance, k và tác động của feature scaling trong KNN.",
        concepts=(
            "KNN lưu training data thay vì học tham số phức tạp.",
            "Feature có scale lớn có thể áp đảo distance.",
            "k nhỏ nhạy nhiễu; k lớn làm mờ ranh giới class.",
        ),
        example='points = [(1, "cold"), (9, "hot")]\nvalue = 8\nprint(min(points, key=lambda point: abs(value - point[0]))[1])',
        pitfalls=(
            "Dùng KNN cho dataset lớn mà không xét chi phí dự đoán.",
            "Không xử lý tie giữa các hàng xóm.",
        ),
        takeaway="KNN giúp trực giác về similarity trước khi học các model tối ưu phức tạp hơn.",
        exercise=_exercise(
            key="ml-04-knn-nearest-label",
            slug="ml-knn-nearest-label",
            title="Chọn nhãn gần nhất",
            prompt="In nhãn của point có giá trị số gần value nhất.",
            starter_code="""
            points = [(1, "cold"), (9, "hot")]
            value = 8
            # TODO: in nhãn gần value nhất
            """,
            expected_output="hot",
        ),
    ),
    _lesson(
        key="ml-05-trees-ensembles",
        track="ml",
        level="intermediate",
        order=29,
        minutes=45,
        title="ML 05 · Decision Tree và Ensemble",
        summary="Diễn giải quyết định và giảm variance bằng random forest hoặc boosting.",
        objective="Hiểu split, overfitting và lý do ensemble thường mạnh hơn một tree đơn lẻ.",
        concepts=(
            "Decision tree chia dữ liệu theo câu hỏi có điều kiện.",
            "Random forest giảm variance bằng nhiều tree khác nhau.",
            "Boosting học dần từ lỗi của model trước và cần chống overfit.",
        ),
        example='has_income = True\nhas_debt = False\nprint("approved" if has_income and not has_debt else "review")',
        pitfalls=(
            "Coi feature importance là quan hệ nhân quả.",
            "Để tree quá sâu và học thuộc training data.",
        ),
        takeaway="Tree-based model mạnh với tabular data, nhưng evaluation và leakage vẫn quyết định kết quả.",
        exercise=_exercise(
            key="ml-05-trees-ensembles-approval",
            slug="ml-trees-approval",
            title="Quy tắc phê duyệt",
            prompt="In approved nếu có income và không có debt; ngược lại in review.",
            starter_code="""
            has_income = True
            has_debt = False
            # TODO: áp dụng quy tắc
            """,
            expected_output="approved",
        ),
    ),
    _lesson(
        key="ml-06-metrics-validation",
        track="ml",
        level="intermediate",
        order=30,
        minutes=45,
        title="ML 06 · Metric, validation và overfitting",
        summary="Chọn metric phù hợp và phát hiện model học thuộc thay vì tổng quát hóa.",
        objective="So sánh accuracy, precision, recall, F1 và dùng validation đúng cách.",
        concepts=(
            "Accuracy không đủ khi class imbalance hoặc chi phí lỗi bất đối xứng.",
            "Precision quan tâm false positive; recall quan tâm false negative.",
            "Cross-validation ổn định ước lượng khi dữ liệu chưa nhiều.",
        ),
        example='actual = [1, 0, 1, 0]\npredicted = [1, 0, 0, 0]\nprint(sum(a == b for a, b in zip(actual, predicted)) / len(actual))',
        pitfalls=(
            "Chọn metric đẹp nhất sau khi đã xem test set.",
            "Tune hyperparameter trên test set nhiều lần.",
        ),
        takeaway="Metric là ngôn ngữ nối mục tiêu sản phẩm với hành vi model.",
        exercise=_exercise(
            key="ml-06-metrics-validation-accuracy",
            slug="ml-metrics-accuracy",
            title="Tính accuracy",
            prompt="Tính tỷ lệ dự đoán đúng và in với hai chữ số thập phân.",
            starter_code="""
            actual = [1, 0, 1, 0]
            predicted = [1, 0, 0, 0]
            # TODO: in accuracy với 2 chữ số thập phân
            """,
            expected_output="0.75",
        ),
    ),
    _lesson(
        key="ml-07-feature-engineering",
        track="ml",
        level="intermediate",
        order=31,
        minutes=40,
        title="ML 07 · Feature engineering và pipeline",
        summary="Biến dữ liệu thô thành feature tái lập được cho model.",
        objective="Thiết kế feature transformation không gây leakage và có thể chạy lại.",
        concepts=(
            "Encode category, impute missing value và scale số là các bước phổ biến.",
            "Pipeline đảm bảo train và inference dùng cùng transformation.",
            "Feature store/versioning giúp truy vết dữ liệu dùng cho model.",
        ),
        example='titles = ["AI", "Python"]\nprint(",".join(str(len(title)) for title in titles))',
        pitfalls=(
            "Tạo feature dùng thông tin tương lai.",
            "Làm transformation ở notebook nhưng quên đưa vào production pipeline.",
        ),
        takeaway="Feature tốt là feature có nghĩa, hợp lệ lúc inference và được version hóa.",
        exercise=_exercise(
            key="ml-07-feature-engineering-title-lengths",
            slug="ml-feature-title-lengths",
            title="Tạo feature độ dài",
            prompt="In độ dài các title, ngăn cách bằng dấu phẩy và không có khoảng trắng.",
            starter_code="""
            titles = ["AI", "Python"]
            # TODO: in độ dài các title
            """,
            expected_output="2,6",
        ),
    ),
    _lesson(
        key="ml-08-unsupervised-learning",
        track="ml",
        level="intermediate",
        order=32,
        minutes=45,
        title="ML 08 · Clustering, giảm chiều và phân khúc",
        summary="Khám phá cấu trúc khi dữ liệu không có label.",
        objective="Hiểu K-means, PCA và cách diễn giải cluster thận trọng.",
        concepts=(
            "K-means gom điểm quanh centroid nhưng cần chọn k và scale đúng.",
            "PCA giảm chiều để quan sát/tiền xử lý, không tự tạo ý nghĩa nghiệp vụ.",
            "Silhouette score hỗ trợ đánh giá nhưng không thay thế domain knowledge.",
        ),
        example='left = [1, 2]\nright = [9, 10]\nprint(f"{sum(left) / len(left):.1f}, {sum(right) / len(right):.1f}")',
        pitfalls=(
            "Gọi cluster là ground truth hay persona chắc chắn.",
            "Dùng distance khi feature chưa được scale.",
        ),
        takeaway="Unsupervised learning tạo giả thuyết để kiểm chứng, không tự thay thế quyết định nghiệp vụ.",
        exercise=_exercise(
            key="ml-08-unsupervised-learning-cluster-means",
            slug="ml-cluster-means",
            title="Tính mean của hai cụm",
            prompt="Tính mean của [1, 2] và [9, 10], in mỗi mean một chữ số thập phân.",
            starter_code="""
            left = [1, 2]
            right = [9, 10]
            # TODO: in mean hai cụm
            """,
            expected_output="1.5, 9.5",
        ),
    ),
    _lesson(
        key="dl-01-neurons-activations",
        track="dl",
        level="intermediate",
        order=33,
        minutes=40,
        title="DL 01 · Neuron, layer và activation",
        summary="Hiểu phép tính bên trong neural network trước khi dùng framework.",
        objective="Tính weighted sum, bias và hiểu trực giác về activation function.",
        concepts=(
            "Neuron tính weighted sum của input rồi cộng bias.",
            "ReLU tạo phi tuyến đơn giản và phổ biến trong hidden layer.",
            "Layer chồng lên nhau để học representation phức tạp hơn.",
        ),
        example='inputs = [1.0, 2.0]\nweights = [0.5, 1.5]\nbias = 0.5\nprint(sum(x * w for x, w in zip(inputs, weights)) + bias)',
        pitfalls=(
            "Nghĩ neuron sinh học và neuron nhân tạo hoạt động giống hệt nhau.",
            "Bỏ qua scale input làm training không ổn định.",
        ),
        takeaway="Deep Learning là nhiều phép tính vector đơn giản được tổ chức và tối ưu hóa cùng nhau.",
        exercise=_exercise(
            key="dl-01-neurons-activations-weighted-sum",
            slug="dl-neuron-weighted-sum",
            title="Tính weighted sum",
            prompt="Tính tổng input * weight cộng bias rồi in kết quả.",
            starter_code="""
            inputs = [1.0, 2.0]
            weights = [0.5, 1.5]
            bias = 0.5
            # TODO: in weighted sum
            """,
            expected_output="4.0",
        ),
    ),
    _lesson(
        key="dl-02-loss-gradients-backprop",
        track="dl",
        level="intermediate",
        order=34,
        minutes=50,
        title="DL 02 · Loss, gradient descent và backpropagation",
        summary="Tối ưu model từng bước bằng gradient có kiểm soát.",
        objective="Hiểu loss, learning rate và quy tắc update tham số cơ bản.",
        concepts=(
            "Loss đo mức sai giữa prediction và target.",
            "Gradient chỉ hướng tăng loss; gradient descent đi ngược hướng đó.",
            "Backpropagation dùng chain rule để tính gradient hiệu quả qua các layer.",
        ),
        example='weight = 0.0\ngradient = -2.0\nlearning_rate = 0.1\nweight -= learning_rate * gradient\nprint(weight)',
        pitfalls=(
            "Learning rate quá lớn làm loss dao động hoặc diverge.",
            "Chỉ nhìn training loss mà không đánh giá validation loss.",
        ),
        takeaway="Training là vòng lặp đo lỗi, tính hướng điều chỉnh, cập nhật và kiểm tra khả năng tổng quát hóa.",
        exercise=_exercise(
            key="dl-02-loss-gradients-backprop-update",
            slug="dl-gradient-update",
            title="Cập nhật một trọng số",
            prompt="Cập nhật weight theo gradient descent và in với một chữ số thập phân.",
            starter_code="""
            weight = 0.0
            gradient = -2.0
            learning_rate = 0.1
            # TODO: cập nhật weight
            print(f"{weight:.1f}")
            """,
            expected_output="0.2",
        ),
    ),
    _lesson(
        key="dl-03-training-pytorch",
        track="dl",
        level="intermediate",
        order=35,
        minutes=50,
        title="DL 03 · Training loop với PyTorch",
        summary="Đọc và thiết kế training loop thực tế mà không bỏ qua validation.",
        objective="Hiểu Dataset/DataLoader, forward, loss, backward, optimizer và checkpoint.",
        concepts=(
            "PyTorch tensor lưu dữ liệu; DataLoader chia batch một cách lặp lại được.",
            "Một training step gồm forward, loss, zero_grad, backward và optimizer.step.",
            "Checkpoint cần lưu model state, optimizer state và metadata version.",
        ),
        example='losses = [0.8, 0.5, 0.2]\nprint(f"{min(losses):.2f}")',
        pitfalls=(
            "Quên model.train() và model.eval() khi có dropout/batch norm.",
            "Lưu checkpoint mà không ghi dataset/model configuration.",
        ),
        takeaway="Framework giúp viết tensor nhanh, nhưng nguyên tắc evaluation và reproducibility vẫn là trách nhiệm của bạn.",
        exercise=_exercise(
            key="dl-03-training-pytorch-best-loss",
            slug="dl-training-best-loss",
            title="Theo dõi loss tốt nhất",
            prompt="In loss nhỏ nhất với hai chữ số thập phân.",
            starter_code="""
            losses = [0.8, 0.5, 0.2]
            # TODO: in loss nhỏ nhất
            """,
            expected_output="0.20",
        ),
    ),
    _lesson(
        key="dl-04-cnn-computer-vision",
        track="dl",
        level="intermediate",
        order=36,
        minutes=45,
        title="DL 04 · CNN và Computer Vision",
        summary="Nhận diện đặc trưng không gian trong ảnh bằng convolution và pooling.",
        objective="Hiểu kernel, feature map, augmentation và transfer learning ở mức thiết kế.",
        concepts=(
            "Convolution quét kernel để tìm pattern cục bộ như cạnh hoặc texture.",
            "Pooling giảm kích thước feature map và giữ tín hiệu nổi bật.",
            "Data augmentation cần phản ánh biến đổi hợp lệ của bài toán thực tế.",
        ),
        example='pixels = [[1, 3], [2, 9]]\nprint(max(value for row in pixels for value in row))',
        pitfalls=(
            "Augment ảnh làm thay đổi label hoặc ngữ nghĩa.",
            "Đánh giá vision model chỉ bằng ảnh đẹp, không có dữ liệu đại diện production.",
        ),
        takeaway="Computer vision tốt phụ thuộc vào dataset, nhãn và cách đánh giá ngang với architecture.",
        exercise=_exercise(
            key="dl-04-cnn-computer-vision-max-pool",
            slug="dl-cnn-max-pooling",
            title="Mô phỏng max pooling",
            prompt="Tìm giá trị lớn nhất trong pixels 2x2 và in nó.",
            starter_code="""
            pixels = [[1, 3], [2, 9]]
            # TODO: in max-pooling 2x2
            """,
            expected_output="9",
        ),
    ),
    _lesson(
        key="dl-05-sequences-rnn",
        track="dl",
        level="intermediate",
        order=37,
        minutes=45,
        title="DL 05 · Dữ liệu tuần tự và RNN",
        summary="Hiểu state khi xử lý văn bản, time series và dữ liệu có thứ tự.",
        objective="Phân biệt sequence model, hidden state, RNN, LSTM và GRU.",
        concepts=(
            "Thứ tự token/timestep thay đổi ý nghĩa của dữ liệu sequence.",
            "RNN truyền hidden state nhưng có thể gặp vanishing/exploding gradient.",
            "LSTM/GRU thêm gate để giữ thông tin quan trọng lâu hơn.",
        ),
        example='next_token = {"learn": "python", "python": "fast"}\nprint(next_token["learn"])',
        pitfalls=(
            "Không mask padding trong batch sequence.",
            "Dùng random split cho time series làm rò rỉ tương lai vào quá khứ.",
        ),
        takeaway="Sequence cần cách chia dữ liệu và metric tôn trọng thời gian/thứ tự.",
        exercise=_exercise(
            key="dl-05-sequences-rnn-next-token",
            slug="dl-sequences-next-token",
            title="Lấy token tiếp theo",
            prompt="In token đứng sau learn từ next_token.",
            starter_code="""
            next_token = {"learn": "python", "python": "fast"}
            # TODO: in token sau learn
            """,
            expected_output="python",
        ),
    ),
    _lesson(
        key="dl-06-transformers-llms",
        track="dl",
        level="advanced",
        order=38,
        minutes=55,
        title="DL 06 · Attention, Transformer và LLM",
        summary="Hiểu nền tảng Transformer, embedding, RAG và chiến lược dùng LLM an toàn.",
        objective="Mô tả self-attention và phân biệt prompting, RAG và fine-tuning.",
        concepts=(
            "Attention gán trọng số cho token liên quan trong context.",
            "Embedding biểu diễn ngữ nghĩa dạng vector cho retrieval và clustering.",
            "RAG lấy nguồn tin trước khi sinh; fine-tuning thay đổi trọng số model.",
        ),
        example='tokens = ["I", "learn", "Python"]\nscores = [0.1, 0.3, 0.9]\nprint(tokens[scores.index(max(scores))])',
        pitfalls=(
            "Tin citation/hallucination của LLM mà không xác minh nguồn.",
            "Fine-tune khi vấn đề thực chất là retrieval hoặc prompt contract.",
        ),
        takeaway="Transformer mạnh nhờ attention và dữ liệu lớn, nhưng hệ thống LLM vẫn cần retrieval, evaluation và guardrail.",
        exercise=_exercise(
            key="dl-06-transformers-llms-top-token",
            slug="dl-transformers-top-token",
            title="Chọn token được chú ý nhất",
            prompt="In token có score lớn nhất.",
            starter_code="""
            tokens = ["I", "learn", "Python"]
            scores = [0.1, 0.3, 0.9]
            # TODO: in token có score lớn nhất
            """,
            expected_output="Python",
        ),
    ),
    _lesson(
        key="django-01-web-mvt",
        track="django",
        level="beginner",
        order=39,
        minutes=35,
        title="Django 01 · Web, HTTP và kiến trúc MVT",
        summary="Đặt Django vào bức tranh request-response của một web application.",
        objective="Hiểu Browser → URL → View → Template/Model → Response trong Django.",
        concepts=(
            "Model quản lý dữ liệu, View xử lý request, Template render HTML.",
            "Middleware chạy quanh request/response cho session, auth, CSRF và security.",
            "HTTP status code là một phần contract với browser/client.",
        ),
        example='request = {"method": "GET", "path": "/lessons/"}\nprint(request["method"], request["path"])',
        pitfalls=(
            "Đặt business logic phức tạp trực tiếp trong template.",
            "Trả HTTP 200 cho lỗi validation/API thất bại.",
        ),
        takeaway="Django giúp tổ chức web app theo request flow có quy ước rõ ràng.",
        exercise=_exercise(
            key="django-01-web-mvt-request-summary",
            slug="django-request-summary",
            title="Tóm tắt request",
            prompt="In HTTP method và path, cách nhau đúng một khoảng trắng.",
            starter_code="""
            request = {"method": "GET", "path": "/lessons/"}
            # TODO: in method và path
            """,
            expected_output="GET /lessons/",
        ),
    ),
    _lesson(
        key="django-02-project-routing-templates",
        track="django",
        level="beginner",
        order=40,
        minutes=40,
        title="Django 02 · Project, app, URL, view và template",
        summary="Tạo một page Django có route, view và template rõ ràng.",
        objective="Biết vai trò startproject, startapp, urls.py, view function/CBV và static files.",
        concepts=(
            "Project chứa cấu hình chung; app đóng gói một domain nghiệp vụ.",
            "URL dispatcher ánh xạ route tới view.",
            "Template tách presentation khỏi request logic.",
        ),
        example='routes = {"/": "home", "/lessons/": "lesson_list"}\nprint(routes["/lessons/"])',
        pitfalls=(
            "Trộn URL routing của project và app mà không có namespace.",
            "Hard-code URL trong template thay vì {% url %}.",
        ),
        takeaway="Routing rõ ràng giúp ứng dụng Django mở rộng mà không biến thành một file view khổng lồ.",
        exercise=_exercise(
            key="django-02-project-routing-templates-route",
            slug="django-routing-view-name",
            title="Tra cứu view theo route",
            prompt="In view được ánh xạ cho /lessons/.",
            starter_code="""
            routes = {"/": "home", "/lessons/": "lesson_list"}
            # TODO: in view của /lessons/
            """,
            expected_output="lesson_list",
        ),
    ),
    _lesson(
        key="django-03-models-orm-admin",
        track="django",
        level="intermediate",
        order=41,
        minutes=50,
        title="Django 03 · Model, ORM, migration và Admin",
        summary="Lưu và truy vấn dữ liệu nghiệp vụ bằng Django ORM.",
        objective="Thiết kế model, relationship, migration và admin theo dữ liệu thực tế.",
        concepts=(
            "Model field mô tả schema; migration version hóa thay đổi database.",
            "QuerySet là lazy và có thể filter/order/prefetch dữ liệu.",
            "Django Admin tăng tốc quản trị nhưng không thay thế UX cho người học.",
        ),
        example='lessons = [{"published": True}, {"published": False}]\nprint(sum(item["published"] for item in lessons))',
        pitfalls=(
            "Sửa database thủ công mà không tạo migration.",
            "Gây N+1 query trong list page vì quên select_related/prefetch_related.",
        ),
        takeaway="Model và migration là contract dài hạn với dữ liệu production.",
        exercise=_exercise(
            key="django-03-models-orm-admin-published-count",
            slug="django-orm-published-count",
            title="Đếm lesson public",
            prompt="Đếm các lesson có published là True.",
            starter_code="""
            lessons = [
                {"title": "Python", "published": True},
                {"title": "AI", "published": True},
                {"title": "Draft", "published": False},
            ]
            # TODO: in số published lesson
            """,
            expected_output="2",
        ),
    ),
    _lesson(
        key="django-04-forms-auth-security",
        track="django",
        level="intermediate",
        order=42,
        minutes=45,
        title="Django 04 · Form, Auth, Session và CSRF",
        summary="Xử lý input và xác thực người dùng an toàn.",
        objective="Hiểu validation, password hash, session và CSRF trước khi tạo form web.",
        concepts=(
            "Django Form tách validation, cleaned_data và hiển thị lỗi.",
            "Mật khẩu phải hash bằng framework, không tự lưu plaintext.",
            "CSRF token bảo vệ POST từ trang giả mạo trong browser session.",
        ),
        example='username = "ada"\npassword = "secure-pass"\nprint("valid" if username and len(password) >= 8 else "invalid")',
        pitfalls=(
            "Tắt CSRF để giải lỗi tạm thời.",
            "Tin file upload theo extension/content-type mà không validate thêm.",
        ),
        takeaway="Security mặc định của Django hữu ích khi được giữ nguyên và cấu hình đúng.",
        exercise=_exercise(
            key="django-04-forms-auth-security-validate",
            slug="django-auth-input-validate",
            title="Kiểm tra input tài khoản",
            prompt="In valid nếu username không rỗng và password dài ít nhất 8 ký tự.",
            starter_code="""
            username = "ada"
            password = "secure-pass"
            # TODO: kiểm tra input
            """,
            expected_output="valid",
        ),
    ),
    _lesson(
        key="django-05-cbv-testing",
        track="django",
        level="intermediate",
        order=43,
        minutes=45,
        title="Django 05 · Class-based view, test và tối ưu truy vấn",
        summary="Mở rộng ứng dụng Django mà vẫn dễ kiểm thử và có hiệu năng tốt.",
        objective="Dùng CBV/mixin hợp lý, viết TestCase và nhận diện query lặp.",
        concepts=(
            "ListView/DetailView giảm boilerplate cho CRUD đọc dữ liệu.",
            "LoginRequiredMixin diễn đạt quyền truy cập ở đúng lớp view.",
            "select_related/prefetch_related tối ưu relationship theo kiểu truy vấn.",
        ),
        example='status_codes = [200, 200, 404]\nprint(status_codes.count(200))',
        pitfalls=(
            "Kế thừa CBV quá sâu tới mức khó hiểu MRO.",
            "Chỉ test status code mà không test authorization và dữ liệu render.",
        ),
        takeaway="Test và query discipline cần được xây ngay khi view còn nhỏ.",
        exercise=_exercise(
            key="django-05-cbv-testing-count-ok",
            slug="django-testing-count-ok",
            title="Đếm response thành công",
            prompt="In số phần tử 200 trong status_codes.",
            starter_code="""
            status_codes = [200, 200, 404]
            # TODO: in số response 200
            """,
            expected_output="2",
        ),
    ),
    _lesson(
        key="django-06-rest-framework",
        track="django",
        level="intermediate",
        order=44,
        minutes=50,
        title="Django 06 · Django REST Framework",
        summary="Xây API có serializer, permission và contract rõ ràng.",
        objective="Hiểu serializer, API view, permission, pagination và API contract.",
        concepts=(
            "Serializer validate/biến đổi dữ liệu model thành JSON và ngược lại.",
            "Permission kiểm soát ai được xem hoặc tạo dữ liệu.",
            "Pagination và filtering bảo vệ API list khỏi response quá lớn.",
        ),
        example='import json\nlesson = {"id": 1, "title": "Python"}\nprint(json.dumps(lesson))',
        pitfalls=(
            "Mở permission AllowAny cho endpoint có dữ liệu riêng tư.",
            "Trả internal exception detail cho client production.",
        ),
        takeaway="API tốt có schema, quyền và error response nhất quán để frontend/service khác tích hợp an toàn.",
        exercise=_exercise(
            key="django-06-rest-framework-json",
            slug="django-rest-json-lesson",
            title="Serialize lesson thành JSON",
            prompt="Dùng json.dumps để in lesson theo JSON một dòng.",
            starter_code="""
            import json

            lesson = {"id": 1, "title": "Python"}
            # TODO: JSON hóa lesson
            """,
            expected_output='{"id": 1, "title": "Python"}',
        ),
    ),
    _lesson(
        key="fastapi-01-routing-pydantic-docs",
        track="fastapi",
        level="beginner",
        order=45,
        minutes=40,
        title="FastAPI 01 · Route, Pydantic và API Docs",
        summary="Tạo endpoint có kiểu dữ liệu rõ ràng và tài liệu tự sinh.",
        objective="Hiểu path/query/body parameter, Pydantic model và /docs của FastAPI.",
        concepts=(
            "FastAPI tạo OpenAPI docs từ type hint và Pydantic schema.",
            "Path, query và JSON body có mục đích khác nhau.",
            "response_model giúp contract response rõ và an toàn hơn.",
        ),
        example='def greet(name):\n    return f"Hello, {name}!"\n\nprint(greet("Ada"))',
        pitfalls=(
            "Dùng dict không schema cho mọi body input.",
            "Cho endpoint trả model nội bộ có field nhạy cảm.",
        ),
        takeaway="FastAPI biến type hint tốt thành API contract và docs hữu dụng cho cả team.",
        exercise=_exercise(
            key="fastapi-01-routing-pydantic-docs-greet",
            slug="fastapi-greet-function",
            title="Viết hàm greet",
            prompt="Hoàn thành greet(name) và in lời chào cho Ada.",
            starter_code="""
            def greet(name):
                # TODO: trả về lời chào
                pass

            print(greet("Ada"))
            """,
            expected_output="Hello, Ada!",
        ),
    ),
    _lesson(
        key="fastapi-02-validation-dependencies",
        track="fastapi",
        level="intermediate",
        order=46,
        minutes=45,
        title="FastAPI 02 · Validation, dependency và error handling",
        summary="Tách validation/auth khỏi business logic để endpoint dễ test.",
        objective="Dùng Pydantic validation, Depends và HTTPException đúng vai trò.",
        concepts=(
            "Pydantic validate kiểu/ràng buộc trước khi logic nghiệp vụ chạy.",
            "Depends tái dùng auth, database session, config và policy.",
            "HTTPException trả status/detail an toàn theo contract API.",
        ),
        example='payload = {"name": "Ada", "age": 20}\nprint("valid" if payload["name"] and payload["age"] >= 0 else "invalid")',
        pitfalls=(
            "Nhét database session global không có lifecycle rõ ràng.",
            "Bắt Exception toàn cục rồi trả 200 với error string.",
        ),
        takeaway="Dependency injection và validation giúp FastAPI service nhỏ nhưng có cấu trúc production-ready.",
        exercise=_exercise(
            key="fastapi-02-validation-dependencies-valid",
            slug="fastapi-validation-payload",
            title="Validate payload",
            prompt="In valid nếu name không rỗng và age không âm.",
            starter_code="""
            payload = {"name": "Ada", "age": 20}
            # TODO: validate payload
            """,
            expected_output="valid",
        ),
    ),
    _lesson(
        key="fastapi-03-async-concurrency",
        track="fastapi",
        level="intermediate",
        order=47,
        minutes=45,
        title="FastAPI 03 · Async, background task và kết nối thời gian thực",
        summary="Dùng async đúng chỗ và tránh block event loop.",
        objective="Phân biệt I/O-bound với CPU-bound và quản lý async endpoint hợp lý.",
        concepts=(
            "async/await hữu ích cho I/O chờ mạng/database, không tăng tốc CPU-bound tự động.",
            "Background task phù hợp công việc ngắn sau response; hàng đợi phù hợp job tin cậy hơn.",
            "WebSocket cần auth, heartbeat và giới hạn tài nguyên.",
        ),
        example='import asyncio\n\nasync def read_lesson():\n    return "lesson ready"\n\nprint(asyncio.run(read_lesson()))',
        pitfalls=(
            "Gọi hàm CPU nặng trực tiếp trong async endpoint.",
            "Dùng BackgroundTasks cho workflow cần retry và durability.",
        ),
        takeaway="Async là công cụ quản lý thời gian chờ; nó cần boundary rõ với công việc nặng.",
        exercise=_exercise(
            key="fastapi-03-async-concurrency-run",
            slug="fastapi-async-run",
            title="Chạy coroutine",
            prompt="Dùng asyncio.run để chạy read_lesson và in kết quả.",
            starter_code="""
            import asyncio

            async def read_lesson():
                return "lesson ready"

            # TODO: chạy coroutine và in kết quả
            """,
            expected_output="lesson ready",
        ),
    ),
    _lesson(
        key="fastapi-04-crud-testing",
        track="fastapi",
        level="intermediate",
        order=48,
        minutes=50,
        title="FastAPI 04 · CRUD, database và kiểm thử API",
        summary="Thiết kế endpoint CRUD có transaction và test đáng tin cậy.",
        objective="Hiểu resource design, repository/service boundary, transaction và TestClient.",
        concepts=(
            "CRUD endpoint cần status code, ownership và validation nhất quán.",
            "Transaction đảm bảo thay đổi liên quan cùng thành công hoặc cùng rollback.",
            "TestClient/fixture giúp test API không phụ thuộc dịch vụ ngoài.",
        ),
        example='items = [{"name": "Django"}]\nitems.append({"name": "FastAPI"})\nprint(len(items))\nprint(items[-1]["name"])',
        pitfalls=(
            "Truy cập database trực tiếp khắp endpoint mà không có transaction boundary.",
            "Test chỉ happy path và bỏ qua auth/404/conflict.",
        ),
        takeaway="CRUD production không chỉ là create/read/update/delete mà còn là data integrity và permission.",
        exercise=_exercise(
            key="fastapi-04-crud-testing-items",
            slug="fastapi-crud-items",
            title="Thêm item vào collection",
            prompt="Thêm FastAPI vào items, rồi in length và tên item cuối.",
            starter_code="""
            items = [{"name": "Django"}]
            # TODO: thêm FastAPI
            """,
            expected_output="2\nFastAPI",
        ),
    ),
    _lesson(
        key="fastapi-05-django-ocr-integration",
        track="fastapi",
        level="advanced",
        order=49,
        minutes=50,
        title="FastAPI 05 · Django ↔ FastAPI và OCR microservice",
        summary="Kết nối Django với OCR/grading service theo contract ổn định.",
        objective="Hiểu multipart upload, timeout, response schema, OCR confidence và sandbox boundary.",
        concepts=(
            "Django nhận user/session/database; FastAPI xử lý OCR/sandbox chuyên biệt.",
            "Service boundary cần timeout, error mapping và schema version rõ ràng.",
            "OCR output là dữ liệu không tin cậy; sandbox cần giới hạn tài nguyên.",
        ),
        example='response = {"status": "passed", "confidence": 91}\nprint(response["status"] if response["confidence"] >= 80 else "review")',
        pitfalls=(
            "Tin OCR code mà không enforce timeout/memory/output limit.",
            "Cho OCR service quyền truy cập database/app network rộng hơn cần thiết.",
        ),
        takeaway="Microservice tốt là contract nhỏ, failure mode rõ và boundary bảo mật có chủ đích.",
        exercise=_exercise(
            key="fastapi-05-django-ocr-integration-status",
            slug="fastapi-ocr-status",
            title="Đọc kết quả OCR",
            prompt="In status nếu confidence >= 80, nếu không in review.",
            starter_code="""
            response = {"status": "passed", "confidence": 91}
            # TODO: kiểm tra confidence và in kết quả
            """,
            expected_output="passed",
        ),
    ),
    _lesson(
        key="fastapi-06-platform-capstone",
        track="fastapi",
        level="advanced",
        order=50,
        minutes=60,
        title="FastAPI 06 · Docker, health check và capstone",
        summary="Đóng gói, quan sát và triển khai Python Learning Platform an toàn.",
        objective="Kết hợp Django, FastAPI, PostgreSQL, Docker Compose, Nginx và health check.",
        concepts=(
            "Docker Compose mô tả service, network, volume, healthcheck và biến môi trường.",
            "Health endpoint khác readiness/liveness khi hệ thống production phức tạp.",
            "Secrets không commit vào git; logging/metric cần không lộ dữ liệu nhạy cảm.",
        ),
        example='services = {"django": "healthy", "fastapi": "healthy", "postgres": "healthy"}\nprint("All services healthy" if all(status == "healthy" for status in services.values()) else "Check services")',
        pitfalls=(
            "Expose database/OCR sandbox thẳng ra Internet không cần gateway.",
            "Dùng DEBUG và secret key development ở production.",
        ),
        takeaway="Capstone tốt là một hệ thống chạy được, quan sát được và an toàn khi có lỗi.",
        exercise=_exercise(
            key="fastapi-06-platform-capstone-health",
            slug="fastapi-platform-health",
            title="Kiểm tra sức khỏe nền tảng",
            prompt="In All services healthy nếu mọi service có trạng thái healthy.",
            starter_code="""
            services = {
                "django": "healthy",
                "fastapi": "healthy",
                "postgres": "healthy",
            }
            # TODO: kiểm tra toàn bộ service
            """,
            expected_output="All services healthy",
        ),
    ),
)

CURRICULUM: tuple[dict[str, Any], ...] = BASE_CURRICULUM + build_master_curriculum(
    _lesson,
    _exercise,
)

CURRICULUM_MANIFEST: dict[str, int] = {
    "lesson_count": len(CURRICULUM),
    "exercise_count": sum(len(entry["exercises"]) for entry in CURRICULUM),
    "mastery_extension_count": len(CURRICULUM) - len(BASE_CURRICULUM),
}
