# Using this repo as a project template

For a complete explanation of how this project works, read [DOCUMENTATION.md](DOCUMENTATION.md).

## Option A — `new-project` script (recommended)

From this repository root:

```bash
./scripts/new-project.sh ../my-billing-api "Billing API"
cd ../my-billing-api
make install
make migrate
make seed
uvicorn app.main:app --reload
```

Or via Makefile:

```bash
make new-project DIR=../my-billing-api NAME="Billing API"
```

The script:

- Copies the tree (excludes `.git`, `.venv`, `*.db`, `.env`)
- Replaces `FastAPI Template` → your display name
- Replaces `fastapi-template` → slug (for docs/docker labels)
- Creates `.env` with a new random `SECRET_KEY`
- Writes `.template-origin` metadata file

## Option B — GitHub template / manual copy

```bash
cp -r my-fastapi my-new-project
cd my-new-project
rm -rf .git && git init
cp .env.example .env
# Edit APP_NAME, SECRET_KEY, DATABASE_URL
make install && make migrate && make seed
```

## Environment variables

| Variable | Purpose |
|----------|---------|
| `APP_NAME` | Title in OpenAPI / health |
| `SECRET_KEY` | JWT signing — must be random in prod |
| `DATABASE_URL` | SQLAlchemy URL (SQLite dev, MySQL/Postgres prod) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | JWT lifetime |
| `CORS_ORIGINS` | Allowed front-end origins (JSON array) |
| `LOG_LEVEL` | `DEBUG` / `INFO` / `WARNING` |
| `ENABLE_DEMO_MIDDLEWARE` | `false` in production |

See `.env.example` for full list.

## Docker

```bash
make up
```

Uses MySQL from `docker-compose.yml`. Override with `.env.docker.example` if needed.

## Package name

Python package stays `app/` — rename only if you accept updating all imports (`from app.` → `from yourpkg.`).

## Before production

See [PRODUCTION.md](PRODUCTION.md).

## Template version

Tag releases on this repo for stable clones:

```bash
git tag -a template-v1.0.0 -m "Template baseline"
git push origin template-v1.0.0
```

Clone a tagged version:

```bash
git clone --branch template-v1.0.0 <repo-url> my-new-api
```

## Remaining roadmap

- Phase 7: Optional stubs (Redis cache, Celery, S3, email)
