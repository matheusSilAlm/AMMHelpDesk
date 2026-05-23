# AMMHelpDesk — Production Refactor Design

**Date:** 2026-05-22  
**Strategy:** Phased refactor (Approach B) — each phase ships working, testable code  
**Goal:** Transform first-project Django app into a deployable, sellable product  

---

## Context

Single Django app (`app_helpdesk`) with hardcoded credentials, no Docker, flat structure, raw POST handling, MySQL. Target: clean architecture, PostgreSQL, Docker-ready, Tailwind UI, security hardened.

---

## Phase 1 — Project Structure + Settings

### Goal
Establish professional folder layout, split settings by environment, remove all hardcoded secrets.

### Folder Structure

```
AMMHelpDesk/
├── config/                        # renamed from AmmHelpDesk/ (project config)
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py                # shared settings (installed apps, middleware, etc.)
│   │   ├── development.py         # DEBUG=True, console email backend
│   │   └── production.py          # DEBUG=False, Postgres, security headers
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   └── helpdesk/                  # renamed from app_helpdesk
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       ├── forms.py               # NEW — Django Form classes
│       ├── urls.py                # NEW — app-level URL conf
│       ├── admin.py
│       ├── apps.py
│       ├── migrations/
│       └── templates/
│           └── helpdesk/          # namespaced templates
│               ├── login.html
│               ├── cliente.html
│               ├── forms_hd.html
│               ├── listpage.html
│               ├── pagecliente.html
│               └── faq.html
├── static/
│   ├── css/
│   ├── js/
│   └── img/
├── templates/                     # global templates
│   └── base.html                  # base layout (Phase 3)
├── requirements/
│   ├── base.txt                   # shared deps
│   ├── development.txt            # dev-only (debug toolbar, etc.)
│   └── production.txt             # prod-only (gunicorn, psycopg2, etc.)
├── .env                           # NOT in git
├── .env.example                   # placeholder values only — IN git
├── manage.py
└── docker-compose.yml             # added in Phase 2
```

### Settings Split

**base.py** contains: INSTALLED_APPS, MIDDLEWARE, TEMPLATES, STATIC_URL, AUTH config, EMAIL base config, LANGUAGE_CODE, TIME_ZONE.

**development.py** extends base:
```python
from .base import *
DEBUG = True
DATABASES = { ... sqlite or local postgres ... }
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**production.py** extends base:
```python
from .base import *
DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
DATABASES = { ... postgres from env ... }
SECURE_HSTS_SECONDS = 3600
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### Environment Variables

Use `python-decouple`. All secrets live in `.env`, never in code.

```
# .env.example
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=helpdesk
DB_USER=helpdesk_user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_PORT=587
```

### Django Forms

Replace all raw `request.POST.get()` with Form classes in `apps/helpdesk/forms.py`:

- `ClienteForm` — nomecliente, cpf_cnpj, email, phone, subject, description
- `LoginForm` — username, password  
- `SolicitacaoForm` — subject, priority  
- `RespostaForm` — response text

Each form handles validation (email format, required fields, max lengths).

### Deliverables
- [ ] Renamed folders, updated all imports
- [ ] `config/settings/` split into 3 files
- [ ] `python-decouple` installed, all secrets in `.env`
- [ ] `.env.example` committed, `.env` in `.gitignore`
- [ ] `apps/helpdesk/forms.py` with all form classes
- [ ] `apps/helpdesk/urls.py` with app-level routes
- [ ] `requirements/` split into 3 files
- [ ] `requirements.tx` renamed to `requirements/base.txt`
- [ ] All tests pass (app loads, login works, forms submit)

---

## Phase 2 — Backend Fixes + PostgreSQL + Docker

### Goal
Fix all critical bugs and security issues, migrate to PostgreSQL, containerize with Docker.

### Backend Fixes

**Security:**
- Remove `"*"` from `ALLOWED_HOSTS`
- Regenerate `SECRET_KEY` (use `django.core.management.utils.get_random_secret_key()`)
- Rotate database and email passwords (current ones are in git history — must change)
- Add `X-Frame-Options`, `X-Content-Type-Options` headers

**N+1 Query Fix** (`views.py` listpage):
```python
# Before (N+1 — hits DB once per client)
for cliente in arr_cliente:
    solicitacao = Solicitacao.objects.get(idcliente=cliente.idcliente)

# After (2 queries total)
clientes = Cliente.objects.select_related('solicitacao').filter(ativo=True)
```

**Error Handling:**
- Replace `.get()` with `.filter().first()` where object may not exist
- Wrap email send in `try/except` with logging on failure
- Add `@transaction.atomic` to views that save + send email

**Logging:**
```python
# base.py
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
        'file': {'class': 'logging.FileHandler', 'filename': 'logs/helpdesk.log'},
    },
    'loggers': {
        'apps.helpdesk': {'handlers': ['console', 'file'], 'level': 'INFO'},
    },
}
```

**Model cleanup:**
- Add `__str__` to all models
- Add `class Meta: verbose_name` for admin readability
- Add field validators (email, phone format)

**Remove:**
- Duplicate URL pattern (`/home/updatecliente/<id>/teste/`)
- `templates/server.py` (Python file in wrong location)
- Commented-out code blocks
- Redundant imports

### PostgreSQL Migration

1. Install `psycopg2-binary` (dev) and `psycopg2` (prod)
2. Update `production.py` database config to use env vars
3. Run `python manage.py dumpdata > data_backup.json` on MySQL
4. Switch database engine to `django.db.backends.postgresql`
5. Run `python manage.py migrate`
6. Run `python manage.py loaddata data_backup.json`
7. Verify data integrity

### Docker Setup

**`Dockerfile`:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements/production.txt .
RUN pip install --no-cache-dir -r production.txt
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**`docker-compose.yml`:**
```yaml
version: '3.9'
services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    env_file: .env

  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file: .env

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
```

### Deliverables
- [ ] All credentials rotated and in `.env` only
- [ ] N+1 queries fixed with `select_related`/`prefetch_related`
- [ ] All views have proper error handling
- [ ] `@transaction.atomic` on save+email views
- [ ] Logging configured, `logs/` directory in `.gitignore`
- [ ] Models have `__str__`, validators, `Meta` classes
- [ ] PostgreSQL running locally and in Docker
- [ ] Data migrated from MySQL successfully
- [ ] `docker-compose up` runs full stack
- [ ] `nginx.conf` serves static files correctly

---

## Phase 3 — Template Reorganization + Tailwind CSS

### Goal
Clean, modern UI using Django template inheritance and Tailwind CSS. Every page looks consistent and professional.

### Template Hierarchy

```
templates/
└── base.html                  # master layout

apps/helpdesk/templates/helpdesk/
├── login.html                 # extends base.html
├── listpage.html              # extends base.html
├── forms_hd.html              # extends base.html
├── cliente.html               # extends base.html
├── pagecliente.html           # extends base.html
└── faq.html                   # extends base.html
```

**`base.html` structure:**
```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  {% block head %}
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% block title %}AMM HelpDesk{% endblock %}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  {% block extra_head %}{% endblock %}
  {% endblock %}
</head>
<body class="bg-gray-50 min-h-screen">
  {% block navbar %}
    {% include 'helpdesk/partials/navbar.html' %}
  {% endblock %}

  <main class="container mx-auto px-4 py-8">
    {% block content %}{% endblock %}
  </main>

  {% block footer %}
    {% include 'helpdesk/partials/footer.html' %}
  {% endblock %}

  {% block extra_js %}{% endblock %}
</body>
</html>
```

### Partials (reusable includes)

```
apps/helpdesk/templates/helpdesk/partials/
├── navbar.html                # navigation bar
├── footer.html                # footer
├── messages.html              # Django messages (alerts/toasts)
└── pagination.html            # pagination controls
```

### Tailwind CSS Approach

Use Tailwind CDN (no build step required). For production, switch to `django-tailwind` package for purged CSS (smaller file size).

Each page gets a consistent design system:
- Color scheme: defined in `tailwind.config` block in `base.html`
- Typography: consistent heading/body sizes
- Components: buttons, cards, form inputs styled uniformly

### Remove
- `pageclienteX.html` — duplicate/unused template
- `teste.html` — test template
- Inline CSS scattered across templates
- Inconsistent Brazilian Portuguese / English mixing in CSS class names

### Deliverables
- [ ] `base.html` with Tailwind CDN
- [ ] All templates extend `base.html`
- [ ] Partials: navbar, footer, messages, pagination
- [ ] All pages visually consistent
- [ ] Mobile responsive (Tailwind responsive prefixes)
- [ ] `pageclienteX.html` and `teste.html` removed
- [ ] No inline styles remaining
- [ ] Forms use Tailwind-styled input classes

---

## Phase 4 — Polish + Security Audit

### Goal
Production-ready security, clean code, and final quality pass before any real deployment.

### Security Checklist

- [ ] `DEBUG=False` verified in production settings
- [ ] `SECRET_KEY` is 50+ random chars, never committed
- [ ] `ALLOWED_HOSTS` has only specific domains (no `*`)
- [ ] `SECURE_HSTS_SECONDS = 31536000` (1 year)
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] `X_FRAME_OPTIONS = 'DENY'`
- [ ] File write operations use `with open()` context manager
- [ ] File path construction uses `os.path.join` with validation (no traversal)
- [ ] All user-facing strings pass through Django's auto-escaping (no `|safe` on user input)
- [ ] Rate limiting on login endpoint (use `django-axes` or `django-ratelimit`)
- [ ] Admin URL changed from `/admin/` to something non-obvious

### Code Quality Pass

- [ ] Remove all `# TODO` and commented-out code
- [ ] Consolidate duplicate imports in `views.py`
- [ ] Rename `requirements.tx` → already fixed in Phase 1
- [ ] `isort` + `black` formatting applied
- [ ] `flake8` passes with no errors
- [ ] All models have `__str__` — already done in Phase 2
- [ ] Views use Django messages framework for user feedback (not hardcoded alerts)

### Input Validation

Ensure all Form classes added in Phase 1 include:
- Email field uses `EmailField` (auto-validates format)
- CPF/CNPJ field has custom validator
- All text fields have `max_length` matching model
- Phone field validates Brazilian phone format

### Transaction Safety

Views that save to DB AND send email:
```python
from django.db import transaction

@transaction.atomic
def update_cliente(request, idcliente):
    # All DB saves happen here
    # Email send AFTER the transaction commits:
    transaction.on_commit(lambda: send_response_email(cliente))
```

### Logging Final Check
- [ ] Production log level set to `WARNING` (not `DEBUG`)
- [ ] `logs/` directory exists in `.gitignore`
- [ ] No sensitive data (passwords, tokens) logged anywhere

### Optional Enhancements (post-sellable baseline)
These are nice-to-have, not required for a sellable product:
- Django REST Framework API layer
- Frontend SPA (React/Vue) consuming API
- Celery + Redis for async email sending
- S3 for static/media file storage in production
- Sentry for error monitoring

### Deliverables
- [ ] All security checklist items resolved
- [ ] `black` + `isort` + `flake8` pass
- [ ] Rate limiting on login
- [ ] Transaction-safe email sends
- [ ] Final `docker-compose up --build` runs clean
- [ ] App accessible at `localhost:80` via Nginx

---

## Implementation Order Summary

| Phase | Focus | Est. Complexity |
|-------|-------|-----------------|
| 1 | Structure + Settings + Forms | Medium |
| 2 | Backend Fixes + Postgres + Docker | High |
| 3 | Templates + Tailwind UI | Medium |
| 4 | Security Audit + Polish | Low-Medium |

Each phase ends with a working, testable app. Do not start Phase N+1 until Phase N is verified working.

---

## Key Decisions

- **PostgreSQL** over MySQL — industry standard, better Docker/cloud support
- **python-decouple** over django-environ — simpler API, `.ini` fallback
- **Tailwind CDN** over django-tailwind — zero build step for initial refactor; migrate to purge later
- **Gunicorn + Nginx** over Django dev server — required for production
- **Split settings** over single settings + env flag — explicit is better than implicit
