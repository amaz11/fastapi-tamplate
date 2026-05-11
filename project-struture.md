# FastAPI learning structure

This project now follows this layout:

```text
my_fastapi_app/
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
│   │   ├── user.py
│   │   └── base.py
│   ├── schemas/
│   │   ├── user.py
│   │   ├── auth.py
│   │   └── common.py
│   ├── services/
│   │   ├── user_service.py
│   │   └── auth_service.py
│   ├── repositories/
│   │   ├── user_repository.py
│   │   └── base.py
│   ├── middleware/
│   │   └── auth_middleware.py
│   ├── utils/
│   │   ├── helpers.py
│   │   └── response.py
│   ├── tests/
│   │   ├── test_users.py
│   │   └── test_auth.py
│   └── main.py
├── alembic/
├── env
├── requirements.txt
├── README.md
└── run.py or main.py
```

## What each part does

- `app/main.py`: create FastAPI app, register middleware, register routers.
- `app/api/v1/endpoints/*.py`: actual route functions. Keep them thin.
- `app/api/deps.py`: dependency injection. Build service/repository objects here.
- `app/core/config.py`: settings from env.
- `app/core/security.py`: token logic. Demo only, not production-safe.
- `app/core/database.py`: SQLAlchemy engine, session, base, table creation.
- `app/schemas/*`: request/response validation with Pydantic.
- `app/models/*`: domain model examples.
- `app/repositories/*`: data access layer.
- `app/services/*`: business logic layer.
- `app/middleware/*`: code that runs on every request/response.
- `app/utils/*`: small shared helper functions.
- `app/tests/*`: simple tests with `TestClient`.

## Request flow

`client -> router -> endpoint -> dependency -> service -> repository -> fake db`

## Demo endpoints

- `GET /` root message
- `GET /api/v1/health` health check
- `POST /api/v1/auth/login` get demo bearer token
- `GET /api/v1/users` list users
- `POST /api/v1/users` create user
- `GET /api/v1/users/me` read current user with bearer token

## Example learning path

1. Start app: `uvicorn app.main:app --reload`
2. Open `/docs`
3. Call `/api/v1/auth/login` with:

```json
{
  "username": "admin",
  "password": "secret123"
}
```

4. Copy `access_token`
5. Click `Authorize` in Swagger
6. Use `Bearer <token>`
7. Call `/api/v1/users/me`

## Important note

This project uses SQLAlchemy setup with SQLite default URL and fake token logic to keep learning easy.
Real production app should use:

- real database
- password hashing
- JWT or session auth
- migrations
- proper test isolation

## Flask to FastAPI mapping

Flask style:

```python
db = SQLAlchemy()
```

FastAPI style:

```python
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
```

Why different:

- Flask extension hides setup inside `SQLAlchemy()`
- FastAPI usually keeps DB pieces explicit
- `SessionLocal()` replaces request-time `db.session`
