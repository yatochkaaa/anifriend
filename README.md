# AniFriend — AI Anime Recommender

**AniFriend** is a personalized anime recommendation service. Instead of manually browsing filters, users fill out a short preference survey — and get tailored recommendations with reasoning.

**Live demo:** [anifriend-inky.vercel.app](https://anifriend-inky.vercel.app)  
**API docs:** [anifriend.onrender.com/docs](https://anifriend.onrender.com/docs)

> [!WARNING]
> The backend is hosted on Render's free tier and **may take up to 1 minute to cold start** after a period of inactivity. If the app seems unresponsive — wait a moment and try again.

---

## Features

- Preference survey — genres to prefer and avoid, favorite anime and characters
- Personalized recommendations via [Shikimori API](https://shikimori.one)
- Auth with JWT (register / login / logout)
- Update survey at any time — recommendations update accordingly
- Protected routes with middleware-based redirect

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js 16 · TypeScript · Tailwind CSS · shadcn/ui |
| Backend | Python 3.14 · FastAPI · SQLAlchemy (async) · Alembic |
| Database | PostgreSQL |
| External API | Shikimori GraphQL API |
| Package Manager | Bun (frontend) · uv (backend) |
| Infrastructure | Docker · Render (backend) · Vercel (frontend) |

## Architecture

Monorepo with two services:

```
hikkin-dom/
  backend/    — FastAPI REST API + Shikimori integration
  frontend/   — Next.js App Router (SSR + Client Components)
```

The backend exposes `/api/v1/` endpoints for auth, survey, and recommendations. The frontend fetches data server-side where possible (Server Components + Server Actions) and uses cookies for auth state.

## Local Development

**Requirements:** PostgreSQL, Bun, Python 3.14, uv

**Backend:**
```bash
cd backend
uv sync
cp ../.env.example ../.env  # fill in values
alembic upgrade head
fastapi dev
```

**Frontend:**
```bash
cd frontend
bun install
bun dev
```

## Roadmap

- [ ] Bug fixes and test coverage (unit + e2e)
- [ ] JWT refresh tokens + social auth
- [ ] "Anime by mood" feature ("for a sad day", "for a lazy evening")
- [ ] Social layer: share recommendations, create anime watch-together sessions with real-time chat
- [ ] ML-based recommendations (Scikit-learn → Hugging Face)
