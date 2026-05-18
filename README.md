# FastAPI Template

Reusable FastAPI project layout: versioned API, layered services/repos, demo auth, SQLAlchemy.

**Full guide:** [DOCUMENTATION.md](DOCUMENTATION.md) — architecture, auth, database, Docker, how to extend.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python scripts/seed.py
uvicorn app.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Docker (API + MySQL)

```bash
make up        # build, migrate, seed, start
make logs      # follow API logs
make down      # stop containers
```

API: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

MySQL on `localhost:3306` — user `fastapi` / password `fastapi` / database `fastapi_db`.

## Makefile

```bash
make help      # all commands
make install   # local venv + deps
make migrate   # alembic upgrade head
make seed      # dev admin user
make test      # pytest
make lint      # ruff
```

Other run options:

```bash
python run.py
# or
fastapi dev run.py
```

## Database

- **Default:** SQLite file `dev.db` in project root.
- **Schema:** Alembic migrations — `alembic upgrade head` (not auto-created on app boot).
- **Dev data:** `python scripts/seed.py` after migrations.
- **MySQL:** set `DATABASE_URL` in `.env` (see `.env.example`). Requires `pymysql`.

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

## New project from this template

```bash
./scripts/new-project.sh ../my-api "My API"
# or: make new-project DIR=../my-api NAME="My API"
```

Full guide: [TEMPLATE.md](TEMPLATE.md).

## Before production

Checklist: [PRODUCTION.md](PRODUCTION.md).

## Layout & learning path

See [project-structure.md](project-structure.md).

## Request flow

1. `app/main.py` — app factory, middleware, routers
2. `app/api/v1/router.py` — route registration
3. `app/api/deps.py` — dependency injection
4. `app/services/` — business logic
5. `app/repositories/` — data access
6. `app/schemas/` — request/response models

## Auth

- Passwords stored as **bcrypt** hashes.
- Login at `POST /api/v1/auth/login` → JWT (`admin` / `secret123` after seed).
- Protected routes: `Authorization: Bearer <token>`.
- Login rate limit: 5 attempts per IP per 60 seconds.

## API

- Errors: `{"detail": ..., "code": "..."}`.
- `GET /api/v1/users` — paginated (`page`, `page_size`).
- Responses include `X-Request-ID` header.

## Tests

```bash
pytest app/tests/ -q
```
