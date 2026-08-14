"""The extended Master Python and ML Engineering learning path.

The browser platform uses one small OCR-checkable Python exercise per lesson.
The lesson text also names a deeper notebook, repository, or system-design lab
because a standard-library sandbox cannot faithfully execute PyTorch, pandas,
Docker, Django, or cloud infrastructure.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class Topic:
    """One curriculum topic rendered through the shared lesson factory."""

    slug: str
    title: str
    summary: str
    level: str = "intermediate"
    minutes: int = 45
    lab: str = ""


def topic(
    slug: str,
    title: str,
    summary: str,
    level: str = "intermediate",
    minutes: int = 45,
    lab: str = "",
) -> Topic:
    """Keep the large declarative catalogue compact and consistent."""
    return Topic(slug, title, summary, level, minutes, lab)


TRACK_CONTEXT: dict[str, tuple[str, str, str]] = {
    "python_pro": (
        "Python 3.12, standard library và công cụ kiểm thử",
        "mã có type rõ ràng, test được và dễ quan sát khi lỗi",
        "Tạo một package nhỏ có test, CLI, logging và cấu hình an toàn.",
    ),
    "engineering": (
        "Git, SQL, Docker và CI/CD",
        "thay đổi có thể review, tái lập và rollback",
        "Đưa một service qua lint, test, container và pipeline CI.",
    ),
    "math": (
        "đại số tuyến tính, giải tích và tối ưu",
        "giải thích được phép toán thay vì chỉ gọi thư viện",
        "Tự cài một phép tính NumPy và giải thích trực giác hình học của nó.",
    ),
    "statistics": (
        "xác suất, thống kê suy luận và information theory",
        "không suy diễn quá mức từ mẫu dữ liệu hoặc metric đơn lẻ",
        "Làm notebook mô phỏng dữ liệu, ước lượng và diễn giải bất định.",
    ),
    "data": (
        "NumPy, pandas, SQL và orchestration dữ liệu",
        "schema, lineage và chất lượng dữ liệu được kiểm tra trước training",
        "Xây pipeline dữ liệu có kiểm tra schema, EDA và báo cáo chất lượng.",
    ),
    "ai": (
        "problem framing, evaluation và Responsible AI",
        "mục tiêu sản phẩm, rủi ro và human review được xác định trước mô hình",
        "Viết AI design brief gồm metric, rủi ro, guardrail và kế hoạch đánh giá.",
    ),
    "ml": (
        "scikit-learn, validation và thiết kế feature",
        "baseline, split, metric và leakage được kiểm soát",
        "Huấn luyện pipeline tabular có experiment report và phân tích lỗi.",
    ),
    "mlops": (
        "versioning, registry, serving, monitoring và CI/CD",
        "model có thể tái lập, quan sát và vận hành khi dữ liệu thay đổi",
        "Triển khai một model service có registry, test, dashboard và rollback plan.",
    ),
    "dl": (
        "PyTorch, GPU, autograd và training loop",
        "training ổn định, tái lập và tối ưu cho inference",
        "Huấn luyện mô hình PyTorch, log experiment và tối ưu checkpoint inference.",
    ),
    "cv": (
        "OpenCV, PyTorch vision và dữ liệu ảnh",
        "nhãn, metric và lỗi theo lát dữ liệu được kiểm soát",
        "Xây vision pipeline có augmentation, evaluation và error analysis.",
    ),
    "nlp": (
        "tokenization, embedding, retrieval và transformer",
        "chất lượng ngôn ngữ, multilingual behavior và dữ liệu nhạy cảm được đánh giá",
        "Xây NLP notebook có dataset card, metric và phân tích lỗi tiếng Việt.",
    ),
    "genai": (
        "LLM, RAG, tool use, guardrail và observability",
        "câu trả lời có grounding, đánh giá và cơ chế human approval",
        "Xây RAG assistant có evaluation set, citation và phòng vệ prompt injection.",
    ),
    "rl": (
        "MDP, value learning, policy optimization và safety",
        "reward, exploration và giới hạn an toàn được mô hình hóa tường minh",
        "Huấn luyện agent trong môi trường mô phỏng, log reward và kiểm tra safety.",
    ),
    "django": (
        "Django, DRF, Redis/Celery và vận hành web",
        "auth, permission, query và background work được test end-to-end",
        "Đóng gói dashboard ML product có auth, queue và audit log.",
    ),
    "fastapi": (
        "FastAPI, Pydantic, async, OpenAPI và resilience",
        "API contract, timeout, retry, auth và telemetry được kiểm chứng",
        "Đưa inference API qua contract test, load test và observability.",
    ),
    "capstone": (
        "repository, notebook, service, architecture và portfolio",
        "dự án chứng minh được quyết định kỹ thuật bằng test và evaluation report",
        "Hoàn thiện Git repository, README, diagram, demo, test và retrospective.",
    ),
}


PYTHON_PRO_TOPICS = (
    topic("iterators-generators", "Iterable, iterator, generator và yield", "Xử lý stream dữ liệu hiệu quả mà không giữ toàn bộ collection trong RAM."),
    topic("functional-closures", "Higher-order function, closure và functools", "Đóng gói hành vi có thể tái sử dụng, nhưng vẫn giữ code dễ đọc và dễ debug."),
    topic("decorators-context-managers", "Decorator và context manager", "Thêm logging, timing hoặc quản lý resource mà không làm rối business logic."),
    topic("oop-composition-protocols", "OOP nâng cao, composition và dunder method", "Thiết kế object theo trách nhiệm rõ ràng thay vì lạm dụng kế thừa."),
    topic("typing-generics-protocol", "Type hints, generic và Protocol", "Dùng typing để làm contract rõ ràng trong codebase ML lớn."),
    topic("packaging-pyproject", "Packaging với pyproject.toml", "Đóng gói thư viện Python có dependency, version và build metadata đúng chuẩn."),
    topic("sqlite-transactions", "SQLite, DB-API và transaction", "Dùng query có tham số, transaction và xử lý lỗi dữ liệu cục bộ an toàn."),
    topic("threading-multiprocessing", "Thread, process và concurrent futures", "Chọn mô hình concurrency theo CPU-bound, I/O-bound và chi phí chia sẻ dữ liệu."),
    topic("asyncio-concurrency", "asyncio, cancellation và async I/O", "Xây client/service bất đồng bộ mà không block event loop."),
    topic("profiling-security-cli", "Profiling, caching, security và production CLI", "Đo hiệu năng, xử lý input không tin cậy và ship công cụ dòng lệnh có logging." , "advanced", 60),
)

ENGINEERING_TOPICS = (
    topic("shell-filesystem", "Terminal, filesystem và process", "Làm việc tự tin với shell, environment variable, pipe và process lifecycle.", "beginner"),
    topic("git-collaboration", "Git, branch, rebase và code review", "Duy trì lịch sử thay đổi dễ review, xử lý conflict và hợp tác qua pull request.", "beginner"),
    topic("pytest-quality", "pytest, fixture, mock và quality gate", "Thiết kế test có fixture, mock hợp lý và regression test cho thay đổi quan trọng."),
    topic("lint-format-typecheck", "Ruff, formatter, type checker và pre-commit", "Tự động hóa chuẩn code trước khi mã vào nhánh chính."),
    topic("sql-modeling-joins", "Data modeling, SQL join và window function", "Mô hình hóa dữ liệu quan hệ và viết truy vấn analytics đáng tin cậy."),
    topic("indexes-transactions", "Index, transaction, query plan và isolation", "Đọc EXPLAIN, tránh N+1 query và hiểu đánh đổi nhất quán dữ liệu.", "advanced"),
    topic("docker-ci-cd", "Docker, image, network, volume và CI/CD", "Đóng gói ứng dụng tái lập và tự động test/build/release.", "advanced"),
    topic("application-security", "Application security và threat modeling", "Bảo vệ secret, auth, input, dependency và hành vi nguy hiểm theo nguyên tắc least privilege.", "advanced"),
)

MATH_TOPICS = (
    topic("sets-logic-notation", "Tập hợp, logic và ký hiệu toán", "Đọc công thức ML, biểu diễn điều kiện và suy luận logic chính xác.", "beginner"),
    topic("vectors-scalars", "Scalar, vector, basis và feature space", "Biểu diễn feature và hiểu vector như một điểm/hướng trong không gian dữ liệu.", "beginner"),
    topic("matrices-linear-transformations", "Ma trận và biến đổi tuyến tính", "Hiểu layer tuyến tính trong neural network như một phép biến đổi không gian.", "beginner"),
    topic("matrix-multiplication-systems", "Nhân ma trận và hệ phương trình", "Tính shape đúng, hiểu broadcast và giải hệ tuyến tính cơ bản.", "beginner"),
    topic("rank-inverse-linear-solve", "Rank, inverse và linear solve", "Nhận biết ma trận suy biến và ưu tiên solve ổn định hơn inverse."),
    topic("eigenvalues-svd-pca", "Eigenvalue, SVD và trực giác PCA", "Hiểu hướng biến thiên chính, giảm chiều và nén biểu diễn."),
    topic("norms-distances-similarity", "Norm, distance và cosine similarity", "Chọn thước đo gần nhau phù hợp cho retrieval, clustering và regularization."),
    topic("derivatives-partials", "Đạo hàm, đạo hàm riêng, Jacobian và Hessian", "Tính độ nhạy của loss theo từng tham số trong mô hình nhiều biến."),
    topic("chain-rule-backprop", "Chain rule và toán của backpropagation", "Theo dõi gradient qua computation graph và nhận biết điểm gây vanishing/exploding gradient."),
    topic("optimization-gradient-descent", "Convexity, gradient descent, momentum và Adam", "Chọn learning rate, optimizer và chẩn đoán đường loss.", "intermediate", 60),
    topic("constrained-numerical", "Lagrange multiplier, numerical stability và floating point", "Xử lý ràng buộc, overflow, underflow và sai số số học trong training.", "advanced", 60),
    topic("math-ml-capstone", "Tự cài linear/logistic regression bằng NumPy", "Kết nối đại số tuyến tính, loss và gradient thành một model có kiểm thử.", "advanced", 75),
)

STATISTICS_TOPICS = (
    topic("probability-axioms-combinatorics", "Tiên đề xác suất và tổ hợp", "Mô hình hóa sample space, event và xác suất của biến cố.", "beginner"),
    topic("conditional-bayes", "Xác suất có điều kiện và Bayes", "Cập nhật niềm tin theo evidence và tránh nhầm base-rate.", "beginner"),
    topic("random-variables-distributions", "Biến ngẫu nhiên và phân phối", "So sánh Bernoulli, categorical, Gaussian và đuôi phân phối."),
    topic("expectation-variance-covariance", "Expectation, variance, covariance và correlation", "Đo trung tâm, độ phân tán và quan hệ biến số mà không nhầm correlation với causation."),
    topic("sampling-lln-clt", "Sampling, LLN và CLT", "Hiểu khi nào thống kê mẫu ổn định và khi nào nó chưa đáng tin."),
    topic("estimation-confidence-intervals", "Ước lượng, bootstrap và confidence interval", "Báo cáo bất định bên cạnh point estimate."),
    topic("hypothesis-testing-ab", "Hypothesis test, p-value, power và A/B test", "Thiết kế thử nghiệm, tránh p-hacking và diễn giải ý nghĩa thực tiễn."),
    topic("likelihood-entropy-kl", "Likelihood, MLE/MAP, entropy và KL divergence", "Kết nối xác suất với cross-entropy loss và đánh giá distribution shift.", "advanced", 60),
)

DATA_TOPICS = (
    topic("numpy-arrays-shapes", "NumPy array, dtype, shape và vectorization", "Tránh loop Python không cần thiết và kiểm soát shape trong pipeline số học.", "beginner"),
    topic("pandas-dataframes", "pandas DataFrame, index, merge và groupby", "Biến dữ liệu bảng thô thành feature có thể kiểm tra.", "beginner"),
    topic("formats-csv-json-parquet", "CSV, JSON, Parquet và schema", "Chọn format trao đổi dữ liệu theo kích thước, type và khả năng evolve schema."),
    topic("cleaning-quality", "Missing value, duplicate, outlier và data quality", "Phát hiện dữ liệu hỏng trước khi nó đi vào training hoặc metric."),
    topic("eda-visualization", "EDA, distribution, correlation và visualization", "Đặt câu hỏi tốt bằng biểu đồ trước khi chọn model."),
    topic("sql-analytics", "SQL analytics, join, window và dimensional model", "Xây dataset training từ nguồn quan hệ có lineage rõ ràng."),
    topic("time-geospatial-leakage", "Dữ liệu thời gian, geospatial và leakage", "Chia dữ liệu đúng theo thời gian và tránh nhìn thấy tương lai."),
    topic("splitting-stratification", "Sampling, split, stratification và imbalance", "Tạo train/validation/test đại diện cho bài toán thật."),
    topic("preprocessing-pipelines", "Encoding, scaling, imputation và sklearn pipeline", "Giữ preprocessing nhất quán giữa training và inference."),
    topic("etl-elt-orchestration", "ETL/ELT, batch pipeline và orchestration", "Lập lịch, retry và backfill pipeline mà vẫn biết lineage."),
    topic("warehouse-lakehouse", "Warehouse, lake, lakehouse và feature dataset", "Chọn kiến trúc lưu trữ phục vụ analytics và ML đúng chi phí."),
    topic("data-pipeline-project", "Dự án data quality pipeline", "Xây pipeline từ raw data đến curated dataset có test và báo cáo chất lượng.", "advanced", 75),
)

AI_TOPICS = (
    topic("problem-framing-objectives", "Problem framing, objective và baseline", "Quyết định AI có đáng dùng không, xác định user value, constraint và baseline."),
    topic("data-centric-lifecycle", "Data-centric AI, annotation và feedback loop", "Ưu tiên chất lượng dữ liệu, guideline nhãn và vòng phản hồi hơn chạy nhiều model."),
    topic("fairness-privacy-security", "Fairness, privacy, security và misuse", "Đánh giá bias, PII, prompt injection và nguy cơ lạm dụng theo bối cảnh."),
    topic("paper-reading-reproducibility", "Đọc paper, ablation và reproducible research", "Đọc nghiên cứu có phản biện, tái tạo kết quả và phân biệt claim với evidence.", "advanced"),
)

ML_TOPICS = (
    topic("preprocessing-regularization", "Preprocessing, bias-variance và regularization", "Điều khiển overfit bằng baseline, regularization và validation đúng."),
    topic("svm-kernels", "SVM, margin và kernel", "Hiểu hyperplane, support vector và khi kernel còn phù hợp."),
    topic("naive-bayes", "Naive Bayes và probabilistic classifier", "Dùng prior/likelihood cho baseline text hoặc dữ liệu nhỏ."),
    topic("boosting-tabular", "Random Forest, Gradient Boosting, XGBoost và LightGBM", "Chọn ensemble tabular, tune có kỷ luật và theo dõi overfit."),
    topic("calibration-thresholds", "Calibration, threshold và decision cost", "Biến probability thành quyết định theo chi phí business thay vì accuracy đơn thuần."),
    topic("imbalanced-learning", "Imbalanced learning và resampling", "Đánh giá rare event bằng metric và sampling phù hợp."),
    topic("cross-validation-hpo", "Cross-validation, nested validation và HPO", "Tuning mà không rò rỉ test set hoặc chọn model theo may mắn."),
    topic("explainability", "Explainability: PDP, ICE, SHAP và error analysis", "Giải thích model với giới hạn đúng và phân tích lỗi theo lát dữ liệu."),
    topic("time-series-recommender", "Time series, anomaly detection và recommender", "Nhận diện khác biệt giữa dữ liệu IID, chuỗi thời gian và ranking problem."),
    topic("tabular-ml-capstone", "Capstone tabular ML production-ready", "Ship model tabular có pipeline, test, calibration, report và inference API.", "advanced", 75),
)

MLOPS_TOPICS = (
    topic("system-design-requirements", "ML system design và requirement", "Biến product requirement thành data, model, latency, cost và safety constraint."),
    topic("reproducibility-versioning", "Reproducibility, config và versioning", "Gắn data/code/config/model version để tái tạo một run."),
    topic("experiment-registry", "Experiment tracking, artifact và model registry", "So sánh run có hệ thống và promote model bằng metadata."),
    topic("orchestration-feature-store", "Pipeline orchestration và feature store", "Điều phối training/inference và tránh training-serving skew."),
    topic("docker-testing-contracts", "Docker cho ML, test data/model và contract", "Đóng gói môi trường và test cả schema lẫn hành vi model."),
    topic("batch-online-serving", "Batch, online serving, queue và autoscaling", "Chọn serving path theo latency, volume và chi phí."),
    topic("ci-cd-continuous-training", "CI/CD/CT, canary, shadow và rollback", "Triển khai model có guardrail và kế hoạch quay lui."),
    topic("drift-monitoring", "Data drift, concept drift và model monitoring", "Phát hiện model xuống cấp trước khi ảnh hưởng người dùng."),
    topic("observability-slo-incidents", "Logs, metrics, traces, SLO và incident response", "Vận hành ML service bằng tín hiệu, alert và runbook."),
    topic("governance-finops-capstone", "Governance, privacy, cost và MLOps capstone", "Cân bằng compliance, observability và chi phí cho hệ ML production.", "advanced", 75),
)

DL_TOPICS = (
    topic("tensors-autograd", "Tensor, autograd và computation graph", "Theo dõi gradient và shape qua PyTorch graph."),
    topic("dataset-dataloader", "Dataset, DataLoader và augmentation", "Tạo input pipeline có shuffle, batching và reproducibility."),
    topic("optimizers-schedulers", "Optimizer, scheduler và learning-rate policy", "Chọn SGD/Adam, warmup và schedule dựa trên learning curve."),
    topic("initialization-normalization", "Initialization, normalization và stable training", "Giảm vanishing/exploding gradient bằng khởi tạo và normalization."),
    topic("regularization-mixed-precision", "Dropout, weight decay, mixed precision và GPU", "Cân bằng generalization, throughput và numerical stability."),
    topic("training-debugging", "Debug training, checkpoint và reproducibility", "Chẩn đoán overfit, data bug, non-determinism và checkpoint corruption."),
    topic("cnn-transfer-learning", "CNN, ResNet/EfficientNet và transfer learning", "Fine-tune backbone vision theo dataset nhỏ và metric đúng."),
    topic("transformer-internals", "Attention, Transformer và positional encoding", "Hiểu self-attention, mask và complexity trước khi dùng LLM."),
    topic("representation-generative", "Embedding, self-supervised, VAE, GAN và diffusion", "Phân biệt representation learning với generative modeling."),
    topic("inference-optimization", "Distributed training, quantization, ONNX và inference optimization", "Đưa model DL đến production với latency và memory hợp lý.", "advanced", 75),
)

CV_TOPICS = (
    topic("image-opencv", "Image representation, OpenCV và augmentation", "Hiểu pixel, color space, geometric transform và pipeline ảnh."),
    topic("classification-transfer", "Image classification và transfer learning", "Xây classifier có dataset split, augmentation và error analysis."),
    topic("detection-metrics", "Object detection, IoU, mAP và NMS", "Đánh giá box prediction đúng bằng IoU/mAP thay vì accuracy."),
    topic("segmentation", "Semantic/instance segmentation", "Phân biệt pixel-level label, mask metric và kiến trúc segmentation."),
    topic("ocr-document-ai", "OCR, layout và Document AI", "Tích hợp preprocessing, OCR confidence, structure extraction và human review."),
    topic("video-pose-tracking", "Video, pose, keypoint và tracking", "Xử lý temporal consistency, privacy và latency của vision video."),
    topic("vision-transformers-vlm", "Vision Transformer và vision-language model", "Hiểu patch embedding, multimodal alignment và đánh giá VLM."),
    topic("edge-vision-capstone", "Edge deployment và CV capstone", "Tối ưu model vision cho thiết bị, theo dõi lỗi thực tế và ship demo.", "advanced", 75),
)

NLP_TOPICS = (
    topic("normalization-tokenization", "Text normalization, tokenization và vocabulary", "Biết tokenization ảnh hưởng fairness, chi phí và chất lượng NLP."),
    topic("bow-tfidf-classification", "BoW, TF-IDF và text classification", "Xây baseline có thể giải thích trước neural/LLM."),
    topic("embeddings-similarity", "Embedding và semantic similarity", "Dùng vector representation cho search, clustering và duplicate detection."),
    topic("ner-sequence-labeling", "NER, sequence labeling và evaluation", "Đánh giá entity extraction bằng span-level metric."),
    topic("transformer-finetuning", "BERT/Transformer fine-tuning", "Fine-tune encoder model với split, scheduler và error analysis."),
    topic("retrieval-reranking", "Sparse/dense retrieval và reranking", "Thiết kế search multi-stage theo recall, precision và latency."),
    topic("vietnamese-multilingual", "Tiếng Việt, multilingual NLP và fairness", "Xử lý dấu, segmentation và chênh lệch chất lượng giữa nhóm ngôn ngữ."),
    topic("document-ai-capstone", "Document AI và NLP capstone", "Kết hợp OCR, extraction, validation và privacy cho tài liệu thật.", "advanced", 75),
)

GENAI_TOPICS = (
    topic("tokens-context-model-selection", "Token, context window và chọn model", "Chọn model theo capability, latency, privacy, cost và context requirement."),
    topic("prompt-design", "Prompt design, system instruction và few-shot", "Viết prompt rõ constraint, format và tiêu chí đánh giá thay vì prompt mơ hồ."),
    topic("structured-output-tools", "Structured output, function calling và tool contract", "Ép schema, validate output và tách tool permission khỏi text generation."),
    topic("ingestion-chunking-metadata", "Document ingestion, chunking và metadata", "Tạo corpus retrieval có chunk boundary, source và quyền truy cập đúng."),
    topic("embeddings-vector-search", "Embedding, vector database và hybrid search", "Thiết kế retrieval theo semantic, keyword, filter và latency."),
    topic("rag-evaluation", "RAG architecture, groundedness và evaluation", "Đo retrieval, answer quality, citation và hallucination bằng eval set."),
    topic("agents-approval", "Agent workflow, state, planning và human approval", "Giới hạn quyền tool, checkpoint hành động và xử lý failure có thể audit."),
    topic("prompt-injection-safety", "Prompt injection, jailbreak và data exfiltration defense", "Xây defense-in-depth cho untrusted document, tool và user input."),
    topic("fine-tuning-lora-serving", "Fine-tuning, LoRA, open model serving và cache", "Quyết định RAG hay adaptation, theo dõi quality/cost/latency."),
    topic("production-rag-capstone", "Production RAG assistant capstone", "Ship trợ lý có auth, citation, eval regression, tracing và incident plan.", "advanced", 90),
)

RL_TOPICS = (
    topic("mdp-rewards", "MDP, state, action, reward và policy", "Mô hình hóa sequential decision problem và reward không tạo shortcut nguy hiểm."),
    topic("value-bellman", "Value function và Bellman equation", "Hiểu backup operator trước khi implement dynamic programming."),
    topic("bandits-exploration", "Multi-armed bandit và exploration", "Cân bằng exploit/explore dưới uncertainty và business constraint."),
    topic("q-learning-td", "Temporal difference và Q-learning", "Học value từ transition, nhận biết instability của bootstrapping."),
    topic("policy-gradient-ppo", "Policy gradient, actor-critic và PPO", "Tối ưu policy với objective, entropy và clipping."),
    topic("offline-safe-rl", "Offline RL, safety, sim-to-real và capstone", "Đánh giá agent offline và không thử policy rủi ro trên hệ thật.", "advanced", 75),
)

DJANGO_TOPICS = (
    topic("relational-performance", "Relational modeling, ORM và query performance", "Thiết kế schema ML product, tránh N+1 và dùng transaction đúng chỗ."),
    topic("drf-security", "DRF auth, permission, throttling và API security", "Bảo vệ endpoint bằng permission, rate limit, serializer validation và audit."),
    topic("celery-redis-realtime", "Celery, Redis, cache và realtime job", "Chạy inference/background work mà không block HTTP request."),
    topic("django-production", "Django production security, observability và deployment", "Ship Django service có static/media strategy, telemetry và rollback plan.", "advanced", 60),
)

FASTAPI_TOPICS = (
    topic("sqlalchemy-alembic", "SQLAlchemy async, migration và transaction", "Thiết kế persistence layer có lifecycle và migration đáng tin cậy."),
    topic("oauth-rbac", "OAuth2, JWT, RBAC và API security", "Xác thực/ủy quyền đúng boundary và tránh token misuse."),
    topic("workers-queues-websocket", "Worker, queue, WebSocket và background inference", "Tách long-running job khỏi request lifecycle và báo trạng thái cho client."),
    topic("observability-resilience", "OpenAPI, telemetry, retry, timeout và deployment", "Làm service có contract, trace và resilience khi dependency lỗi.", "advanced", 60),
)

CAPSTONE_TOPICS = (
    topic("python-cli-package", "Capstone: Python CLI package", "Ship CLI có config, logging, type, test, release và documentation.", "advanced", 120),
    topic("data-pipeline-warehouse", "Capstone: data pipeline và warehouse", "Tạo dataset tin cậy có schema, lineage, quality check và dashboard.", "advanced", 150),
    topic("tabular-ml-product", "Capstone: tabular ML product", "Xây model tabular từ EDA đến API, evaluation report và monitoring.", "advanced", 180),
    topic("vision-or-nlp-product", "Capstone: vision hoặc Vietnamese NLP product", "Chọn một chuyên ngành, xử lý data, metric, model card và demo.", "advanced", 180),
    topic("rag-assistant-product", "Capstone: RAG assistant có guardrail", "Ship RAG có auth, evaluation, citation, tracing và prompt-injection defense.", "advanced", 210),
    topic("ml-platform-system-design", "Capstone: Django + FastAPI ML platform", "Tích hợp product UI, service inference, queue, PostgreSQL, Docker và observability.", "advanced", 240),
)


MASTER_TRACKS: tuple[tuple[str, str, int, str, tuple[Topic, ...]], ...] = (
    ("python_pro", "python", 19, "Python", PYTHON_PRO_TOPICS),
    ("engineering", "engineering", 1, "Engineering", ENGINEERING_TOPICS),
    ("math", "math", 1, "Toán AI", MATH_TOPICS),
    ("statistics", "statistics", 1, "Xác suất", STATISTICS_TOPICS),
    ("data", "data", 1, "Data", DATA_TOPICS),
    ("ai", "ai", 7, "AI", AI_TOPICS),
    ("ml", "ml", 9, "ML", ML_TOPICS),
    ("mlops", "mlops", 1, "MLOps", MLOPS_TOPICS),
    ("dl", "dl", 7, "DL", DL_TOPICS),
    ("cv", "cv", 1, "CV", CV_TOPICS),
    ("nlp", "nlp", 1, "NLP", NLP_TOPICS),
    ("genai", "genai", 1, "GenAI", GENAI_TOPICS),
    ("rl", "rl", 1, "RL", RL_TOPICS),
    ("django", "django", 7, "Django", DJANGO_TOPICS),
    ("fastapi", "fastapi", 7, "FastAPI", FASTAPI_TOPICS),
    ("capstone", "capstone", 1, "Capstone", CAPSTONE_TOPICS),
)


def _checkpoint(
    exercise_factory: Callable[..., dict[str, Any]],
    *,
    key: str,
    slug: str,
    title: str,
    position: int,
) -> dict[str, Any]:
    """Build a deterministic standard-library checkpoint for OCR grading."""
    template = position % 6
    challenge_title = f"Checkpoint · {title}"
    prompt_prefix = (
        f"Đây là checkpoint Python ngắn cho bài “{title}”. "
        "Lab chuyên sâu được mô tả trong nội dung bài học; OCR sandbox chỉ chạy "
        "Python standard library."
    )
    if template == 0:
        return exercise_factory(
            key=f"{key}-checkpoint",
            slug=f"{slug}-checkpoint",
            title=challenge_title,
            prompt=f"{prompt_prefix}\n\nTính tổng các số chẵn trong values và in kết quả.",
            starter_code="values = [3, 4, 7, 8]\n# TODO: in tổng các số chẵn\n",
            expected_output="12",
        )
    if template == 1:
        return exercise_factory(
            key=f"{key}-checkpoint",
            slug=f"{slug}-checkpoint",
            title=challenge_title,
            prompt=f"{prompt_prefix}\n\nTạo một dict summary có count và in count.",
            starter_code="items = [\"data\", \"model\", \"serve\"]\n# TODO: tạo summary và in số item\n",
            expected_output="3",
        )
    if template == 2:
        return exercise_factory(
            key=f"{key}-checkpoint",
            slug=f"{slug}-checkpoint",
            title=challenge_title,
            prompt=f"{prompt_prefix}\n\nDùng vòng lặp hoặc comprehension để in bình phương của numbers, cách nhau bởi dấu phẩy.",
            starter_code="numbers = [2, 3, 4]\n# TODO: in 4,9,16\n",
            expected_output="4,9,16",
        )
    if template == 3:
        return exercise_factory(
            key=f"{key}-checkpoint",
            slug=f"{slug}-checkpoint",
            title=challenge_title,
            prompt=f"{prompt_prefix}\n\nViết hàm normalize(text) trả về chuỗi lower-case đã bỏ khoảng trắng ngoài, rồi in kết quả.",
            starter_code="def normalize(text):\n    # TODO\n    pass\n\nprint(normalize(\"  ML Engineer  \"))\n",
            expected_output="ml engineer",
        )
    if template == 4:
        return exercise_factory(
            key=f"{key}-checkpoint",
            slug=f"{slug}-checkpoint",
            title=challenge_title,
            prompt=f"{prompt_prefix}\n\nTừ metric list, in accuracy với đúng hai chữ số thập phân.",
            starter_code="actual = [1, 0, 1, 1]\npredicted = [1, 0, 0, 1]\n# TODO: in accuracy\n",
            expected_output="0.75",
        )
    return exercise_factory(
        key=f"{key}-checkpoint",
        slug=f"{slug}-checkpoint",
        title=challenge_title,
        prompt=f"{prompt_prefix}\n\nDùng json standard library để đọc payload và in status.",
        starter_code=(
            "import json\npayload = '{\"status\": \"ready\", \"version\": 1}'\n"
            "# TODO: parse payload và in status\n"
        ),
        expected_output="ready",
    )


def build_master_curriculum(
    lesson_factory: Callable[..., dict[str, Any]],
    exercise_factory: Callable[..., dict[str, Any]],
) -> tuple[dict[str, Any], ...]:
    """Return 130 extensions, bringing the bundled path to 180 lessons."""
    entries: list[dict[str, Any]] = []
    global_order = 51

    for track, key_prefix, first_number, label, topics in MASTER_TRACKS:
        toolchain, engineering_criterion, default_lab = TRACK_CONTEXT[track]
        for offset, item in enumerate(topics):
            sequence = first_number + offset
            key = f"{key_prefix}-{sequence:02d}-{item.slug}"
            slug = f"{key_prefix}-{item.slug}"
            lab = item.lab or default_lab
            entries.append(
                lesson_factory(
                    key=key,
                    track=track,
                    level=item.level,
                    order=global_order,
                    minutes=item.minutes,
                    title=f"{label} {sequence:02d} · {item.title}",
                    summary=item.summary,
                    objective=(
                        f"Nắm vững {item.title.lower()} và đưa nó vào workflow "
                        "của một Python/ML Engineer."
                    ),
                    concepts=(
                        item.summary,
                        f"Công cụ hoặc bối cảnh thực hành: {toolchain}.",
                        f"Tiêu chí kỹ thuật: {engineering_criterion}.",
                        f"Lab mở rộng sau checkpoint: {lab}",
                    ),
                    example=(
                        f"# Mục tiêu của bài: {item.title}\n"
                        f"workflow_step = {item.slug!r}\n"
                        "print(f\"Study: {workflow_step}\")"
                    ),
                    pitfalls=(
                        "Chỉ ghi nhớ API mà không kiểm tra giả định dữ liệu, metric hoặc ràng buộc hệ thống.",
                        "Nhảy thẳng vào thư viện lớn trước khi giải thích input, output và failure mode.",
                        "Xem checkpoint OCR là thay thế cho notebook lab, test và dự án repository.",
                    ),
                    takeaway=(
                        f"{item.title} là một mảnh của năng lực ML Engineering; hãy hoàn thành "
                        "checkpoint, sau đó thực hiện lab mở rộng và lưu evidence vào portfolio."
                    ),
                    exercise=_checkpoint(
                        exercise_factory,
                        key=key,
                        slug=slug,
                        title=item.title,
                        position=global_order,
                    ),
                )
            )
            global_order += 1

    return tuple(entries)
