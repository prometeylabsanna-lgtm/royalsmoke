# DigitalOcean Droplet — HTTP-first

Один стек: Docker Compose + nginx + gunicorn + PostgreSQL.
`git push` не деплоїть. SSL — окремий крок після DNS (`deploy/nginx/docker.prod.conf`).

Локальна розробка лишається `venv` + `runserver` (див. кореневий README).

## Передумови

- Ubuntu 24.04 Droplet, shop/CMS ≥ 2 GB RAM (1 GB лише з swap 2G)
- Шлях коду: `/var/www/royalsmoke` (не вкладений `royalsmoke/royalsmoke`)
- Firewall: 22, 80 (443 одразу, для SSL пізніше)
- Репо запушене в remote Git

## 1. SSH (Mac)

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_royalsmoke_do -N "" -C "royalsmoke-do"
chmod 600 ~/.ssh/id_royalsmoke_do
cat ~/.ssh/id_royalsmoke_do.pub
```

Публічний ключ — у DigitalOcean SSH Keys до створення Droplet.

Після появи IPv4 дописати в `~/.ssh/config`:

```sshconfig
Host royalsmoke
  HostName 203.0.113.10
  User root
  IdentityFile ~/.ssh/id_royalsmoke_do
  IdentitiesOnly yes
  ServerAliveInterval 30
  ServerAliveCountMax 3
```

Перевірка: `ssh royalsmoke`.

Swap на 1 GB:

```bash
fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile && swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

## 2. Перший HTTP-деплой

```bash
mkdir -p /var/www
git clone <REPO_URL> /var/www/royalsmoke
cd /var/www/royalsmoke
bash deploy/docker/install-docker.sh
cp .env.docker.example .env
nano .env
```

У `.env` обов'язково:

- реальний `SECRET_KEY` і `POSTGRES_PASSWORD` (і той самий пароль у `DATABASE_URL`)
- `ALLOWED_HOSTS=<IPv4>,127.0.0.1,localhost,web` — **не** літерал `DROPLET_IP`
- `CSRF_TRUSTED_ORIGINS=http://<IPv4>`
- `SESSION_COOKIE_SECURE=False`, `CSRF_COOKIE_SECURE=False`, `SECURE_SSL_REDIRECT=False`

```bash
bash deploy/docker/deploy.sh
curl -sI -H "Host: <IPv4>" http://127.0.0.1/healthz/
curl -sI -H "Host: <IPv4>" http://127.0.0.1/health/
```

Після `nano .env` завжди:

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --force-recreate web
```

## 3. Дані і суперюзер

Спочатку healthz OK. Якщо переносите дамп: flush + loaddata + media, **потім** createsuperuser.

```bash
docker compose -f docker-compose.yml -f docker-compose.prod.yml exec web \
  python3 manage.py createsuperuser
```

Не запускати `seed_demo` на проді.

## 4. Оновлення

```bash
cd /var/www/royalsmoke
git pull origin main
bash deploy/docker/deploy.sh
```

`docker compose up -d` без `--build` не підхоплює новий код.

## 5. Локальний compose (опційно)

Не займати хостові 80 і 5432:

```bash
cp .env.docker.example .env.docker.local
# виставити SECRET_KEY, POSTGRES_PASSWORD, ALLOWED_HOSTS=127.0.0.1,localhost,web
ENV_FILE=.env.docker.local HTTP_PORT=8080 docker compose -f docker-compose.yml up --build
curl -sf http://127.0.0.1:8080/healthz/
```

## Після DNS

Certbot на хості, `docker.prod.conf`, cookies `True` — окремий захід (`django-docker-ssl`).
На HTTP-тесті не вмикати `SESSION_COOKIE_SECURE=True` і не патчити compose на сервері.
