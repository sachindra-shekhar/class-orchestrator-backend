# class-orchestrator-backend

FastAPI backend implementing tenant management and tenant-scoped class orchestration APIs under `/api/v1`.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -e .[dev]
   ```
3. Configure environment variables (optional `.env`):
   - `DATABASE_URL` (default: `postgresql+psycopg://postgres:postgres@localhost:5432/class_orchestrator`)
   - `API_PREFIX` (default: `/api/v1`)
   - `LOG_LEVEL` (default: `INFO`)

## Run migrations

```bash
alembic upgrade head
```

## Run app

```bash
uvicorn app.main:app --reload
```

- Swagger UI: `http://localhost:8000/docs`
- OpenAPI JSON: `http://localhost:8000/openapi.json`
- API base path: `http://localhost:8000/api/v1`

## Run tests

```bash
pytest
```
