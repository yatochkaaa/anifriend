# Backend

**Language:** Python 3.14.4
**Framework:** FastAPI
**Virtual environment:** `backend/.venv`

## Project Structure

```
backend/
  app/
    api/
      routes/
        users.py      # /api/v1/users
        survey.py     # /api/v1/survey
        recommend.py  # /api/v1/recommend
      deps.py         # FastAPI dependencies (SessionDep, ShikimoriDep)
      main.py         # api_v1_router aggregator
    core/
      config.py       # Pydantic Settings (env vars, DB URL)
      db.py           # SQLAlchemy async engine + session maker
    dto/              # TypedDict DTOs (boundary between routes and services)
    integrations/
      shikimori.py    # ShikimoriClient, ShikimoriAnime, ShikimoriGenre models
    models/
      base.py         # DeclarativeBase, shared type aliases (int_pk, IntrospectedEnum)
      user.py         # User ORM model
      survey.py       # Survey, SurveyGenre, SurveyAnime, SurveyCharacter
      genre.py        # Genre ORM model + GenreKindEnum
      watched_anime.py # WatchedAnime + WatchedAnimeStatus
    schemas/
      user.py         # UserCreate, UserRead, UserUpdate
      survey.py       # SurveyCreate, SurveyRead, SurveyUpdate
      anime.py        # AnimeRead, PosterRead
    services/
      survey.py       # get_survey, add_survey, modify_survey
      recommend.py    # get_recommendations
    main.py           # FastAPI app entrypoint + lifespan (ShikimoriClient)
  scripts/
    seed_genres.py    # Seeds genres from Shikimori API into DB
  alembic/            # DB migrations
  alembic.ini
  pyproject.toml
```

## Key Decisions

- **SQLAlchemy + Pydantic separately** (not SQLModel) — cleaner separation between DB models and API schemas
- **`models/base.py`** holds `Base`, `DeclarativeBase`, shared type aliases (`int_pk`), and `IntrospectedEnum` helper
- **`IntrospectedEnum`** — wraps `sa.Enum` with `values_callable` to store lowercase values (StrEnum + auto())
- **`core/db.py`** holds only engine and session maker — no model logic
- **`api/routes/`** instead of `routers/` — follows FastAPI full-stack template pattern
- **`api_v1_router`** aggregates all routes, prefix `/api/v1` set in `main.py` via `settings.API_V1_STR`
- **`ShikimoriClient`** stored in `app.state` via lifespan — single instance, connection pooling via httpx
- **`ShikimoriDep` / `SessionDep`** in `api/deps.py` — typed FastAPI dependencies for DI
- **DTO pattern** — services accept TypedDicts, Pydantic schemas only in routes
- **Alembic at `backend/` root** — correct placement, not inside `app/`
- **Shikimori API** via GraphQL — genre filter is AND logic, so parallel requests per genre via `asyncio.gather()`
- **Shikimori IDs** are strings in API but stored/used as `int` — Pydantic coerces on validate
- **`UserUpdate` has no password fields** — password change is a separate flow

## Commands

```bash
# Activate venv
source backend/.venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt

# Run dev server
cd backend && uvicorn app.main:app --reload

# Run migrations
cd backend && .venv/bin/alembic upgrade head

# Run tests
cd backend && .venv/bin/pytest tests/ -v
```
