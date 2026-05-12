# AniFriend — Product Plan

## 1. Project Description

**Name:** AniFriend ("Аниме-Друг" for Russian localization).

**Goal:** Help users discover new anime through personalized recommendations. Core feature — AI analysis of preferences (genres, studios, characters) and recommendation generation with explanations. Additional: social layer (sharing recommendations), release calendar integration, Russian-language localization (subtitles, descriptions).

**Target audience:** Anime fans in CIS (18-35 y.o.), both newcomers and experienced viewers. Japan has similar services (MyAnimeList, AniList), but CIS has almost no AI-driven tools — this is the competitive advantage.

**MVP:** Web app with a survey form, AI recommendations, and an anime list. No social features at start.

## 2. Key Features

### MVP (in scope)
- **Survey:** User answers questions ("Do you like romance? What genres?")
- **AI recommendations:** Generates a list of anime based on answers with explanations ("Why this fits you")
- **Search and filters:** Browse anime by genres, ratings, studios

### Extended (future)
- **Social network:** Users share recommendations, vote for "anime dates"
- **API integrations:** Sync with AniList/MAL for additional data
- **Personalization:** Watch history tracking and improving recommendations over time
- **Mobile version:** PWA or native app

### CIS-specific differentiators
- Russian subtitles/descriptions
- Integration with Russian resources (Shikimori, fan sites)

## 3. Architecture

Microservices (for scalability testing):
- **Frontend** — React SPA (survey UI + recommendations page)
- **Backend** — FastAPI (API gateway + business logic)
- **AI service** — separate microservice for recommendations (Python + ML)
- **Database** — PostgreSQL for users and anime data
- **External API** — Shikimori API for Russian titles and CIS-relevant data

## 4. Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + FastAPI (async, fast) |
| Frontend | React + TypeScript |
| Database | PostgreSQL + Redis (recommendations cache) |
| AI/ML | Scikit-learn → Hugging Face Transformers (NLP for preferences) |
| External API | Shikimori API (Russian titles, CIS audience) |
| Infrastructure | Docker + docker-compose |
| CI/CD | GitHub Actions |
| Testing | Pytest (backend), Jest + Cypress (frontend) |
| Deploy | Heroku/Vercel → AWS |

## 5. Development Roadmap

### Stage 1: Planning and Prototype (1-2 weeks) — DONE
- [x] Research Shikimori API (docs, test queries)
- [ ] Create interface mockups (Figma or sketches)
- [ ] Set up repository (Git), CI/CD (GitHub Actions)
- **Goal:** Understand available data, define project structure

### Stage 2: Backend MVP (2-3 weeks) — IN PROGRESS
- [ ] Set up FastAPI project structure (routers, models, schemas, services, db)
- [ ] Connect PostgreSQL, create User model
- [ ] Implement `/survey` endpoint
- [ ] Implement `/recommend` endpoint (rule-based first, ML later)
- [ ] Integrate Shikimori API as data source
- [ ] Tests: Pytest, Postman
- **Goal:** API returns 5 recommendations based on survey

### Stage 3: Frontend MVP (2-3 weeks)
- [ ] Create React app with survey form and recommendations page
- [ ] Connect to backend
- [ ] Basic design (anime style: bright colors, icons)
- [ ] Tests: Cypress e2e
- **Goal:** Working UI connected to backend

### Stage 4: Testing and Launch (1 week)
- [ ] Integration testing (backend + frontend)
- [ ] Deploy to Heroku/Vercel
- [ ] Collect feedback from communities (VK, Reddit anime subs)
- **Goal:** Live site with recommendations

### Stage 5: Extensions (future sprints)
- [ ] JWT authentication
- [ ] Improve AI: ML model trained on user data
- [ ] Social features: real-time chat via WebSockets
- [ ] Mobile version: React Native
- [ ] Integrate future modules (fanfic generator, quiz bot, etc.)

**Overall timeline:** 2-3 months to MVP.

## 6. Monetization

- **Freemium:** Basic recommendations free, premium (advanced AI, no ads) — $5-10/month
- **Advertising:** Anime studios and merch shops
- **Future:** NFT for exclusive recommendations

## 7. Success Metrics

- 1,000+ users in the first year
- Positive reviews in CIS anime communities

## 8. Risks

| Risk | Mitigation |
|---|---|
| AI inaccurate at start (needs data) | Start with rule-based, collect data, improve over time |
| Shikimori API rate limits | Cache responses in Redis, batch requests |
| Russian localization effort | Use Shikimori which already has Russian content |
