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

Commit discipline: remind the developer to commit at logical checkpoints — when a cohesive unit of work is complete (e.g. model done, schemas done, endpoint done). Use Conventional Commits format: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`. For monorepo use scope: `feat(backend):`, `feat(frontend):`. Each commit = one concern.

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

Microservices in a monorepo:
- `frontend/` — React SPA
- `backend/` — FastAPI (API gateway + business logic)
- AI service — separate microservice for recommendations (future)
- PostgreSQL + Redis

## Project Structure

```
hikkin-dom/
  backend/
    app/
      api/
        routes/
          users.py      # /api/v1/users
          survey.py     # /api/v1/survey
          recommend.py  # /api/v1/recommend
        main.py         # api_v1_router aggregator
      core/
        config.py       # Pydantic Settings (env vars, DB URL)
        db.py           # SQLAlchemy engine + session maker
      models/
        base.py         # DeclarativeBase, shared type annotations (int_pk, str_uniq, etc.)
        user.py         # User ORM model
      schemas/
        user.py         # Pydantic schemas (UserCreate, UserRead, UserUpdate)
      services/         # Business logic layer
      main.py           # FastAPI app entrypoint
    alembic/            # DB migrations (to be configured)
    alembic.ini
    pyproject.toml
    requirements.txt
    .venv/              # Python 3.14.4 virtual environment
  frontend/             # Not yet initialized
  docs/
    PLAN.md             # Full product plan
  .env                  # Environment variables (not committed)
  .gitignore
```

## Development Roadmap

| Stage | Description | Status |
|---|---|---|
| 1 | Planning: Shikimori API research, project structure, repo setup | **Done** |
| 2 | Backend MVP: /survey and /recommend endpoints, Shikimori integration | **Current** |
| 3 | Frontend MVP: React survey form + recommendations page | Planned |
| 4 | Testing + launch: deploy, community feedback | Planned |
| 5 | Extensions: JWT auth, ML model, WebSocket chat, mobile | Future |

## Future Modules (Roadmap)

### 2. Anime Fanfic Generator with Collaborative Editing
Platform where users generate fan fiction via AI (input characters + plot → get a story). Collaborative mode: multiple users edit text in real-time like Google Docs, but anime-themed (illustrations, voice comments). Voice AI integration for "narrating" stories. Generation in Russian + translations.
> Tech to explore: GPT-like models, WebSockets + Operational Transform for real-time collab, AWS S3, DALL-E for illustrations, PWA.

### 3. Anime Collector with AR and NFT
Virtual collector of anime figures/cards — users build collections of anime characters. AR mode: show a figure in the real world via phone camera. NFT for unique items (rare cards tradeable on blockchain). Synced with real anime releases and local CIS shops.
> Tech to explore: ARCore/ARKit, Ethereum/blockchain for NFT, Flutter/React Native, ML for generating unique cards.

### 4. Anime Stream Chat with Interactive Features
Streaming platform for anime with built-in chat where viewers vote on next episode, add emoji reactions, or influence the plot (for fan content). AI moderation and meme generation. Legal content alternative to pirate sites for CIS, with Russian focus.
> Tech to explore: WebRTC/HLS for video streaming, Socket.io for real-time chat, NLP for moderation, payment integration for premium features.

### 5. Anime Quiz Bot with Social Tournaments
Telegram/Discord bot or web app with anime quizzes (characters, plots, memes). Team tournaments with AI-generated questions and rewards (virtual badges). Integrated with anime release calendar. Russian questions and local memes.
> Tech to explore: Telegram API, ML for question generation, WebSockets for real-time updates, leaderboard DB, external API integrations.

## Key Decisions

- **SQLAlchemy + Pydantic separately** (not SQLModel) — cleaner separation between DB models and API schemas
- **`models/base.py`** holds `Base`, `DeclarativeBase` and shared type annotations (`int_pk`, `str_uniq`)
- **`core/db.py`** holds only engine and session maker — no model logic
- **`api/routes/`** instead of `routers/` — follows FastAPI full-stack template pattern
- **`api_v1_router`** aggregates all routes, prefix `/api/v1` set in `main.py` via `settings.API_V1_STR`
- **Alembic at `backend/` root** — correct placement, not inside `app/`
- **`UserUpdate` has no password fields** — password change is a separate flow (`UserChangePassword`)
- **`UserPasswordMixin`** handles password validation (min 8 chars, match check) — used only in `UserCreate`
- **Monorepo** — backend + frontend in one repo, can split later via `git subtree split`
- **Shikimori API** chosen over AniList for Russian titles and CIS audience

## Backend

**Python version:** 3.14.4
**Virtual environment:** `backend/.venv`

Activate the venv before running any Python commands:

```powershell
backend\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r backend/requirements.txt
```

Run the backend:

```powershell
cd backend
uvicorn app.main:app --reload
```

## Frontend

Not yet initialized. Commands will be added here once the frontend is set up.
