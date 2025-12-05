# smbOss Backend (FastAPI)

Project scaffold for a FastAPI backend with public, user, and admin APIs.

## Quick start
- Create and populate `.env` (see `.env.example`).
- Install deps: `python -m venv .venv && .venv\\Scripts\\activate && pip install -r requirements.txt`
- Run dev server: `uvicorn app.main:app --reload`

## Project layout
- `app/main.py` – FastAPI entrypoint and router wiring.
- `app/api/v1/` – Public, user, and admin route modules.
- `app/models` & `app/schemas` – Data models and request/response schemas.
- `app/services` – Business logic layer (currently in-memory stubs).
- `app/core` – Security, time utilities, result parsing helpers, constants, dependencies.
- `app/config.py` – Settings loaded from environment.
- `app/database.py` – Placeholder for DB session factory.
- `tests/` – Minimal placeholder tests.

## Notes
- This scaffold uses in-memory stores for demonstration; replace with real DB logic in `database.py` and services.

"# smboss_satta_server" 


# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup environment
cp .env.example .env
# Edit .env with your database credentials

# 4. Initialize database
python scripts/init_db.py

# 5. Run migrations
alembic upgrade head

# 6. Start server
uvicorn app.main:app --reload

# 7. Visit API documentation
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
