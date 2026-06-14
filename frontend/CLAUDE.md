@AGENTS.md

# Frontend

**Framework:** Next.js 16 (App Router)
**Package manager:** Bun
**UI components:** shadcn/ui + Tailwind CSS

## Documentation References

Before implementing any Next.js or shadcn feature, read the relevant doc:
- Next.js: `node_modules/next/dist/docs/` (version-matched)
- shadcn/ui: https://ui.shadcn.com/llms.txt

## Project Structure

```
frontend/
  app/
    layout.tsx                      # Root layout
    page.tsx                        # Home page
    globals.css
    login/
      page.tsx
      LoginForm.tsx                 # Client Component
    signup/
      page.tsx
      SignupForm.tsx                # Client Component
    survey/
      page.tsx
      SurveyForm.tsx               # Client Component
    recommendations/
      page.tsx
      RecommendationList.tsx       # Client Component
  components/
    Navbar.tsx
    NavbarUserMenu.tsx
    ui/                            # shadcn/ui components
      button.tsx, card.tsx, input.tsx, checkbox.tsx, ...
  lib/
    actions/                       # Next.js Server Actions
      auth.ts
      survey.ts
      users.ts
    api/                           # API client functions (fetch to backend)
      auth.ts
      genres.ts
      recommend.ts
      survey.ts
    utils.ts
  types/                           # TypeScript type definitions
    anime.ts, auth.ts, genre.ts, survey.ts
  proxy.ts                         # Dev proxy to backend
  next.config.ts
  components.json                  # shadcn/ui config
  package.json
```

## Key Decisions

- **Next.js 16 App Router** — SSR, file-based routing, Server/Client Components
- **Bun** — package manager and runtime (faster than npm/yarn)
- **shadcn/ui** — copy-paste component library, components live in `components/ui/`
- **Tailwind CSS** — utility-first styling
- **Server Actions** в `lib/actions/` — мутации через Next.js Server Actions, не REST с клиента
- **API клиент** в `lib/api/` — fetch-функции к бэкенду, используются в Server Actions и Server Components
- **`proxy.ts`** — dev-прокси, перенаправляет запросы к FastAPI бэкенду в режиме разработки

## Commands

```bash
# Install dependencies
cd frontend && bun install

# Run dev server
cd frontend && bun dev

# Build
cd frontend && bun run build

# Lint
cd frontend && bun run lint
```
