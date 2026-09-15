# DigitalOcean Droplet deploy

## Prerequisites
- Ubuntu 22.04/24.04 droplet
- Domain A-record pointing to droplet IP
- Remote Git repo pushed

## Quick path
1. SSH as root, upload/clone repo, run `bash deploy/setup.sh` (optionally `REPO_URL=...`).
2. Create `/etc/royalsmoke.env` from `.env.example` (`DEBUG=False`, real `SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS=https://your.domain`, SMTP, LiqPay, NP, Telegram).
3. Create PostgreSQL DB and user; set `DATABASE_URL`.
4. `migrate`, `collectstatic`, `createsuperuser`.
5. Install `deploy/gunicorn.service` and `deploy/nginx.conf` (replace `example.com`).
6. `certbot --nginx -d your.domain`.
7. Deploy updates:

```bash
cd /var/www/royalsmoke
sudo -u royalsmoke git pull
sudo -u royalsmoke .venv/bin/pip install -r requirements.txt
sudo -u royalsmoke .venv/bin/python manage.py migrate
sudo -u royalsmoke .venv/bin/python manage.py collectstatic --noinput
systemctl restart gunicorn
```

Health check: `https://your.domain/health/`
