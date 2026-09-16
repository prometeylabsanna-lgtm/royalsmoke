#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.prod.yml)

free_host_ports() {
  systemctl stop nginx 2>/dev/null || true
  systemctl disable nginx 2>/dev/null || true
  systemctl stop gunicorn gunicorn.service royalsmoke 2>/dev/null || true
  systemctl disable gunicorn gunicorn.service royalsmoke 2>/dev/null || true
}

if [[ ! -f .env ]]; then
  echo "FATAL: .env missing. Copy .env.docker.example → .env and set secrets."
  exit 1
fi

if grep -qE 'ALLOWED_HOSTS=.*DROPLET_IP' .env; then
  echo "FATAL: .env still has literal DROPLET_IP — replace with real IPv4"
  exit 1
fi
if grep -qE 'SECRET_KEY=(change-me-in-production|generate-a-long-random-string|insecure-dev-key)\s*$' .env; then
  echo "FATAL: set a real SECRET_KEY in .env"
  exit 1
fi

free_host_ports

"${COMPOSE[@]}" build web
"${COMPOSE[@]}" up -d --force-recreate

echo "==> waiting for healthz..."
ok=0
for _ in $(seq 1 40); do
  if curl -sf http://127.0.0.1/healthz/ >/dev/null; then
    ok=1
    break
  fi
  sleep 3
done

"${COMPOSE[@]}" ps

if [[ "$ok" -ne 1 ]]; then
  echo "FATAL: /healthz/ not 200"
  "${COMPOSE[@]}" logs --tail=80 web nginx
  exit 1
fi

echo "==> HTTP healthz OK"
for svc in db web nginx; do
  if ! "${COMPOSE[@]}" ps --format '{{.Name}} {{.Status}}' | grep -q "$svc"; then
    echo "WARN: service $svc not listed — check compose ps"
  fi
done
