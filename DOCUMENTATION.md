# FastAPI Template — Full Documentation

Read this document to understand what this project is, how it is organized, and how every major piece works together. It is written for developers who want to reuse this repo as a starting point for new APIs without building structure from scratch.

**Related files (shorter reference):**

| File | Purpose |
|------|---------|
| [README.md](README.md) | Quick start commands |
| [TEMPLATE.md](TEMPLATE.md) | How to copy this repo into a new project |
| [PRODUCTION.md](PRODUCTION.md) | Checklist before deploying to production |
| [project-structure.md](project-structure.md) | Folder tree at a glance |

---

## Table of contents

1. [What is this project?](#1-what-is-this-project)
2. [High-level architecture](#2-high-level-architecture)
3. [Project layout](#3-project-layout)
4. [How a request travels through the app](#4-how-a-request-travels-through-the-app)
5. [Layers explained](#5-layers-explained)
6. [Authentication and security](#6-authentication-and-security)
7. [Database and migrations](#7-database-and-migrations)
8. [Configuration (.env)](#8-configuration-env)
9. [Middleware](#9-middleware)
10. [Errors and logging](#10-errors-and-logging)
11. [API reference](#11-api-reference)
12. [Running the project](#12-running-the-project)
13. [Docker](#13-docker)
14. [Makefile commands](#14-makefile-commands)
15. [Testing](#15-testing)
16. [Creating a new project from this template](#16-creating-a-new-project-from-this-template)
17. [How to add a new feature](#17-how-to-add-a-new-feature)
18. [What is intentionally not included](#18-what-is-intentionally-not-included)
19. [Glossary](#19-glossary)

---

## 1. What is this project?

This repository is a **reusable FastAPI backend template**. It is not a finished product for end users; it is a **blueprint** you clone or copy when starting a new Python API.

It includes:

- A **layered architecture** (routes → services → repositories → database)
- **Versioned API** under `/api/v1`
- **User model** with registration-style create, list (paginated), and “current user”
- **JWT login** with bcrypt password hashing
- **Alembic** database migrations (schema is not auto-created on app startup)
- **Docker Compose** (API + MySQL) and a **Makefile** for common tasks
- **Tests**, **linting**, and a script to **spawn new projects** from this template

Think of it as: *“Every new API I build starts with the same solid skeleton; I only add business-specific code.”*

---

## 2. High-level architecture

```text
                    ┌─────────────────────────────────────┐
                    │           Client (browser, app)      │
                    └──────────────────┬──────────────────┘
                                       │ HTTP
                                       ▼
┌──────────────────────────────────────────────────────────────────┐
│  FastAPI app (app/main.py)                                        │
│  ┌────────────┐  ┌──────────────┐  ┌─────────────────────────┐ │
│  │ Middleware │→ │ API routers  │→ │ Endpoints (thin handlers) │ │
│  │ CORS, ID   │  │ /api/v1/...  │  │ auth, users, health     │ │
│  └────────────┘  └──────────────┘  └───────────┬─────────────┘ │
│                                                   │ Depends()     │
│                                                   ▼               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Services — business rules (AuthService, UserService)         │ │
│  └───────────────────────────────┬────────────────────────────┘ │
│                                  ▼                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ Repositories — SQL queries (UserRepository)                  │ │
│  └───────────────────────────────┬────────────────────────────┘ │
│                                  ▼                               │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │ SQLAlchemy models + database (SQLite or MySQL)               │ │
│  └────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

**Design principle:** each layer has one job. Routes should stay thin; business logic lives in services; SQL lives in repositories.

---

## 3. Project layout

```text
my-fastapi/
├── app/                          # Application code (Python package)
│   ├── main.py                   # App factory, lifespan, middleware, routers
│   ├── api/
│   │   ├── deps.py               # Dependency injection (DB session, services, current user)
│   │   └── v1/
│   │       ├── router.py         # Combines all v1 endpoint routers
│   │       └── endpoints/        # Route handlers (auth, users, health)
│   ├── core/
│   │   ├── config.py             # Settings from environment
│   │   ├── database.py           # Engine, sessions, DB health check
│   │   ├── security.py           # bcrypt + JWT helpers
│   │   ├── exceptions.py         # Global error JSON shape
│   │   └── logging.py            # Log format and level
│   ├── models/                   # SQLAlchemy table definitions
│   ├── schemas/                  # Pydantic request/response models
│   ├── services/                 # Business logic
│   ├── repositories/             # Database access
│   ├── middleware/               # Request ID, optional demo header
│   ├── utils/                    # Pagination, rate limit, response helpers
│   └── tests/                    # pytest + TestClient
├── alembic/                      # Database migration scripts
├── scripts/
│   ├── seed.py                   # Dev-only: create admin user
│   └── new-project.sh            # Copy template → new directory
├── docker/
│   └── entrypoint.sh             # Docker: wait DB, migrate, seed, start uvicorn
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── requirements.txt              # Runtime dependencies
├── requirements-dev.txt          # pytest, ruff
├── .env.example                  # Environment variable template
├── DOCUMENTATION.md              # This file
├── TEMPLATE.md
├── PRODUCTION.md
└── README.md
```

---

## 4. How a request travels through the app

Example: `GET /api/v1/users/me` with a Bearer token.

| Step | Where | What happens |
|------|--------|----------------|
| 1 | **Uvicorn** | Receives HTTP request |
| 2 | **CORS middleware** | Adds CORS headers if origin allowed |
| 3 | **RequestIdMiddleware** | Assigns `X-Request-ID`, logs method + path + status |
| 4 | **Router** | Matches `/api/v1/users/me` → `users.read_me` |
| 5 | **`deps.get_current_user`** | Reads `Authorization: Bearer <jwt>`, decodes JWT, loads user from DB |
| 6 | **Endpoint** | Returns `UserPublic` schema from the `User` model |
| 7 | **Response** | JSON + headers (including `X-Request-ID`) |

Example: `POST /api/v1/auth/login`

| Step | Where | What happens |
|------|--------|----------------|
| 1 | **Rate limit** | `check_login_rate_limit` — max 5 attempts per IP per 60s |
| 2 | **`AuthService.login`** | Find user, `bcrypt` verify password |
| 3 | **`create_access_token`** | Build JWT with `sub=username`, `exp=...` |
| 4 | **Response** | `{ "access_token": "...", "token_type": "bearer" }` |

---

## 5. Layers explained

### 5.1 Endpoints (`app/api/v1/endpoints/`)

**Job:** Define HTTP routes, status codes, and which dependencies to use.  
**Should not:** Contain SQL, password hashing, or complex business rules.

Example responsibilities:

- Parse query params (`page`, `page_size`)
- Call a service method
- Return a Pydantic `response_model`

Files:

| File | Routes |
|------|--------|
| `health.py` | `GET /health` |
| `auth.py` | `POST /auth/login` |
| `users.py` | `GET/POST /users`, `GET /users/me` |

### 5.2 Dependencies (`app/api/deps.py`)

**Job:** Wire objects into route functions via FastAPI `Depends()`.

Provides:

| Dependency | Returns |
|------------|---------|
| `get_db` | SQLAlchemy session (from `database.py`) |
| `get_user_repository` | `UserRepository` with active session |
| `get_user_service` | `UserService` |
| `get_auth_service` | `AuthService` |
| `get_current_user` | `User` model after valid JWT |

This pattern makes routes easy to test (you can override dependencies in tests).

### 5.3 Schemas (`app/schemas/`)

**Job:** Validate **incoming JSON** and shape **outgoing JSON** (Pydantic models).

Examples:

- `LoginRequest` — username + password on login
- `UserCreate` — fields required to register a user
- `UserRead` / `UserPublic` — what clients see (public omits password)

Schemas are **not** database tables. They define the API contract.

### 5.4 Models (`app/models/`)

**Job:** Define **database tables** (SQLAlchemy).

Example: `User` table with columns `id`, `username`, `email`, `full_name`, `password` (bcrypt hash), `is_active`.

### 5.5 Repositories (`app/repositories/`)

**Job:** Read and write the database. One repository per aggregate (here: `UserRepository`).

Methods:

- `list_users(skip, limit)` — paginated query
- `count_users()` — total for pagination meta
- `get_by_username(username)`
- `create_user(payload, password_hash)`

No HTTP concepts here — only DB operations.

### 5.6 Services (`app/services/`)

**Job:** **Business rules** — the place for “what should happen.”

Examples:

- `UserService.create_user` — reject duplicate username, hash password, then call repository
- `AuthService.login` — verify password, check `is_active`, return JWT

If you add “forgot password,” “invite user,” or “deactivate account,” the logic goes in a service.

### 5.7 Core (`app/core/`)

Shared infrastructure:

| Module | Role |
|--------|------|
| `config.py` | All settings; loaded from `.env` |
| `database.py` | SQLAlchemy `engine`, `SessionLocal`, `get_db()`, `check_db_connection()` |
| `security.py` | `hash_password`, `verify_password`, `create_access_token`, `decode_access_token` |
| `exceptions.py` | Uniform error body `{ "detail": ..., "code": "..." }` |
| `logging.py` | Configures Python logging on startup |

### 5.8 Utils (`app/utils/`)

Small shared helpers:

| Module | Role |
|--------|------|
| `pagination.py` | `PaginatedResponse`, `build_pagination_meta` |
| `rate_limit.py` | In-memory login throttling (dev-oriented) |
| `response.py` | `success_response()` wrapper for create user |

---

## 6. Authentication and security

### 6.1 Password storage

Passwords are **never** stored in plain text.

1. On user create (or seed), `hash_password()` runs **bcrypt**.
2. Only the hash is saved in the `users.password` column.
3. On login, `verify_password(plain, hash)` checks the password.

### 6.2 JWT access tokens

After successful login, the API returns a **JWT** (JSON Web Token).

- Signed with `SECRET_KEY` from `.env`
- Algorithm: `HS256` (config: `JWT_ALGORITHM`)
- Payload includes `sub` (username) and `exp` (expiry)
- Lifetime: `ACCESS_TOKEN_EXPIRE_MINUTES` (default 30)

Clients send:

```http
Authorization: Bearer <access_token>
```

Protected routes use `Depends(get_current_user)`.

### 6.3 Login rate limiting

`POST /auth/login` is limited to **5 attempts per client IP per 60 seconds** (in-memory).  
For production at scale, replace this with Redis-backed limiting (see [PRODUCTION.md](PRODUCTION.md)).

### 6.4 Dev seed user

After migrations, run:

```bash
python scripts/seed.py
```

Creates (if missing):

- Username: `admin`
- Password: `secret123`  
**Do not use in production** — rotate or remove after deploy.

---

## 7. Database and migrations

### 7.1 Why Alembic?

The app **does not** call `create_all()` on startup. Schema changes are versioned migration files under `alembic/versions/`. This is how real teams manage databases safely.

**First-time setup:**

```bash
alembic upgrade head    # apply all migrations
python scripts/seed.py  # optional dev data
```

**After you change a model:**

```bash
alembic revision --autogenerate -m "describe change"
alembic upgrade head
```

### 7.2 SQLite vs MySQL

| Environment | Typical `DATABASE_URL` |
|-------------|------------------------|
| Local dev | `sqlite:///./dev.db` |
| Docker Compose | `mysql+pymysql://fastapi:fastapi@db:3306/fastapi_db` |
| Production | Your managed MySQL/Postgres URL |

SQLite needs `check_same_thread=False` in SQLAlchemy (handled in `database.py`).

### 7.3 Sessions

Each request that needs the DB gets a session via `get_db()`:

1. Open session
2. Handle request
3. Close session in `finally`

Repositories receive the session from dependencies — they do not create their own.

---

## 8. Configuration (.env)

Copy `.env.example` to `.env` before running locally.

| Variable | Meaning |
|----------|---------|
| `APP_NAME` | Shown in OpenAPI title and health response |
| `APP_VERSION` | API version string |
| `API_V1_PREFIX` | Default `/api/v1` |
| `SECRET_KEY` | JWT signing key — **must be random in production** |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT lifetime |
| `JWT_ALGORITHM` | Usually `HS256` |
| `DATABASE_URL` | SQLAlchemy connection string |
| `CORS_ORIGINS` | JSON array of allowed origins |
| `LOG_LEVEL` | `DEBUG`, `INFO`, `WARNING`, … |
| `ENABLE_DEMO_MIDDLEWARE` | `true` adds `X-App-Mode: learning` header |
| `DEFAULT_PAGE_SIZE` / `MAX_PAGE_SIZE` | Pagination defaults for `GET /users` |

Settings class: `app/core/config.py` (uses `pydantic-settings`).

---

## 9. Middleware

Middleware runs **around** every request (order matters: last added runs first on the way in).

| Middleware | Purpose |
|------------|---------|
| **CORSMiddleware** | Allows browser apps on other origins to call the API |
| **RequestIdMiddleware** | Sets `X-Request-ID`, logs request line |
| **DemoHeaderMiddleware** | Optional; only if `ENABLE_DEMO_MIDDLEWARE=true` |

---

## 10. Errors and logging

### 10.1 Error response shape

All handled errors return JSON like:

```json
{
  "detail": "Incorrect username or password",
  "code": "http_401"
}
```

Validation errors (`422`) use `code: "validation_error"` with `detail` as a list of field errors.

Unhandled server errors return `500` with `code: "internal_error"` (no stack trace leaked to client).

### 10.2 Logging

On app startup (`lifespan`), logging is configured to stdout with timestamp, level, and logger name.  
`RequestIdMiddleware` logs each request when it completes.

---

## 11. API reference

Base URL (local): `http://127.0.0.1:8000`  
Interactive docs: `http://127.0.0.1:8000/docs`

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `GET` | `/` | No | Welcome message |
| `GET` | `/api/v1/health` | No | Health + DB status; `503` if DB down |
| `POST` | `/api/v1/auth/login` | No | Returns JWT |
| `GET` | `/api/v1/users` | No | Paginated user list |
| `POST` | `/api/v1/users` | No | Create user (password hashed) |
| `GET` | `/api/v1/users/me` | Bearer JWT | Current user profile |

### Paginated list response

`GET /api/v1/users?page=1&page_size=10`

```json
{
  "items": [ { "id": 1, "username": "admin", ... } ],
  "meta": {
    "page": 1,
    "page_size": 10,
    "total": 1,
    "total_pages": 1
  }
}
```

### Login response

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

## 12. Running the project

### Local (SQLite)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
python scripts/seed.py
uvicorn app.main:app --reload
```

Open: http://127.0.0.1:8000/docs

Alternative: `python run.py` (runs on port **5002** in `run.py`).

### Using Makefile

```bash
make install   # venv + deps + copy .env if missing
make migrate
make seed
# then run uvicorn yourself, or:
make up        # Docker instead
```

---

## 13. Docker

`docker-compose.yml` starts:

1. **db** — MySQL 8.4 (port 3306)
2. **api** — builds from `Dockerfile`, port 8000

`docker/entrypoint.sh` automatically:

1. Waits until MySQL accepts connections
2. Runs `alembic upgrade head`
3. Runs `scripts/seed.py`
4. Starts `uvicorn` on `0.0.0.0:8000`

```bash
make up      # build + start in background
make logs    # follow API logs
make down    # stop everything
```

Default MySQL credentials (dev only): user `fastapi`, password `fastapi`, database `fastapi_db`.

---

## 14. Makefile commands

Run `make help` for the full list.

| Command | Description |
|---------|-------------|
| `install` | Create `.venv`, install deps, copy `.env.example` if needed |
| `migrate` | `alembic upgrade head` |
| `seed` | Create dev admin user |
| `test` | Run pytest |
| `lint` / `format` | Ruff check and format |
| `up` / `down` / `logs` | Docker Compose |
| `new-project` | `make new-project DIR=../x NAME="My API"` |

---

## 15. Testing

Tests live in `app/tests/`.

`conftest.py`:

- Sets `DATABASE_URL=sqlite:///./test.db`
- Runs migrations and seed once per session
- Provides `client` (TestClient with lifespan) and `admin_token` fixtures

```bash
pytest app/tests/ -q
# or
make test
```

Tests cover login, JWT shape, `/users/me`, pagination, and create user.

CI (`.github/workflows/ci.yml`) runs ruff + pytest on push/PR.

---

## 16. Creating a new project from this template

**Recommended:**

```bash
./scripts/new-project.sh ../my-shop-api "Shop API"
cd ../my-shop-api
make install && make migrate && make seed
```

The script copies the repo (excluding `.git`, `.venv`, databases), renames placeholders, and generates a new `SECRET_KEY` in `.env`.

Details: [TEMPLATE.md](TEMPLATE.md)

---

## 17. How to add a new feature

Example: add a **Product** resource.

1. **Model** — `app/models/product.py` (SQLAlchemy table)
2. **Import model** in `alembic/env.py` so autogenerate sees it
3. **Migration** — `alembic revision --autogenerate -m "add products"`
4. **Schemas** — `app/schemas/product.py` (Pydantic)
5. **Repository** — `app/repositories/product_repository.py`
6. **Service** — `app/services/product_service.py`
7. **Deps** — `get_product_repository`, `get_product_service` in `deps.py`
8. **Endpoints** — `app/api/v1/endpoints/products.py`
9. **Router** — include in `app/api/v1/router.py`
10. **Tests** — `app/tests/test_products.py`

Keep the same flow: **endpoint → Depends → service → repository → DB**.

---

## 18. What is intentionally not included

These are left for you or later phases:

- Refresh tokens / OAuth2 providers
- Role-based access control (RBAC)
- Redis cache, Celery background jobs, S3 uploads (Phase 7 stubs optional)
- Email sending
- Admin UI
- Production-grade rate limiting (Redis)

See [PRODUCTION.md](PRODUCTION.md) before going live.

---

## 19. Glossary

| Term | Meaning |
|------|---------|
| **FastAPI** | Modern Python web framework for APIs |
| **Pydantic** | Data validation via Python type hints |
| **SQLAlchemy** | ORM for talking to SQL databases |
| **Alembic** | Migration tool for SQLAlchemy |
| **JWT** | Signed token proving identity between requests |
| **bcrypt** | Slow password hashing algorithm |
| **Dependency injection** | FastAPI `Depends()` supplies shared objects per request |
| **Repository** | Class that encapsulates database queries |
| **Service** | Class that encapsulates business rules |
| **Schema** | Pydantic model for API input/output |
| **Model** | SQLAlchemy class for a database table |
| **Lifespan** | Startup/shutdown hooks (replaces old `@app.on_event`) |

---

## Quick mental model

```text
You write business logic in SERVICES.
You write SQL in REPOSITORIES.
You write HTTP in ENDPOINTS.
You write validation in SCHEMAS.
You write tables in MODELS.
You configure everything in .env → config.py.
You change the database with ALEMBIC, not at app startup.
```

If you remember only one sentence:

> **Requests enter through endpoints, pass through dependencies into services, and reach the database through repositories.**

That is the entire architecture this template teaches.
