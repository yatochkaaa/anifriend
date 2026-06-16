@AGENTS.md

# Frontend

**Framework:** Next.js 16 (App Router)
**Package manager:** Bun
**UI components:** shadcn/ui + Tailwind CSS

## Documentation References

Before implementing any Next.js or shadcn feature, consult docs MCP-first (see root `CLAUDE.md` → Documentation Sources):
- **Next.js** → `next-devtools` MCP (`nextjs_docs` + `nextjs-docs://llms-index`). Local `node_modules/next/dist/docs/` is the offline fallback and the source of truth on any version conflict (matches installed `next@16.2.6`).
- **shadcn/ui** → `shadcn` skill / MCP; `https://ui.shadcn.com/llms.txt` as fallback.
- **Other libraries** → Context7.

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
- **Server Actions** in `lib/actions/` — mutations go through Next.js Server Actions, not REST from the client
- **API client** in `lib/api/` — fetch functions to the backend, used in Server Actions and Server Components
- **`proxy.ts`** — dev proxy, forwards requests to the FastAPI backend in development

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
