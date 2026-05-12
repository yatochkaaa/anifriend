# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**AniFriend** — AI-driven anime recommender for the CIS audience (18-35 y.o.). Think of it as a "smart anime friend" — the app asks the user questions about their preferences (genres, studios, characters, mood) and AI analyzes them to recommend anime with explanations ("why this fits you").

**Key differentiators from existing services (MAL, AniList):**
- Russian-language UX and Russian anime titles (via Shikimori API)
- "Anime by mood" feature — e.g. "for a sad day", "for a lazy evening" (inspired by Japanese services like Anime-Planet, localized for CIS)
- Social layer: users share recommendations and create "anime dates" (virtual watch-together sessions with real-time chat)
- AI personalization — not just filters, but actual reasoning behind each recommendation

**Target gap:** Japan has MAL/AniList with rich communities; CIS has no AI-personalized service with Russian-language UX and social features.

## Working Style

Claude acts as a **mentor**, not a code writer. The developer writes the code; Claude keeps the plan, explains approaches, reviews on request. Code examples only when explicitly asked.

Code quality bar: **enterprise-level**. Every decision (structure, naming, patterns, configs) should follow best practices for the given technology. If something is done "the wrong way" — point it out even if it works.

Commit discipline: remind the developer to commit at logical checkpoints — when a cohesive unit of work is complete (e.g. model done, schemas done, endpoint done). Use Conventional Commits format: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`. Each commit = one concern.

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.14 + FastAPI |
| Frontend | React + TypeScript |
| Database | PostgreSQL + Redis (cache) |
| AI/ML | Scikit-learn → Hugging Face Transformers |
| External API | Shikimori API (русские названия, СНГ-аудитория) |
| Infrastructure | Docker + docker-compose |
| CI/CD | GitHub Actions |
| Testing | Pytest (backend), Jest + Cypress (frontend) |
| Deploy | Heroku/Vercel → AWS |

## Architecture

Microservices:
- `frontend/` — React SPA
- `backend/` — FastAPI (API gateway + business logic)
- AI service — separate microservice for recommendations
- PostgreSQL + Redis

## Project Structure

```
backend/
  app/
    core/
      config.py     # Pydantic Settings (env vars, DB URL)
      db.py         # SQLAlchemy engine + session maker
    models/
      base.py       # DeclarativeBase, shared type annotations
      user.py       # User ORM model
    routers/        # FastAPI route handlers
    schemas/
      user.py       # Pydantic schemas (UserCreate, UserRead, UserUpdate)
    services/       # Business logic layer
    main.py         # FastAPI app entrypoint
  alembic/          # DB migrations
  alembic.ini
  pyproject.toml
  requirements.txt
  .venv/            # Python 3.14.4 virtual environment
```

## Development Roadmap

| Stage | Description | Status |
|---|---|---|
| 1 | Planning: Shikimori API research, project structure, repo setup | **Done** |
| 2 | Backend MVP: /survey and /recommend endpoints, Shikimori integration | **Current** |
| 3 | Frontend MVP: React survey form + recommendations page | Planned |
| 4 | Testing + launch: deploy, community feedback | Planned |
| 5 | Extensions: JWT auth, ML model, WebSocket chat, mobile | Future |

## Backend

**Python version:** 3.14.4
**Virtual environment:** `.venv`

Activate the venv before running any Python commands:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Run the backend:

```powershell
uvicorn app.main:app --reload
```

## Key Decisions

- **SQLAlchemy + Pydantic separately** (not SQLModel) — cleaner separation between DB models and API schemas
- **`models/base.py`** holds `Base`, `DeclarativeBase` and shared type annotations (`int_pk`, `str_uniq`, etc.)
- **`core/db.py`** holds only engine and session maker — no model logic
- **Alembic at `backend/` root** — correct placement, not inside `app/`
- **`UserUpdate` has no password fields** — password change is a separate flow (`UserChangePassword`)
- **Shikimori API** chosen over AniList for Russian titles and CIS audience

## Frontend

Not yet initialized. Commands will be added here once the frontend is set up.
