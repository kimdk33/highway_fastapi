# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Highway CCTV monitoring system API — 고속도로 CCTV 조회 및 YOLO 기반 이상 징후 감지 서비스.

## Commands

```bash
# Install dependencies
uv sync

# Dev server
uvicorn app.main:app --reload

# Docker (full stack: PostGIS + FastAPI)
docker compose up --build        # all services
docker compose up db -d           # DB only for local dev

# Migrations
uv run alembic revision --autogenerate -m "description"
uv run alembic upgrade head
```

No test framework or linter is configured yet.

## Architecture

Layered architecture with strict dependency direction:

```
Endpoint → Service → CRUD → Model → PostgreSQL
```

- **Endpoints** (`app/api/v1/endpoints/`) — route handlers, request validation via schemas, session injection
- **Services** (`app/services/`) — business logic, raises domain exceptions from `app/core/exceptions.py`
- **CRUD** (`app/crud/`) — data access, inherits generic `CRUDBase[ModelType, CreateSchemaType]`
- **Models** (`app/models/`) — SQLModel `table=True` classes (DB tables)
- **Schemas** (`app/schemas/`) — SQLModel classes without `table=True` (request/response DTOs: Create, Read, Update)

Each domain (cctv, detection, traffic) has its own file in every layer.

## Key Design Decisions

- **SQLModel** for both ORM models and Pydantic schemas — same library, `table=True` distinguishes DB models from DTOs
- **CCTV location** uses PostGIS `Geometry(POINT, SRID=4326)` via GeoAlchemy2 — not plain lat/lng floats
- **Configuration** flows from `.env` → `pydantic-settings` (`app/core/config.py`) → `settings` singleton. All config lives in `.env`; `config.py` declares field types only, no default values for DB fields
- **Session dependency**: `app/api/deps.py` exports `SessionDep = Depends(get_session)`. Endpoints use `session: Session = SessionDep`
- **Alembic** reads DB URL dynamically from `settings.DATABASE_URL` in `migrations/env.py`, not from `alembic.ini`
- **Docker Compose** uses `env_file: .env` for both services; app overrides `DB_HOST=db` for container networking

## Alembic + PostGIS Gotchas

- `migrations/script.py.mako` includes `import sqlmodel` and `import geoalchemy2` — required because autogenerate uses `sqlmodel.sql.sqltypes.AutoString` and `geoalchemy2.types.Geometry`
- `migrations/env.py` has an `EXCLUDE_TABLES` set that filters out PostGIS/tiger/topology internal tables from autogenerate
- GeoAlchemy2 auto-creates spatial indexes on `Geometry` columns — do not add duplicate index creation in migrations

## API Routes

All domain routes are under `/api/v1/`. Router hub: `app/api/v1/router.py`.

| Prefix | Tags | Domain |
|--------|------|--------|
| `/api/v1/cctvs` | cctvs | CCTV CRUD |
| `/api/v1/detections` | detections | anomaly detection results |
| `/api/v1/traffic` | traffic | traffic info per CCTV |
| `/api/v1/health` | health | service health check |

Root `/health` endpoint also exists in `app/main.py`.

## Database

PostgreSQL 16 + PostGIS 3.4. Three tables with FK relationships:

- `cctvs` — central entity (CCTV cameras)
- `detections` → `cctvs.id` — YOLO anomaly detection results
- `traffic_info` → `cctvs.id` — vehicle count, speed, congestion level
