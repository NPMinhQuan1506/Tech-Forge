# OCR grading microservice

This independent FastAPI service is called by Django after a learner uploads a
photo or screenshot of Python code. It has two endpoints:

- `GET /health`
- `POST /api/v1/grade-image` (`multipart/form-data`)

## API contract

`grade-image` accepts the following multipart fields:

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `image` | file | yes | Photograph or screenshot of Python code |
| `expected_output` | string | yes | Expected standard output |
| `test_input` | string | no | Input passed to the submitted code via stdin |
| `timeout_seconds` | integer | no | Requested limit, from 1 to `MAX_CODE_TIMEOUT_SECONDS` |

The primary response fields are:

```json
{
  "status": "passed",
  "extracted_code": "print('Hello')",
  "ocr_confidence": 94.2,
  "execution_output": "Hello\\n",
  "error_message": null
}
```

`status` is `passed`, `failed`, or `error`. The response also supplies
`exit_code`, `timed_out`, and `output_truncated` as optional diagnostics.

## OCR logic

The service decodes the image with OpenCV, rejects unusually large dimensions,
converts it to grayscale, scales it 2x, improves local contrast with CLAHE,
removes light noise, and applies adaptive thresholding. The result is supplied
to Tesseract in `--psm 6` (a uniform code block) mode with
`preserve_interword_spaces=1`; preserving whitespace matters for Python
indentation. It returns Tesseract's mean word confidence alongside the raw
extracted code. The service does not auto-correct suspected syntax because that
can silently change a learner's intended program.

## Local setup (Windows)

1. Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).
   During setup, include the English language data. Its typical executable path
   is `C:\Program Files\Tesseract-OCR\tesseract.exe`.
2. From this `ocr_service` directory, create and activate a virtual
   environment:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. Copy `.env.example` to `.env` and either add Tesseract to `PATH` or set
   `TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe`. Environment
   variables can also be configured in the shell before starting the server;
   process-level variables take priority over values in `.env`.
4. Start the service:

   ```powershell
   uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
   ```

5. Open `http://127.0.0.1:8001/docs` or run the tests:

   ```powershell
   pytest -q
   ```

## Safety model

Each submission runs with an isolated Python invocation (`-I -B`), an empty
working directory, a scrubbed environment, a wall-clock timeout, source/input
and captured-output caps, and Unix `RLIMIT` CPU, address-space, file-size,
file-descriptor, and process limits. On Windows the portable implementation
enforces the wall-clock, working-directory, environment, and size limits, but
cannot apply Unix `RLIMIT`s. This is intentionally a **best-effort** sandbox,
not a substitute for isolation: deploy it as a non-root container/VM with no
network, a read-only filesystem, and platform resource quotas.
