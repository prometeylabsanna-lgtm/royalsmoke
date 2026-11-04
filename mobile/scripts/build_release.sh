#!/usr/bin/env bash
# Локальна release-збірка: analyze, тести, Android App Bundle, iOS без підпису.
# API_BASE_URL з оточення, якщо задано, перекриває дефолт застосунку.
set -euo pipefail

cd "$(dirname "$0")/.."

define_args=()
if [[ -n "${API_BASE_URL:-}" ]]; then
  define_args+=(--dart-define="API_BASE_URL=${API_BASE_URL}")
fi

flutter analyze
flutter test

if ((${#define_args[@]})); then
  flutter build appbundle --release "${define_args[@]}"
  flutter build ios --release --no-codesign "${define_args[@]}"
else
  flutter build appbundle --release
  flutter build ios --release --no-codesign
fi
