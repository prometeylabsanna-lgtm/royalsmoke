# Royal Smoke

Інтернет-магазин сигар / сигарет / аксесуарів.

## Стек

- Django 5.2 + PostgreSQL
- HTML / CSS / Vanilla JS + HTMX
- Unfold admin + SiteBlock CMS
- DRF API `/api/v1/` (під iOS / Telegram)
- i18n: UK / EN / ZH-Hans (modeltranslation)

## Швидкий старт

```bash
cd /Users/olegbonislavskyi/Sites/RoyalSmoke
source .venv/bin/activate
createdb royalsmoke   # якщо ще немає
python3 manage.py migrate
python3 manage.py seed_demo
python3 manage.py createsuperuser --email you@example.com
python3 manage.py runserver 127.0.0.1:8001
```

- Сайт: http://127.0.0.1:8001/
- Адмінка: http://127.0.0.1:8001/rs-admin/
- Демо-адмін (якщо створювали seed): `admin@royalsmoke.ua` / `admin123`

## Apps

`accounts` `catalog` `cart` `orders` `booking` `calculator` `leads` `core` `pages` `api`
