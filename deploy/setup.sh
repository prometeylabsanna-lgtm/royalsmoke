#!/usr/bin/env bash
# DigitalOcean droplet bootstrap (run as root once).
set -euo pipefail

APP_USER="${APP_USER:-royalsmoke}"
APP_DIR="${APP_DIR:-/var/www/royalsmoke}"
REPO_URL="${REPO_URL:-}"

apt-get update
apt-get install -y python3 python3-venv python3-pip nginx postgresql postgresql-contrib certbot python3-certbot-nginx git

id -u "$APP_USER" >/dev/null 2>&1 || useradd --system --create-home --shell /bin/bash "$APP_USER"
mkdir -p "$APP_DIR"
chown -R "$APP_USER:$APP_USER" "$APP_DIR"

if [[ -n "$REPO_URL" && ! -d "$APP_DIR/.git" ]]; then
  sudo -u "$APP_USER" git clone "$REPO_URL" "$APP_DIR"
fi

sudo -u "$APP_USER" bash -lc "
  cd '$APP_DIR'
  python3 -m venv .venv
  .venv/bin/pip install -U pip
  .venv/bin/pip install -r requirements.txt
"

echo "Next steps:"
echo "1. Copy .env.example to /etc/royalsmoke.env and fill secrets (chmod 600)"
echo "2. Create PostgreSQL DB/user matching DATABASE_URL"
echo "3. sudo -u $APP_USER $APP_DIR/.venv/bin/python manage.py migrate"
echo "4. sudo -u $APP_USER $APP_DIR/.venv/bin/python manage.py collectstatic --noinput"
echo "5. Install deploy/gunicorn.service -> /etc/systemd/system/ && systemctl enable --now gunicorn"
echo "6. Install deploy/nginx.conf -> /etc/nginx/sites-available/royalsmoke && enable + certbot"
