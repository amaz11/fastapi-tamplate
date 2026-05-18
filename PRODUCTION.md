# Before production checklist

Use this list before deploying any environment that handles real users or data.

## Secrets & config

- [ ] `SECRET_KEY` is a long random value (never use `dev-only-change-me`)
- [ ] `.env` is not committed (only `.env.example` / `.env.docker.example`)
- [ ] Database credentials are unique per environment
- [ ] `ACCESS_TOKEN_EXPIRE_MINUTES` matches your security policy
- [ ] CORS `CORS_ORIGINS` lists only trusted front-end URLs (not `*`)

## Database

- [ ] `alembic upgrade head` run in CI/CD before app starts
- [ ] Backups enabled on managed database
- [ ] SQLite not used in production (use MySQL/Postgres)
- [ ] Connection string uses TLS where provider supports it

## Auth & users

- [ ] Default seed user (`admin` / `secret123`) removed or password rotated
- [ ] `scripts/seed.py` not run in production deploy pipeline (dev only)
- [ ] Login rate limiting backed by Redis (in-memory limiter is dev-only)
- [ ] Plan for refresh tokens if sessions must stay long-lived

## Application

- [ ] `ENABLE_DEMO_MIDDLEWARE=false`
- [ ] `LOG_LEVEL=WARNING` or `INFO` (not `DEBUG` in prod)
- [ ] Health check monitored (`GET /api/v1/health` expects DB up)
- [ ] Run behind HTTPS reverse proxy (nginx, Caddy, load balancer)
- [ ] Container runs as non-root (Dockerfile already uses `app` user)

## Operations

- [ ] CI passes: `make lint` and `make test`
- [ ] Error tracking configured (Sentry, etc.) if needed
- [ ] Structured logs shipped to your log aggregator
- [ ] Resource limits set on containers / processes

## Optional hardening

- [ ] Security headers at proxy (HSTS, CSP)
- [ ] Dependency scanning in CI (`pip audit`, Dependabot)
- [ ] Secrets from vault / cloud secret manager, not plain env files on disk
