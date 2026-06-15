---
category: system
type: resource
topic: [PRD, Product, Specification]
status: active
industry: Technology
created: 2026-06-03
---

> [!IMPORTANT] Key Takeaway
> **Why this matters:** This PRD defines the core architectural and functional requirements for the personal synthesis platform (PM + Composer).
> **How to use it:** Use as the source of truth for technical implementation and feature prioritization.
> **Informs:** Website development and portfolio presentation.

# PRD — Personal Blog & Portfolio Website
**Owner:** Seungjo Han (한승조)
**Version:** 4.1
**Updated:** May 25, 2026
**Status:** Actively Iterating

---

## 1. Purpose & Goals

A personal website serving three functions simultaneously:

1. **Identity** — First-impression page for recruiters, collaborators, and contacts. Name, role, keyword badges, bio bullets, and direct contact links.
2. **Portfolio** — Selected work presented as one-column project cards on the listing page (Impact / What I Did / Outcome), linking to full 6-section case studies on the detail page.
3. **Blog** — Long-form essays organized by tag and grouped into curated *Magazine* series. Writing-first, distraction-free reading experience.

### Explicit Non-Goals (v1)

| Out of scope | Reason |
|---|---|
| CMS or database backend | All content is static TypeScript data files |
| Authentication / gated content | Not needed for this phase |
| Real email capture | No backend |
| Analytics | Planned for v2 |
| Server-side rendering | SPA is sufficient |
| Comment system | Removed in v2.1 |

---

## 2. Tech Stack

| Layer | Package | Notes |
|---|---|---|
| Build tool | `vite` | Dev server + production bundler. No SSR. |
| UI library | `react` 18 | StrictMode enabled in `main.tsx` |
| Language | `typescript` 5.x | Strict mode. No `any` in production code. |
| Routing | `react-router` 7.x | Data Mode. `createBrowserRouter`. **NOT** `react-router-dom`. |
| Styling | Tailwind CSS v4 | CSS-first config. No `tailwind.config.js`. Tokens in `/src/styles/theme.css`. |
| Animation | `motion` | Import from `motion/react` subpath: `import { motion } from 'motion/react'`. |
| Icons | `lucide-react` | 1px stroke, 24px base. Tree-shakeable. |
| Toast | `sonner` | `import { toast } from 'sonner'`. `<Toaster>` lives in `Layout.tsx`. |
| Fonts | CSS ` @import` | Declared in `/src/styles/fonts.css` (top of file only). System stack fallback. |

---

## 3. File Structure

```
/
├── PRD.md
├── package.json
└── src/
    ├── main.tsx
    ├── app/
    │   ├── App.tsx                          ← Root; renders <RouterProvider router={router} />
    │   ├── routes.tsx                       ← createBrowserRouter config
    │   ├── components/
    │   │   ├── Layout.tsx                   ← Persistent shell: header + footer + toaster + search
    │   │   ├── SearchModal.tsx              ← Full-screen Cmd+K search overlay
    │   │   ├── AnchorNav.tsx                ← Sticky in-page section nav (blog + projects)
    │   │   └── figma/
    │   │       └── ImageWithFallback.tsx    ← PROTECTED — do not create or modify
    │   ├── pages/
    │   │   ├── Home.tsx                     ← /
    │   │   ├── About.tsx                    ← /about
    │   │   ├── Projects.tsx                 ← /projects
    │   │   ├── ProjectCase.tsx              ← /projects/:slug
    │   │   ├── Blog.tsx                     ← /blog
    │   │   ├── BlogPost.tsx                 ← /blog/:slug
    │   │   └── MagazineDetail.tsx           ← /magazine/:slug
    │   └── data/
    │       ├── posts.ts                     ← Post[]
    │       ├── projects.ts                  ← Project[]
    │       └── magazines.ts                 ← Magazine[]
    └── styles/
        ├── theme.css                        ← CSS custom properties / design tokens
        └── fonts.css                        ← @gstack/browse/src/cookie-import-browser.ts declarations (top of file only)
```

---

## 4. Routing

**Config file:** `src/app/routes.tsx`
**Pattern:** React Router v7 Data Mode — `createBrowserRouter`

```ts
createBrowserRouter([
  {
    path: '/',
    Component: Layout,
    children: [
      { index: true,              Component: Home },
      { path: 'about',            Component: About },
      { path: 'blog',             Component: Blog },
      { path: 'blog/:slug',       Component: BlogPost },
      { path: 'projects',         Component: Projects },
      { path: 'projects/:slug',   Component: ProjectCase },
      { path: 'magazine/:slug',   Component: MagazineDetail },
    ],
  },
]);
```

---

## 5. Data Models

### 5.1 `Post` — `src/app/data/posts.ts`

```ts
interface Post {
  slug: string;        // URL-safe kebab-case. Must be unique.
  title: string;
  subtitle: string;    // One-sentence hook. Shown under title on post page.
  date: string;        // Human-readable: "April 15, 2026". Parsed by formatDate().
  readTime: string;    // Present in data but NOT displayed (removed in v2.1).
  tags: string[];      // Used for /blog?tag= link filtering, related post scoring.
  excerpt: string;     // 1–2 sentences. Blog listing rows, PostCard previews, home feed.
  coverImage?: string; // Unsplash URL. Article header and PostCard thumbnail.
}
```

---

## 13. Changelog

| Version | Date | Changes |
|---|---|---|
| 4.1 | May 25, 2026 | Real portfolio projects added; Dokdo post added; "What I Bring" grid update. |

## 🔗 Connections
- [[../index|Master Index]]
- [[Personal Blog & Portfolio]]
