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

**Concept: "Companion-led warmth".** AniFriend's personality is a slightly goofy, emotional anime guide — a friend who pulls faces, cheers you on, and hands you anime that match your mood. The product gives the user warmth, fun, and a little silliness so they can switch off and feel something. **Style keywords: energetic, fun, playful, modern** — always carrying anime + comedy/humor in the copy and micro-interactions. Tone: bright, genki — never tiring.

**Color is allowed to be bold.** The palette is intentionally bright and multicolor — pink, green, yellow — not a single trendy accent. The one hard rule that stays is **readability**: text must keep its contrast on every accent (see Quality floor). "Garish" is avoided by tuning chroma and text contrast, not by banning color.

**Don't default.** Avoid the stock AI looks: cream + serif + terracotta; near-black + one acid accent; broadsheet hairlines. Our warmth comes from a curated multicolor anime palette + an expressive character, not from a single trendy accent.

**Themes — light & dark (MVP).** Two brightnesses now: light (contrasty pink-grey canvas + white cards) and dark (near-black). `next-themes` (`attribute="class"`, system default) drives it via `ModeToggle`. The richer **mood-driven colorways** (each mood repainting the whole surface) are **deferred to a future "custom themes" feature** — see root `CLAUDE.md` roadmap.

**Color** — one bold, playful multicolor palette; light & dark share the accents (defined in `app/globals.css`):
- Primary `oklch(0.58 0.21 3)` — deep raspberry-pink for CTAs with **white text** (4.8:1, passes AA; the brighter `0.686` looked nicer but failed white-on-pink at 3.1:1).
- Secondary `oklch(0.808 0.240 136)` — genki green · Accent `oklch(0.838 0.171 83)` — sunny yellow.
- Light: canvas `oklch(0.971 0.014 343)` (soft pink-grey) + white cards + dark-plum ink `oklch(0.257 0.086 281)`. Dark: near-black `oklch(0.170 0.006 286)` + light ink.
- Focus ring = primary; soft pink shadows; `radius: 1rem` (rounded, friendly).

**Type** — Latin + Cyrillic (critical for the CIS audience; Cyrillic must be in `subsets`):
- **Nunito** — body / UI; rounded, friendly grotesque.
- **Fira Code** — utility: data and labels ("92% match", episodes, ratings).
- Deferred brand layers: a display face and a handwritten **companion voice** font — add when the companion/custom-theme work lands.

**Layout** — a conversational vertical flow, not a dense catalog grid. The hero is a warm question from the guide leading into the survey, not a generic value-prop block. Recommendation cards read as a "note from a friend" with the AI's "why this fits you" reasoning, not a metadata row.

**Signature — a companion that arrives in layers.** The personality ships before its body does:
1. **Voice & color first** (MVP) — handwritten popups, bright multicolor, playful hover micro-interactions.
2. **Embodied chibi later** — once the conversational-AI layer is live (it shares that AI plumbing): an interactive chibi guide that reacts to hovers, pulls faces, and drops the occasional text bubble. It becomes the brand's one memorable, embodied element. Roadmap lives in root `CLAUDE.md`.

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
