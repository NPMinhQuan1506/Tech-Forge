"""Structured teaching aids rendered on every lesson detail page."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class LearningMap:
    """A visual explanation scaffold for one curriculum track."""

    mental_model: str
    pipeline: tuple[str, ...]
    edge_cases: tuple[str, ...]
    mistakes: tuple[str, ...]
    practice_loop: tuple[str, ...]


@dataclass(frozen=True)
class LearningVisual:
    """A compact ASCII diagram that makes a track's feedback loop tangible."""

    title: str
    diagram: str
    explanation: str


DEFAULT_LEARNING_VISUAL = LearningVisual(
    title="Nhìn luồng xử lý trước khi đi vào cú pháp",
    diagram="""input
  |
  v
[rule / model] ---> output
       ^              |
       |---- feedback-+""",
    explanation=(
        "Mọi bài kỹ thuật đều có cùng câu hỏi: dữ liệu đi vào là gì, bước biến đổi "
        "nào tạo ra kết quả, và bạn dùng phản hồi nào để biết mình làm đúng?"
    ),
)


TRACK_LEARNING_VISUALS: dict[str, LearningVisual] = {
    "python": LearningVisual(
        title="Python: dữ liệu đi qua logic rồi thành kết quả",
        diagram="""input() -> str -> convert -> condition / loop -> print()\n                  |                         |\n                  +---- invalid value? -----+--> handle error""",
        explanation="Đừng bắt đầu bằng câu lệnh. Hãy xác định kiểu dữ liệu đầu vào, quy tắc biến đổi và định dạng đầu ra trước.",
    ),
    "math": LearningVisual(
        title="Toán cho AI: loss chỉ đường cho bước cập nhật",
        diagram="""parameters w --forward--> prediction --compare--> loss\n     ^                                           |\n     +----------- update <--- gradient <--------+""",
        explanation="Gradient không phải công thức để học thuộc: nó là mũi tên cho biết nên đổi tham số theo hướng nào để loss giảm.",
    ),
    "statistics": LearningVisual(
        title="Thống kê: mẫu chỉ là cửa sổ nhìn vào quần thể",
        diagram="""population -> sample -> statistic -> uncertainty -> decision\n                 (biased?)       |\n                                  +--> check assumptions""",
        explanation="Một con số tóm tắt không tự nói lên sự thật. Bạn cần xem kích thước mẫu, outlier và giả định trước khi kết luận.",
    ),
    "data": LearningVisual(
        title="Data pipeline: biến dữ liệu thô thành feature đáng tin",
        diagram="""raw data -> validate -> clean -> transform -> feature table\n                 |                    |\n                 +---- bad schema ----+--> quarantine / fix rule""",
        explanation="Chất lượng model bị giới hạn bởi chất lượng dữ liệu. Mỗi mũi tên cần một quy tắc có thể chạy lại và kiểm tra được.",
    ),
    "ai": LearningVisual(
        title="AI system: mục tiêu thật quan trọng hơn model to",
        diagram="""user need -> task + metric -> baseline -> model -> user feedback\n                               ^                         |\n                               +---- failure analysis ----+""",
        explanation="Một model chỉ hữu ích khi task, metric và chi phí sai được mô tả rõ; feedback thực tế là phần bắt buộc của hệ thống AI.",
    ),
    "ml": LearningVisual(
        title="Machine Learning: học quy luật, không học thuộc đáp án",
        diagram="""train data -> features -> model -> prediction -> loss\n                              ^                  |\n                              +---- update -------+\n\nvalidation data -----------------> generalization check""",
        explanation="Training loss thấp chưa đủ. Validation giúp phát hiện model đang học được quy luật hay chỉ đang nhớ noise của tập train.",
    ),
    "dl": LearningVisual(
        title="Deep Learning: forward để dự đoán, backward để sửa trọng số",
        diagram="""x -> [layer 1] -> [layer 2] -> y_hat -> loss\n     ^                                  |\n     +---- gradients <- backward <------+""",
        explanation="Mỗi layer tạo representation mới. Backpropagation chuyển tín hiệu lỗi ngược lại để từng trọng số nhận được hướng cập nhật.",
    ),
    "mlops": LearningVisual(
        title="MLOps: model chỉ bắt đầu sau khi rời notebook",
        diagram="""data + code + config -> train -> registry -> deploy\n       ^                                      |\n       +------ monitor <--- production <-----+""",
        explanation="Một vòng lặp MLOps tốt phải truy được model được train từ dữ liệu, code và cấu hình nào; monitor sẽ cho biết khi nào cần lặp lại.",
    ),
    "django": LearningVisual(
        title="Django: request đi qua các lớp có trách nhiệm rõ ràng",
        diagram="""browser -> URL -> view -> service/model -> PostgreSQL\n   ^                                             |\n   +------------- template / JSON response <----+""",
        explanation="Tách route, xử lý nghiệp vụ và lưu trữ dữ liệu làm code dễ test hơn, đồng thời giúp auth và permission được đặt đúng chỗ.",
    ),
    "fastapi": LearningVisual(
        title="FastAPI: contract trước, xử lý sau",
        diagram="""Django/client -> request schema -> route -> service\n                                      |          |\n                              validation error    +-> response schema""",
        explanation="Schema là ranh giới bảo vệ service: input sai bị chặn sớm, output ổn định để Django hoặc client có thể xử lý an toàn.",
    ),
}


DEFAULT_LEARNING_MAP = LearningMap(
    mental_model=(
        "Xem topic này như một hệ thống có input, transformation, output và "
        "feedback. Muốn hiểu bản chất, hãy luôn hỏi dữ liệu đi vào là gì, quy "
        "tắc biến đổi nằm ở đâu, và kết quả được kiểm chứng bằng cách nào."
    ),
    pipeline=(
        "Định nghĩa vấn đề bằng ngôn ngữ đơn giản.",
        "Viết ví dụ nhỏ có thể chạy được.",
        "Kiểm tra kết quả đúng, sai và trường hợp rỗng.",
        "Tổng quát hóa thành hàm, class hoặc API contract.",
    ),
    edge_cases=(
        "Input rỗng, None, kiểu dữ liệu sai hoặc kích thước lớn.",
        "Kết quả nhìn đúng nhưng sai định dạng, sai thứ tự hoặc sai rounding.",
        "Code chạy trên máy cá nhân nhưng lỗi khi vào container/service.",
    ),
    mistakes=(
        "Học thuộc cú pháp mà không tự tạo ví dụ phản chứng.",
        "Bỏ qua lỗi và chỉ nhìn output của happy path.",
        "Không viết test nhỏ trước khi ghép vào hệ thống lớn.",
    ),
    practice_loop=(
        "Chạy starter code trong sandbox.",
        "Đổi một biến để dự đoán output trước khi chạy lại.",
        "Thêm một edge case và xem chương trình có gãy không.",
        "Chụp ảnh lời giải cuối cùng để OCR chấm checkpoint.",
    ),
)


TRACK_LEARNING_MAPS: dict[str, LearningMap] = {
    "python": LearningMap(
        mental_model=(
            "Python là cách mô tả dữ liệu và hành động theo từng bước. Bản chất "
            "không nằm ở câu lệnh riêng lẻ, mà ở việc biến trạng thái ban đầu "
            "thành trạng thái mong muốn bằng biểu thức, nhánh và vòng lặp."
        ),
        pipeline=(
            "Đọc đề và xác định input/output.",
            "Tạo biến đại diện cho dữ liệu.",
            "Biến đổi dữ liệu bằng expression, if, loop hoặc function.",
            "In hoặc return kết quả theo đúng format.",
        ),
        edge_cases=(
            "Chuỗi rỗng, list rỗng, số 0 và giá trị None.",
            "Indentation sai khiến logic đổi nghĩa.",
            "So sánh string và number như nhau nhưng thực chất khác kiểu.",
        ),
        mistakes=(
            "Dùng print thay cho return trong hàm cần trả dữ liệu.",
            "Quên chuyển kiểu từ input() vì input luôn trả string.",
            "Viết loop chạy đúng một ví dụ nhưng sai khi list dài hoặc rỗng.",
        ),
        practice_loop=DEFAULT_LEARNING_MAP.practice_loop,
    ),
    "python_pro": LearningMap(
        mental_model=(
            "Python chuyên sâu là quản trị độ phức tạp: chia trách nhiệm, kiểm "
            "soát side effect, viết API nhỏ và làm cho code dễ test khi project lớn."
        ),
        pipeline=(
            "Tách pure logic khỏi I/O.",
            "Đóng gói dữ liệu bằng function, dataclass hoặc class.",
            "Viết test cho contract trước khi tối ưu.",
            "Refactor để tên gọi phản ánh đúng trách nhiệm.",
        ),
        edge_cases=(
            "Mutable default argument bị chia sẻ giữa nhiều lần gọi.",
            "Exception bị nuốt mất làm lỗi thật khó truy vết.",
            "Import vòng tròn khi module phụ thuộc ngược nhau.",
        ),
        mistakes=(
            "Tạo class khi function đơn giản là đủ.",
            "Tối ưu sớm trước khi đo bằng dữ liệu.",
            "Trộn parsing, xử lý và render trong một hàm dài.",
        ),
        practice_loop=DEFAULT_LEARNING_MAP.practice_loop,
    ),
    "engineering": LearningMap(
        mental_model=(
            "Software Engineering là biến code chạy được thành code đáng tin. "
            "Bạn học cách kiểm soát version, dependency, test, review và deploy."
        ),
        pipeline=(
            "Đóng gói thay đổi nhỏ có mục tiêu rõ.",
            "Viết test cho hành vi quan trọng.",
            "Chạy lint/test trước khi ghép vào nhánh chính.",
            "Ghi lại command và cấu hình cần thiết.",
        ),
        edge_cases=(
            "Dependency khác version giữa local và Docker.",
            "Test phụ thuộc thời gian, network hoặc thứ tự chạy.",
            "Config bí mật bị commit hoặc lộ qua log.",
        ),
        mistakes=(
            "Tin rằng code chạy local nghĩa là production ổn.",
            "Không có rollback path khi deploy lỗi.",
            "Không đọc error log theo thứ tự nguyên nhân.",
        ),
        practice_loop=DEFAULT_LEARNING_MAP.practice_loop,
    ),
    "math": LearningMap(
        mental_model=(
            "Toán cho AI là ngôn ngữ của cấu trúc: vector mô tả dữ liệu, ma trận "
            "mô tả phép biến đổi, đạo hàm mô tả hướng thay đổi, tối ưu tìm trạng "
            "thái tốt hơn."
        ),
        pipeline=(
            "Vẽ đại lượng thành vector, điểm, đường hoặc surface.",
            "Viết công thức nhỏ rồi thay số cụ thể.",
            "Nhìn chiều, đơn vị và miền giá trị trước khi tính.",
            "Liên hệ công thức với loss, gradient hoặc model decision.",
        ),
        edge_cases=(
            "Chia cho 0, log của số không dương, overflow khi exp quá lớn.",
            "Nhầm shape vector hàng/cột làm phép nhân ma trận sai.",
            "Đạo hàm đúng công thức nhưng sai ý nghĩa hướng giảm loss.",
        ),
        mistakes=(
            "Học công thức mà không biết công thức đo cái gì.",
            "Bỏ qua giả định tuyến tính, độc lập hoặc khả vi.",
            "Không kiểm tra bằng ví dụ 2D có thể vẽ được.",
        ),
        practice_loop=DEFAULT_LEARNING_MAP.practice_loop,
    ),
    "statistics": LearningMap(
        mental_model=(
            "Xác suất và thống kê là cách suy luận khi không chắc chắn. Bạn không "
            "chỉ hỏi model đúng chưa, mà hỏi bằng chứng mạnh đến đâu và sai lệch "
            "đến từ dữ liệu hay từ giả định."
        ),
        pipeline=(
            "Xác định biến ngẫu nhiên và phân phối giả định.",
            "Tóm tắt dữ liệu bằng mean, variance, quantile hoặc histogram.",
            "Ước lượng tham số và đo độ bất định.",
            "Diễn giải kết quả bằng confidence, risk và bias.",
        ),
        edge_cases=(
            "Sample nhỏ làm kết luận dao động mạnh.",
            "Outlier kéo mean lệch khỏi trung tâm thực tế.",
            "Correlation bị hiểu nhầm thành causation.",
        ),
        mistakes=(
            "Chỉ nhìn accuracy mà bỏ qua base rate.",
            "Leak test data vào quá trình chọn model.",
            "Không phân biệt population, sample và estimator.",
        ),
        practice_loop=DEFAULT_LEARNING_MAP.practice_loop,
    ),
    "data": LearningMap(
        mental_model=(
            "Data Engineering là biến dữ liệu bẩn, phân tán và thay đổi thành dữ "
            "liệu có contract. ML chỉ tốt khi pipeline dữ liệu ổn định."
        ),
        pipeline=(
            "Ingest dữ liệu từ file, API hoặc database.",
            "Validate schema, kiểu dữ liệu và missing values.",
            "Transform thành feature hoặc bảng phân tích.",
            "Lưu kết quả với lineage và khả năng chạy lại.",
        ),
        edge_cases=(
            "Timestamp lệch timezone hoặc format.",
            "Duplicate record làm metric phồng lên.",
            "Schema drift phá code transform sau vài tuần.",
        ),
        mistakes=(
            "Sửa dữ liệu bằng tay mà không ghi lại rule.",
            "Không phân biệt raw, cleaned và feature table.",
            "Không kiểm tra row count trước/sau transform.",
        ),
        practice_loop=DEFAULT_LEARNING_MAP.practice_loop,
    ),
    "ai": LearningMap(
        mental_model=(
            "AI là hệ thống ra quyết định dựa trên dữ liệu, mục tiêu và phản hồi. "
            "Bản chất nằm ở việc biểu diễn bài toán đúng, không phải gọi một model "
            "thật to."
        ),
        pipeline=(
            "Xác định task: classify, predict, rank, generate hay plan.",
            "Chọn dữ liệu và metric phản ánh mục tiêu thật.",
            "Xây baseline đơn giản trước model phức tạp.",
            "Đánh giá lỗi theo nhóm case, không chỉ điểm trung bình.",
        ),
        edge_cases=(
            "Dữ liệu huấn luyện không giống dữ liệu thực tế.",
            "Metric đẹp nhưng user experience xấu.",
            "Model tự tin khi gặp input ngoài phân phối.",
        ),
        mistakes=(
            "Nhảy ngay vào deep learning khi rule/baseline chưa có.",
            "Không định nghĩa failure cost.",
            "Không tách training, validation và test đúng cách.",
        ),
        practice_loop=DEFAULT_LEARNING_MAP.practice_loop,
    ),
    "ml": LearningMap(
        mental_model=(
            "Machine Learning là tối ưu một hàm dự đoán để giảm lỗi trên dữ liệu "
            "chưa thấy. Bạn cần hiểu feature, loss, regularization và generalization."
        ),
        pipeline=(
            "Tạo baseline và chia dữ liệu đúng.",
            "Chọn feature, model và loss phù hợp.",
            "Train, validate, tune rồi khóa test set.",
            "Phân tích lỗi để biết model học gì và bỏ sót gì.",
        ),
        edge_cases=(
            "Data leakage làm kết quả ảo.",
            "Class imbalance khiến accuracy đánh lừa.",
            "Overfitting khi model thuộc lòng noise.",
        ),
        mistakes=(
            "Tune trên test set.",
            "Không so với baseline đơn giản.",
            "Không lưu pipeline tiền xử lý cùng model.",
        ),
        practice_loop=DEFAULT_LEARNING_MAP.practice_loop,
    ),
    "mlops": LearningMap(
        mental_model=(
            "MLOps là vòng đời model sau notebook: version dữ liệu, train lặp lại "
            "được, deploy có rollback, monitoring phát hiện drift và lỗi."
        ),
        pipeline=(
            "Đóng gói training/inference thành pipeline.",
            "Lưu artifact, metric, config và data version.",
            "Deploy qua API hoặc batch job có health check.",
            "Monitor latency, quality, drift và feedback.",
        ),
        edge_cases=(
            "Model mới tốt offline nhưng giảm quality online.",
            "Feature training và serving tính khác nhau.",
            "Traffic spike làm inference timeout.",
        ),
        mistakes=(
            "Không lưu seed/config nên không reproduce được.",
            "Deploy model không có contract input/output.",
            "Chỉ monitor uptime mà không monitor quality.",
        ),
        practice_loop=DEFAULT_LEARNING_MAP.practice_loop,
    ),
    "dl": LearningMap(
        mental_model=(
            "Deep Learning học biểu diễn nhiều tầng bằng gradient descent. Mỗi "
            "layer biến dữ liệu thành đặc trưng trừu tượng hơn, loss điều khiển "
            "hướng cập nhật trọng số."
        ),
        pipeline=(
            "Chuẩn hóa tensor shape và scale.",
            "Chọn architecture phù hợp dữ liệu.",
            "Train bằng forward, loss, backward, optimizer step.",
            "Theo dõi learning curve để phát hiện underfit/overfit.",
        ),
        edge_cases=(
            "Gradient vanish/explode.",
            "Batch size quá nhỏ làm train nhiễu, quá lớn tốn memory.",
            "Validation loss tăng dù training loss giảm.",
        ),
        mistakes=(
            "Không kiểm tra shape ở từng layer.",
            "Dùng model lớn khi dữ liệu ít.",
            "Quên set model train/eval trong framework DL.",
        ),
        practice_loop=DEFAULT_LEARNING_MAP.practice_loop,
    ),
}


TRACK_LEARNING_MAPS.update(
    {
        key: TRACK_LEARNING_MAPS.get("dl", DEFAULT_LEARNING_MAP)
        for key in ("cv", "nlp", "genai", "rl")
    }
)

ENGLISH_MENTAL_MODELS = {
    "python": "Python transforms an initial program state into a desired state through expressions, branches, loops, and functions. Trace data before focusing on syntax.",
    "math": "Math for AI describes structure: vectors represent data, matrices transform it, and derivatives show which direction reduces loss.",
    "statistics": "Statistics supports decisions under uncertainty; every result needs its sample, assumptions, and possible bias.",
    "data": "Data engineering turns messy inputs into a reproducible, validated contract that analytics and ML can trust.",
    "ai": "An AI system connects a user need, a measurable task, a decision rule or model, and feedback from the real world.",
    "ml": "Machine learning minimizes error on unseen data. Features, loss, regularization, and validation decide whether it generalizes.",
    "mlops": "MLOps is the model lifecycle after a notebook: versioned data, repeatable training, safe deployment, and quality monitoring.",
    "dl": "Deep learning learns layered representations. Forward passes predict; backpropagation turns error into weight updates.",
    "django": "Django assigns clear responsibilities: URL, view, model, database, and response work together as one request lifecycle.",
    "fastapi": "FastAPI is contract-first: schemas validate at the boundary, routes coordinate work, and structured responses keep services compatible.",
    "capstone": "A capstone connects users, data, models, APIs, storage, deployment, and monitoring into one demonstrable product.",
}

ENGLISH_LEARNING_MAP = LearningMap(
    mental_model="A technical topic is a system: identify its input, transformation, output, and feedback loop before memorizing syntax.",
    pipeline=("Define input, output, and success in plain language.", "Build the smallest runnable example.", "Check a normal, failure, and boundary case.", "Generalize it into a function, class, or API contract."),
    edge_cases=("Empty input, None, invalid types, or a large input size.", "Correct-looking output with wrong order, format, or rounding.", "Code that works locally but fails at a service or container boundary."),
    mistakes=("Memorizing syntax without creating a counterexample.", "Testing only a happy path and ignoring error output.", "Skipping a small test before composing a larger system."),
    practice_loop=("Run starter code in the sandbox.", "Change one variable and predict the output.", "Add one edge case and observe the result.", "Explain the solution, then submit the checkpoint."),
)

ENGLISH_LEARNING_VISUAL = LearningVisual(
    title="See the processing loop before you learn the syntax",
    diagram="""input
  |
  v
[rule / model] ---> output
       ^              |
       |---- feedback-+""",
    explanation="Every technical lesson asks what enters the system, which transformation creates the result, and which feedback proves it correct.",
)
TRACK_LEARNING_MAPS.update(
    {
        "django": LearningMap(
            mental_model=(
                "Django là backend nguyên khối có pin sẵn: URL nhận request, view "
                "xử lý, model lưu database, template/API trả response, admin quản trị."
            ),
            pipeline=(
                "Thiết kế model và migration.",
                "Viết view/form/serializer cho luồng chính.",
                "Bảo vệ auth, CSRF và permission.",
                "Test request, database side effect và template output.",
            ),
            edge_cases=(
                "User chưa đăng nhập nhưng gọi endpoint ghi dữ liệu.",
                "Query N+1 làm page chậm khi dữ liệu lớn.",
                "Form hợp lệ ở UI nhưng serializer API lại nhận contract khác.",
            ),
            mistakes=(
                "Đưa business logic dài vào template.",
                "Bỏ permission ở API vì page HTML đã có login.",
                "Không test migration/seed khi schema đổi.",
            ),
            practice_loop=DEFAULT_LEARNING_MAP.practice_loop,
        ),
        "fastapi": LearningMap(
            mental_model=(
                "FastAPI là microservice contract-first: type hint và Pydantic mô "
                "tả dữ liệu, route xử lý task chuyên biệt, OpenAPI giúp service khác gọi đúng."
            ),
            pipeline=(
                "Định nghĩa request/response schema.",
                "Validate input trước khi chạy tác vụ nặng.",
                "Tách service logic khỏi route.",
                "Trả lỗi có cấu trúc để Django xử lý ổn định.",
            ),
            edge_cases=(
                "Timeout giữa Django và FastAPI.",
                "Payload lớn làm OCR/sandbox quá tải.",
                "Exception lộ stack trace thay vì message an toàn.",
            ),
            mistakes=(
                "Để browser gọi thẳng microservice nội bộ.",
                "Không version API contract.",
                "Không test validation và failure path.",
            ),
            practice_loop=DEFAULT_LEARNING_MAP.practice_loop,
        ),
        "capstone": LearningMap(
            mental_model=(
                "Capstone là lúc ghép mọi mảnh thành sản phẩm: người dùng, dữ liệu, "
                "model, API, database, deployment và monitoring cùng hoạt động."
            ),
            pipeline=(
                "Chọn problem có người dùng thật.",
                "Thiết kế data/model/API/UI contract.",
                "Ship bản nhỏ nhưng chạy được end-to-end.",
                "Đo lỗi, cải thiện và ghi lại quyết định kỹ thuật.",
            ),
            edge_cases=(
                "Demo đẹp nhưng không có đường xử lý lỗi.",
                "Model tốt nhưng không tích hợp được vào product.",
                "Thiếu README/runbook khiến người khác không chạy lại được.",
            ),
            mistakes=(
                "Xây quá rộng trước khi có vertical slice.",
                "Không có test smoke cho luồng quan trọng.",
                "Không ghi trade-off nên portfolio khó thuyết phục.",
            ),
            practice_loop=DEFAULT_LEARNING_MAP.practice_loop,
        ),
    }
)


def get_learning_map(track: str, language: str = "vi") -> LearningMap:
    """Return a structured teaching scaffold for a lesson track."""
    if language == "en":
        return LearningMap(
            mental_model=ENGLISH_MENTAL_MODELS.get(track, ENGLISH_LEARNING_MAP.mental_model),
            pipeline=ENGLISH_LEARNING_MAP.pipeline,
            edge_cases=ENGLISH_LEARNING_MAP.edge_cases,
            mistakes=ENGLISH_LEARNING_MAP.mistakes,
            practice_loop=ENGLISH_LEARNING_MAP.practice_loop,
        )
    return TRACK_LEARNING_MAPS.get(track, DEFAULT_LEARNING_MAP)


def get_learning_visual(track: str, language: str = "vi") -> LearningVisual:
    """Return an approachable diagram for the current curriculum track."""
    if language == "en":
        return ENGLISH_LEARNING_VISUAL
    return TRACK_LEARNING_VISUALS.get(track, DEFAULT_LEARNING_VISUAL)
