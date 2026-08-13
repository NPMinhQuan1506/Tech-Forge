#!/bin/sh
set -eu

# Named volumes are mounted after the image is built and are usually owned by
# root on first use.  Prepare only the writable upload/static paths, then drop
# privileges before Django, migrations, or Gunicorn run.
if [ "$(id -u)" = "0" ]; then
    mkdir -p /app/django_app/media /app/django_app/staticfiles
    chown -R app:app /app/django_app/media /app/django_app/staticfiles
    exec gosu app "$@"
fi

exec "$@"
