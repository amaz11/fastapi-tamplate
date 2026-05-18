# Project structure

```text
my-fastapi/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── users.py
│   │   │   │   ├── auth.py
│   │   │   │   └── health.py
│   │   │   └── router.py
│   │   └── deps.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── models/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   ├── middleware/
│   ├── utils/
│   ├── tests/
│   └── main.py
├── alembic/
│   └── versions/
├── scripts/
│   ├── seed.py
│   └── new-project.sh
├── PRODUCTION.md
├── TEMPLATE.md
├── .env.example
├── alembic.ini
├── requirements.txt
├── TEMPLATE.md
├── README.md
└── run.py
```

├── Dockerfile
├── docker-compose.yml
├── Makefile
├── docker/entrypoint.sh

## What each part does

| Path | Role |
|------|------|
| `app/main.py` | Create app, middleware, routers, startup |
| `app/api/v1/endpoints/` | Route handlers (keep thin) |
| `app/api/deps.py` | Dependency injection |
| `app/core/config.py` | Settings from `.env` |
| `app/core/security.py` | Password hashing + JWT create/decode |
| `app/core/database.py` | SQLAlchemy engine, session, DB health check |
| `app/schemas/` | Pydantic request/response models |
| `app/models/` | SQLAlchemy tables |
| `app/repositories/` | Data access |
| `app/services/` | Business logic |
| `app/middleware/` | Request ID, optional demo header |
| `app/core/exceptions.py` | Global error handlers |
| `app/core/logging.py` | Logging setup |
| `app/utils/` | Shared helpers, pagination |
| `app/tests/` | `TestClient` tests |

## Request flow

`client → router → endpoint → Depends → service → repository → database`

## Demo endpoints

- `GET /` — root message
- `GET /api/v1/health` — health check (includes DB ping; 503 if DB down)
- `POST /api/v1/auth/login` — JWT access token
- `GET /api/v1/users` — list users (paginated)
- `POST /api/v1/users` — create user
- `GET /api/v1/users/me` — current user (Bearer token)

## Example: Swagger auth flow

1. Start: `uvicorn app.main:app --reload`
2. Open `/docs`
3. `POST /api/v1/auth/login`:

```json
{
  "username": "admin",
  "password": "secret123"
}
```

4. Copy `access_token`
5. **Authorize** → `Bearer <token>`
6. Call `GET /api/v1/users/me`

## Database

- **Default:** SQLite (`sqlite:///./dev.db`) — file created on startup.
- **MySQL:** set `DATABASE_URL` in `.env` to `mysql+pymysql://...`.

Schema via Alembic: `alembic upgrade head`. Dev user via `python scripts/seed.py`.

## Documentation

- [DOCUMENTATION.md](DOCUMENTATION.md) — full architecture and how-to guide
- [PRODUCTION.md](PRODUCTION.md) — deploy checklist
- [TEMPLATE.md](TEMPLATE.md) — spawn new projects

## Optional next steps

- Refresh tokens, RBAC, Redis rate limit, background jobs (see DOCUMENTATION.md §18)
