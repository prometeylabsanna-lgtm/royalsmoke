#!/usr/bin/env bash
set -euo pipefail

echo "==> Waiting for PostgreSQL..."
python3 <<'PY'
import os
import sys
import time

import psycopg

url = os.environ.get("DATABASE_URL", "")
if not url:
    sys.exit(0)
for _ in range(30):
    try:
        with psycopg.connect(url) as conn:
            conn.execute("SELECT 1")
        print("==> DB ready")
        break
    except Exception:
        time.sleep(2)
else:
    print("FATAL: DB not ready")
    sys.exit(1)
PY

echo "==> Django check + migrate + seed + collectstatic"
python3 manage.py check --deploy
python3 manage.py migrate --noinput
python3 manage.py seed_demo
python3 manage.py fill_i18n_content
python3 manage.py collectstatic --noinput

_static_count=$(find "${STATIC_ROOT:-/app/staticfiles}" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "==> static files: ${_static_count}"
if [ "${_static_count:-0}" -lt 10 ]; then
  echo "WARN: staticfiles count low — check STATIC_ROOT and collectstatic"
fi

exec "$@"
