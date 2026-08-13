# Python Learning Platform

Nền tảng học Python gồm Django (UI, Auth, Admin và database) và FastAPI
(nhận ảnh code, OCR Tesseract, thực thi code có giới hạn và chấm kết quả).
Người học đăng nhập, mở bài tập, nộp ảnh code Python và nhận kết quả
"passed", "failed" hoặc "error".

~~~mermaid
flowchart LR
    U["Người học / trình duyệt"] -->|"code text hoặc ảnh code"| D["Django :8000"]
    D -->|"lưu bài nộp"| P[("PostgreSQL :5432")]
    D -->|"POST /api/v1/grade-image"| O["FastAPI OCR :8001"]
    D -->|"POST /api/v1/run-code"| O
    O -->|"kết quả chấm"| D
    O -->|"nhận dạng chữ"| T["Tesseract OCR"]
~~~

## Cấu trúc

| Đường dẫn | Mục đích |
| --- | --- |
| django_app/ | Django project config, app learning, UI, REST API, Admin/Auth và migration. |
| ocr_service/ | FastAPI microservice nhận ảnh, OCR và sandbox chấm code. |
| docker-compose.yml | Chạy PostgreSQL, Django và FastAPI cùng lúc. |
| .env.example | Cấu hình mẫu cho Docker Compose. |
| django_app/.env.example | Cấu hình mẫu khi chạy Django local. |
| ocr_service/.env.example | Cấu hình mẫu khi chạy FastAPI local. |

## Step 1 — Coding và luồng xử lý

### Django

- Lưu Lesson, Exercise, Submission trong PostgreSQL và quản lý qua /admin/.
- Chỉ người dùng đã đăng nhập mới có thể nộp ảnh bài làm.
- Trang thực hành có code sandbox trực tiếp: learner gõ/chạy Python, truyền stdin
  mô phỏng `input()`, xem stdout/lỗi rồi mới chụp ảnh nộp OCR.
- Django lưu ảnh vào media/, gọi FastAPI bằng HTTP multipart và lưu lại code
  OCR, confidence, output thực thi, lỗi và trạng thái chấm.
- Django không thực thi code người học. Endpoint Django
  `POST /api/v1/sandbox/run/` chỉ xác thực session, validate JSON rồi gọi FastAPI
  `POST /api/v1/run-code` bằng API nội bộ chuyên biệt.
- Lỗi file, lỗi mạng, timeout hoặc JSON response không hợp lệ được bắt và lưu
  thành trạng thái error; stack trace nội bộ không hiển thị cho người học.
- Lúc khởi động container, Django tự chạy migration và seed_learning_data, tạo
  nội dung bài học mẫu theo cách idempotent.

### Curriculum Master Python & ML Engineering

- 180 bài học và 180 checkpoint OCR/code sandbox, chia thành 17 track: Python nền tảng và
  chuyên sâu, Software Engineering, toán tuyến tính/giải tích, xác suất/thống
  kê, data, AI có trách nhiệm, ML, MLOps, DL/PyTorch, CV, NLP, GenAI/RAG/agent,
  RL, Django, FastAPI và 6 capstone portfolio.
- Trang bài học có "Bản đồ tư duy" theo track: mô hình bản chất, pipeline xử lý,
  trường hợp biên, lỗi hay gặp và vòng thực hành để học theo cơ chế thay vì học
  thuộc lý thuyết.
- Đây là lõi nghề nghiệp rộng, không phải lời hứa sai rằng một catalog hữu hạn
  có thể chứa “toàn bộ AI”. Mỗi lesson có mục tiêu, khái niệm, lỗi thường gặp,
  checkpoint OCR và một lab notebook/repository/systems-design tiếp theo để
  biến kiến thức thành năng lực ML Engineering.
- Checkpoint OCR chỉ dùng Python standard library để chạy an toàn. Các lab sâu
  hơn chỉ dẫn thực hành NumPy, pandas, scikit-learn, PyTorch, Docker, Django và
  cloud workflow trong môi trường phụ thuộc được kiểm soát; không ép sandbox
  OCR cài hoặc chạy framework nặng.
- Trang chủ dùng track có thể thu gọn và tìm kiếm không phân biệt dấu (ví dụ
  `dao ham` tìm được “Đạo hàm”), nên 180 bài vẫn dễ duyệt trên desktop/mobile.
- Khởi động bình thường chỉ tạo các bài còn thiếu và giữ nguyên chỉnh sửa trong
  Django Admin. Chỉ khi muốn khôi phục nội dung mẫu đã chỉnh sửa mới chạy:

~~~powershell
docker compose --env-file .env exec django python manage.py seed_learning_data --refresh
~~~

Các lệnh seed hữu ích:

~~~powershell
# Xem trước việc tạo 12 bài toán AI, không ghi PostgreSQL.
docker compose --env-file .env exec django python manage.py seed_learning_data --track math --dry-run

# Seed một track còn thiếu (không ghi đè bài đã chỉnh trong Admin).
docker compose --env-file .env exec django python manage.py seed_learning_data --track genai
~~~

### Giao diện và Three.js

- Trang chủ có animation CSS nhẹ (reveal, terminal float, floating chips và
  card hover) cùng một scene Three.js trang trí phía sau terminal code.
- Three.js được import theo phiên bản đã pin `0.160.1` và chỉ tải ở trang chủ;
  không cần cài thêm `pip` hay `npm` để chạy giao diện.
- Scene tự dừng khi hero ra khỏi màn hình/tab bị ẩn và không khởi tạo trên
  mobile, chế độ Save-Data, WebGL2 không khả dụng hoặc
  `prefers-reduced-motion: reduce`. Nội dung Django vẫn hiển thị bình thường
  trong mọi trường hợp fallback.

### FastAPI, OCR và grading

- GET /health: health check.
- POST /api/v1/grade-image: nhận image và expected_output bắt buộc; test_input,
  timeout_seconds là tuỳ chọn.
- POST /api/v1/run-code: nhận JSON `{code, stdin, timeout_seconds}` để chạy code
  text trong cùng sandbox, không qua OCR. Django dùng endpoint này cho editor
  thực hành trên trang bài tập.
- Ảnh được kiểm tra MIME type, dung lượng, decode và giới hạn pixel trước khi
  OCR. Các lỗi đầu vào/trạng thái Tesseract đều trả JSON an toàn.

**Logic OCR:** OpenCV chuyển ảnh sang grayscale, phóng 2× để nhận tốt dấu
:, _, ngoặc; tăng tương phản cục bộ bằng CLAHE, khử nhiễu và adaptive threshold.
Tesseract chạy với --psm 6 (một block code) và preserve_interword_spaces=1.
Việc giữ khoảng trắng rất quan trọng vì Python phụ thuộc indentation. Service
chỉ chuẩn hoá line ending/khoảng trắng không ngắt được; không tự sửa syntax để
tránh biến đổi code của học viên.

Code OCR chạy trong subprocess Python với -I -B, working directory tạm,
environment tối giản, timeout và giới hạn source/input/output. Linux áp dụng
thêm RLIMIT; Docker chạy user không đặc quyền, read-only filesystem, /tmp
tmpfs, no-new-privileges, capability drop và quota CPU/RAM/process. Đây là
defense-in-depth, không phải security boundary tuyệt đối; production nên dùng
VM/container cách ly và quota ở hạ tầng.

## Step 2 — Self-testing

Sau khi cài dependencies, chạy test từng service:

~~~powershell
# FastAPI OCR (terminal 1)
Set-Location ocr_service
pytest -q

# Django (terminal 2). Test tự dùng SQLite in-memory, không sửa PostgreSQL.
Set-Location django_app
python manage.py test
python manage.py check
~~~

Test FastAPI mock Tesseract/sandbox để kiểm tra health endpoint, contract
passed/failed và upload quá lớn. Test Django không cần service OCR thật khi dùng
manage.py test.

Smoke test toàn stack Docker:

~~~powershell
docker compose --env-file .env config --quiet
docker compose --env-file .env up --build -d
docker compose ps
Invoke-WebRequest http://localhost:8001/health | Select-Object -Expand Content
Invoke-WebRequest http://localhost:8000/ | Select-Object -Expand StatusCode
docker compose logs --tail=100 django ocr-service db
~~~

Kết quả kỳ vọng: db là healthy, Django/FastAPI là running; endpoint OCR trả JSON
có "status":"ok" và Django trả HTTP 200.

Kiểm tra grading bằng ảnh code thật sample-code.png, chứa
print("Hello, Python!"):

~~~powershell
curl.exe -X POST http://localhost:8001/api/v1/grade-image -F "image=@sample-code.png;type=image/png" -F "expected_output=Hello, Python!" -F "timeout_seconds=3"
~~~

Kết quả mong đợi là "status":"passed" với output Hello, Python!.

Kiểm tra code sandbox text:

~~~powershell
$payload = @{ code = "print(123)"; stdin = ""; timeout_seconds = 2 } | ConvertTo-Json -Compress
Invoke-RestMethod -Uri http://localhost:8001/api/v1/run-code -Method Post -ContentType "application/json" -Body $payload
~~~

Kết quả mong đợi là `"status":"passed"` và `"execution_output":"123\n"`.

## Step 3 — Chạy bằng Docker (khuyến nghị)

### Điều kiện

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) đã chạy.
- PowerShell. Không cần cài PostgreSQL hoặc Tesseract trên Windows: image OCR
  tự cài Tesseract và English language data trên Linux.

### Khởi động

Tại thư mục gốc:

~~~powershell
Copy-Item .env.example .env
# Sửa POSTGRES_PASSWORD và DJANGO_SECRET_KEY trong .env trước khi dùng ngoài local.
docker compose up --build -d
docker compose ps
~~~

Mở:

- Django: <http://localhost:8000/>
- Django Admin: <http://localhost:8000/admin/>
- FastAPI Swagger: <http://localhost:8001/docs>
- FastAPI health: <http://localhost:8001/health>

Người học mới có thể chọn **Create account** ở thanh điều hướng Django (hoặc mở
<http://localhost:8000/accounts/register/>), sau đó đăng nhập và nộp ảnh code.

Tạo tài khoản quản trị:

~~~powershell
docker compose exec django python manage.py createsuperuser
~~~

Xem log và dừng stack:

~~~powershell
docker compose logs -f django ocr-service db
docker compose down
~~~

PostgreSQL, media và static files nằm trên named volumes nên không mất sau
docker compose down. Chỉ khi muốn xoá toàn bộ database và ảnh local:

~~~powershell
docker compose down -v
~~~

Lệnh này có tính phá huỷ dữ liệu. Lần up mới sẽ tự tạo database python_learning,
bảng Django và dữ liệu bài học mẫu.

## Chạy local trên Windows

Docker là lựa chọn dễ nhất. Phần này dùng khi cần debug từng service trực tiếp
trên Windows; PostgreSQL vẫn chạy qua Docker.

### 1. Cài Tesseract OCR

1. Tải bản 64-bit từ [Tesseract at UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki).
2. Cài ở thư mục mới, thường là C:\Program Files\Tesseract-OCR, và chọn
   English language data (eng).
3. Kiểm tra trong PowerShell mới:

   ~~~powershell
   & "C:\Program Files\Tesseract-OCR\tesseract.exe" --version
   & "C:\Program Files\Tesseract-OCR\tesseract.exe" --list-langs
   ~~~

4. Đặt biến cho terminal chạy FastAPI:

   ~~~powershell
   $env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"
   $env:OCR_LANGUAGE = "eng"
   ~~~

TESSERACT_CMD có thể bỏ trống nếu tesseract.exe đã có trong PATH. FastAPI cũng
đọc ocr_service/.env (process environment có ưu tiên cao hơn), nên có thể copy
.env.example rồi đặt giá trị ở đó.

### 2. Khởi động PostgreSQL

~~~powershell
Set-Location <duong-dan-toi-python_ai_mini_project>
Copy-Item .env.example .env
docker compose up -d db
~~~

### 3. Khởi động FastAPI

~~~powershell
Set-Location ocr_service
Copy-Item .env.example .env
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

$env:TESSERACT_CMD = "C:\Program Files\Tesseract-OCR\tesseract.exe"
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
~~~

Nếu PowerShell chặn activation script:

~~~powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
~~~

### 4. Khởi động Django

Trong terminal khác:

~~~powershell
Set-Location django_app
Copy-Item .env.example .env
~~~

Sửa django_app/.env cho local service/database:

~~~dotenv
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
FASTAPI_OCR_URL=http://127.0.0.1:8001/api/v1/grade-image
FASTAPI_RUN_CODE_URL=http://127.0.0.1:8001/api/v1/run-code
DJANGO_DEBUG=True
~~~

Sau đó:

~~~powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_learning_data
python manage.py collectstatic --noinput
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
~~~

## Biến môi trường chính

| Biến | Giá trị Docker mặc định | Ý nghĩa |
| --- | --- | --- |
| POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD | python_learning, python_learning, mật khẩu mẫu | Khởi tạo/kết nối PostgreSQL. |
| POSTGRES_HOST, POSTGRES_PORT | db, 5432 | Kết nối database của Django. |
| FASTAPI_OCR_URL | http://ocr-service:8001/api/v1/grade-image | Django gọi OCR grader. |
| FASTAPI_RUN_CODE_URL | http://ocr-service:8001/api/v1/run-code | Django gọi code sandbox text. |
| TESSERACT_CMD | rỗng | Đường dẫn tesseract.exe khi chạy Windows local. |
| OCR_LANGUAGE | eng | Language data của Tesseract. |
| CODE_TIMEOUT_SECONDS / MAX_CODE_TIMEOUT_SECONDS | 3 / 10 | Timeout code; exercise Django cũng tối đa 10 giây. |
| MAX_UPLOAD_BYTES / MAX_IMAGE_PIXELS | 5 MiB / 16M | Chặn ảnh quá lớn trước khi OCR. |
| CODE_MEMORY_LIMIT_MB | 128 | Giới hạn memory subprocess trên Unix. |

## Mini project CLI cũ (tuỳ chọn)

Các file `app.py`, `lessons.py`, `quiz_data.py`, `exercises.py` và
`test_exercises.py` là mini project học Python trên CMD ban đầu; chúng độc lập
với nền tảng Django/FastAPI. Có thể tiếp tục dùng để học cú pháp cơ bản:

~~~powershell
python app.py
python test_exercises.py
~~~

## Lưu ý production

- Không commit .env, PostgreSQL password hoặc DJANGO_SECRET_KEY.
- Đặt DJANGO_DEBUG=False, secret ngẫu nhiên dài, DJANGO_ALLOWED_HOSTS và
  DJANGO_CSRF_TRUSTED_ORIGINS theo HTTPS domain thật trước khi public.
- Ảnh mờ, phản sáng hoặc font nhỏ làm OCR giảm chính xác. Nên dùng ảnh thẳng,
  nền sáng/chữ tối, đủ nét và chỉ có code; API trả ocr_confidence để giao diện
  có thể cảnh báo khi độ tin cậy thấp.
