---
type: resource
topic: [Design, System, UI/UX]
status: active
industry: Technology
created: 2026-06-03
---

# DESIGN.md — Seungjo Han Personal Website
**Owner:** Seungjo Han (한승조)
**Version:** 1.0
**Updated:** June 3, 2026

---

## 1. Design Philosophy

**Editorial minimalism.** The site is built like a high-quality print publication — white space is deliberate, type does the heavy lifting, and every element earns its place. No decorative gradients, shadows, or illustrations. Color is used only for meaning, not decoration.

Three principles govern every decision:

| Principle | Meaning |
|---|---|
| **Clarity first** | Information hierarchy is always obvious. The reader never has to guess what something is. |
| **Typographic restraint** | Weight, size, and spacing carry meaning. Bold and color are reserved for true emphasis. |
| **Calm interaction** | Animations are subtle and fast. Nothing bounces, pulses, or demands attention. |

---

## 2. Color System

All colors are Tailwind CSS utility classes. No custom hex values in component code.

### Base Palette

| Role | Tailwind | Usage |
|---|---|---|
| Page background | `bg-white` | All page backgrounds |
| Primary text | `text-gray-900` | Headings, titles, strong values |
| Body text | `text-gray-700` | Prose paragraphs, card body |
| Muted text | `text-gray-500` | Subtitles, excerpts, descriptions |
| Label / meta | `text-gray-400` | Dates, section labels, meta info |
| Borders | `border-gray-100` | All dividers and card outlines |
| Accent | `bg-black text-white` | Primary CTA buttons only |

---

## 3. Typography

> **Never use Tailwind text-size classes** (`text-xl`, `text-2xl`, etc.) for headings or body. Use inline `style={{ fontSize: '...' }}` for precise control.

---

## 4. Spacing & Layout

### Page Widths

| Context | Max width | Class |
|---|---|---|
| Projects page | 4xl | `max-w-4xl` |
| Blog listing | 3xl | `max-w-3xl` |
| Blog post article | 48rem | `max-w-[48rem]` |

---

## 5. Component Patterns

(Refer to component files for specific styles.)

---

## 8. Animation

All animation uses `motion/react`.

### Entry Animation (on mount)

```ts
initial={{ opacity: 0, y: 20 }}
animate={{ opacity: 1, y: 0 }}
transition={{ duration: 0.7–0.8, ease: [0.22, 1, 0.36, 1] }}
```
