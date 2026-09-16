#!/usr/bin/env bash
set -euo pipefail

if command -v docker >/dev/null 2>&1; then
  docker compose version >/dev/null
  echo "==> Docker already installed"
  exit 0
fi

curl -fsSL https://get.docker.com | sh
systemctl enable --now docker
docker compose version
