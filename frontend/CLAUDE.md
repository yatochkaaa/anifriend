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

## Design Direction

**Concept: "Companion-led warmth".** AniFriend's personality is a slightly goofy, emotional anime guide — a friend who pulls faces, cheers you on, and hands you anime that match your mood. The product gives the user warmth, fun, and a little silliness so they can switch off and feel something. Tone: playful, bright, genki — never tiring.

**The discipline that keeps "fun" from turning into "garish"** (the real risk of this brief): keep a calm, warm canvas and spend color on accents, motion, the character, and copy — not on every surface. One accent leads per view (driven by the active mood); the rest stays quiet. This is how playful brands stay premium (Duolingo/Discord energy, not a flashing banner). If a view feels loud everywhere, it's wrong.

**Don't default.** Avoid the stock AI looks: cream + serif + terracotta; near-black + one acid accent; broadsheet hairlines. Our warmth comes from a curated multicolor anime palette + an expressive character, not from a single trendy accent.

**Themes** — ship both **light** and **dark** (Stage 3, Frontend MVP). Tokens are theme-aware; the multicolor accents are shared, tuned to glow on dark and sing on light.

**Color** — mid-bright, pleasant anime/Japanese hues; saturated enough to feel genki, softened so nothing stings the eye.
- Light: `Cream #FFF8F2` canvas · `Cloud #FFFFFF` surface · `Sumi #2B2533` text · `Mist #8A8398` secondary
- Dark: `Night #1E1A2A` canvas · `Slate #2A2538` surface · `Paper #F4EFF7` text · `Haze #9A93AC` secondary
- Mood/accent spectrum (shared, one leads at a time): `Sakura #FF8FB1` · `Sky #5FC9E8` · `Sun #FFC24B` · `Matcha #8BD17C` · `Ube #A98BE8`

**Type** — all four ship Latin + Cyrillic (critical for the CIS audience):
- **Unbounded** — display; bouncy geometric, big and with restraint
- **Onest** — body; Cyrillic-first grotesque, clean and friendly
- **Caveat** — the companion's voice *only*; handwritten, used for the character's speech bubbles / popups so its "friend's note" feel never bleeds into UI chrome
- **JetBrains Mono** — utility: data and labels ("92% match", episodes, ratings)

**Layout** — a conversational vertical flow, not a dense catalog grid. The hero is a question from the guide + an interactive mood picker (the page's thesis). Recommendation cards read as a "note from a friend" with the AI's "why this fits you" reasoning, not a metadata row.

**Signature — a companion that arrives in layers.** The personality ships before its body does:
1. **Voice & color first** (MVP) — handwritten popups, mood-driven multicolor, playful hover micro-interactions.
2. **Embodied chibi later** — once the conversational-AI layer is live (it shares that AI plumbing): an interactive chibi guide that reacts to hovers, pulls faces, and drops the occasional text bubble. It becomes the brand's one memorable element; everything else stays quiet so it can be loud. Roadmap lives in root `CLAUDE.md`.

**Motion** — playful, small, intentional: card hover wobble, popup pop-in, the eventual character's expressions. `prefers-reduced-motion` disables the character's idle motion and ambient transitions.

**Voice** — Russian, informal "ты", a warm and slightly silly friend: "Какое у тебя сегодня настроение?", not "Выберите параметры". Buttons name the action ("Сохранить", not "Отправить"); empty states and errors are an invitation to act in the interface's voice, no apologies. Humor is welcome, condescension is not.

**Quality floor** (unannounced): responsive down to mobile, visible keyboard focus, WCAG-AA contrast for text on every accent in both themes, `prefers-reduced-motion` respected.

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
