# Dong goi source de chay tren may khac

Tai lieu nay uu tien cach chay bang Docker Compose. May moi khong can cai Python,
PostgreSQL hay Tesseract rieng; cac thanh phan do duoc dong trong container.

## 1. Tren may hien tai: tao goi source sach

Dung PowerShell tai thu muc goc project:

```powershell
$src = (Resolve-Path .).Path
$stamp = Get-Date -Format "yyyyMMdd-HHmmss"
$stage = Join-Path ([System.IO.Path]::GetTempPath()) "python-learning-package-$stamp"
$zip = Join-Path (Split-Path $src -Parent) "python-learning-platform-source-$stamp.zip"

New-Item -ItemType Directory -Path $stage | Out-Null

robocopy $src $stage /E `
  /XD .venv __pycache__ .pytest_cache django_app\staticfiles django_app\media `
  /XF .env *.pyc *.pyo *.sqlite3

Compress-Archive -Path (Join-Path $stage "*") -DestinationPath $zip -Force

Write-Host "Created: $zip"
```

Goi zip nay se bo qua:

- `.env`: khong mang secret/local password sang may khac.
- `.venv`, `__pycache__`, `.pytest_cache`: file sinh ra luc chay.
- `django_app/staticfiles`: Docker se tu `collectstatic`.
- `django_app/media`: anh upload local, chi copy rieng neu can.
- `*.sqlite3`: project chay PostgreSQL bang Docker.

## 2. Tren may moi: cai cong cu

Can cai:

- Docker Desktop.
- Git hoac chi can giai nen file zip.
- PowerShell/Terminal.

Khong can cai Tesseract tren Windows neu chay Docker, vi image FastAPI da cai:
`tesseract-ocr` va `tesseract-ocr-eng`.

## 3. Tren may moi: chay project

Giai nen file zip, mo terminal tai thu muc project, roi tao file `.env`:

```powershell
Copy-Item .env.example .env
```

Neu chay local mac dinh, co the giu nguyen cau hinh. Neu port 8000/8001/5432 dang bi
may khac dung, sua trong `.env`:

```env
DJANGO_PORT=8000
FASTAPI_PORT=8001
POSTGRES_EXPOSE_PORT=5432
```

Build va chay toan bo he thong:

```powershell
docker compose --env-file .env up -d --build
```

Mo ung dung:

- Django UI: http://localhost:8000
- FastAPI health qua gateway: http://localhost:8001/health

Xem log neu can:

```powershell
docker compose --env-file .env logs -f django
docker compose --env-file .env logs -f ocr-service
docker compose --env-file .env logs -f gateway
```

## 4. Tao tai khoan admin tren may moi

Sau khi container dang chay:

```powershell
docker compose --env-file .env exec django python manage.py createsuperuser
```

Trang admin:

```text
http://localhost:8000/admin/
```

## 5. Kiem tra nhanh sau khi chay

```powershell
docker compose --env-file .env ps
docker compose --env-file .env exec django python manage.py check
docker compose --env-file .env exec django python manage.py test learning
docker compose --env-file .env exec ocr-service pytest
```

Khi Django khoi dong, container se tu chay:

```text
python manage.py migrate --noinput
python manage.py seed_learning_data
python manage.py collectstatic --noinput
gunicorn config.wsgi:application
```

Nghia la PostgreSQL se duoc tao bang Docker volume, migrations tu chay, va noi dung
180 bai hoc duoc seed lai neu database moi.

## 6. Muon mang theo database hien tai

Neu muon may moi co ca user/submission/du lieu hien tai, dump PostgreSQL tu may cu:

```powershell
$db = docker compose --env-file .env ps -q db
docker compose --env-file .env exec db pg_dump -U python_learning -d python_learning -Fc -f /tmp/python_learning.dump
docker cp "${db}:/tmp/python_learning.dump" .\python_learning.dump
```

Restore tren may moi sau khi `docker compose up -d --build`:

```powershell
$db = docker compose --env-file .env ps -q db
docker cp .\python_learning.dump "${db}:/tmp/python_learning.dump"
docker compose --env-file .env exec db pg_restore -U python_learning -d python_learning --clean --if-exists /tmp/python_learning.dump
docker compose --env-file .env restart django
```

Neu chi can source va bai hoc mau, bo qua buoc database nay.

## 7. Lenh dung / chay lai

Dung container:

```powershell
docker compose --env-file .env down
```

Dung va xoa database/media/static Docker volumes:

```powershell
docker compose --env-file .env down -v
```

Can than voi `down -v`: lenh nay xoa database PostgreSQL local cua project tren may do.
