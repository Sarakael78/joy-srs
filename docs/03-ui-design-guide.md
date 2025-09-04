# UI Style Guide for Project Precedent

This guide codifies the design decisions made for the "dark mode" aesthetic of the application. It's intended for future UI developers to ensure consistency, maintainability, and a high-quality user experience as the project evolves.

---

## 1. Design Philosophy 🏛️

The **Project Precedent** UI is built on three core principles:

- **Clarity:** The interface must be immediately understandable. Visual hierarchy should guide the user to the most important information without distraction.
- **Professionalism:** The aesthetic is modern, clean, and serious, reflecting the strategic nature of the content. It's designed to build trust and convey authority.
- **Focus:** The dark theme is used intentionally to reduce visual noise, lessen eye strain during extended use, and make key data points—like metrics and strategic highlights—stand out vividly.

---

## 2. Colour Palette 🎨

The palette is minimal and high-contrast, built around a core of deep neutrals and a single, powerful primary action colour.

### Primary Colours

These are the main brand and action colours.

- **Strategic Green**
  - **HEX:** `#41824A`
  - **Use:** Primary calls-to-action (buttons), active states (tabs), highlights, and key conclusions. It signifies positive progression and success.
- **Accent Blue**
  - **HEX:** `#60a5fa` (Tailwind: `blue-400`)
  - **Use:** Exclusively for gradient text effects in combination with Strategic Green to add visual flair to major headings.

### Neutral Palette (Surfaces & Text)

These colours form the backbone of the UI, creating a layered and legible dark mode experience.

- **Base Background**
  - **HEX:** `#1E293B` (Tailwind: `slate-800`)
  - **Use:** The main background colour for all pages.
- **Surface Background**
  - **HEX:** `#334155` (Tailwind: `slate-700`)
  - **Use:** For primary content containers and cards to lift them off the base background. Also used for dropdown menus.
- **Text & Borders**
  - **Heading Text:** `#F1F5F9` (Tailwind: `slate-100`) - For all major headings.
  - **Body Text:** `#94A3B8` (Tailwind: `slate-400`) - For paragraph text and secondary information.
  - **Borders:** `#475569` (Tailwind: `slate-600`) - For separating components and defining card edges.

### Semantic Colours

Used for providing contextual feedback to the user (e.g., risk levels, alerts).

- **Success / Low Risk:** `#22C55E` (Tailwind: `green-500`)
- **Warning / Medium Risk:** `#FBBF24` (Tailwind: `amber-400`)
- **Error / High Risk:** `#F87171` (Tailwind: `red-400`)

---

## 3. Typography ✒️

Consistent typography is crucial for readability and a professional appearance.

- **Font Family:** **Inter** is used for all UI text, headings, and body copy. It should be sourced from Google Fonts.
- **Weights:**
  - **Normal:** 400
  - **Semibold:** 600
  - **Bold:** 700
  - **Extra Bold:** 800
- **Scale & Usage:**
  - **Hero Title (`<h1>`):** `text-4xl` to `text-6xl`, `font-extrabold`, `text-slate-100`. Used for the main page title.
  - **Section Title (`<h2>`):** `text-3xl` to `text-4xl`, `font-bold`, `gradient-text`. Used for major section headings.
  - **Card Title (`<h3>`):** `text-xl` to `text-2xl`, `font-bold`, `text-slate-100`. Used for titles within components.
  - **Body (`<p>`):** `text-base` or `text-lg`, `font-normal`, `text-slate-400`.
  - **Labels & UI Text:** `text-sm`, `font-medium`, `text-slate-300`.

---

## 4. Layout & Spacing 📏

A consistent spacing system ensures a balanced and organised layout.

- **Base Unit:** **4px**. All padding, margins, and gaps should be multiples of this unit.
- **Standard Gaps:** Use `gap-4` (16px), `gap-6` (24px), and `gap-8` (32px) for component spacing.
- **Card Padding:** All cards and primary containers should use a standard padding of `p-6` (24px) or `p-8` (32px).
- **Container Width:** The main content container should have a `max-w-7xl` and be centered with `mx-auto`.

---

## 5. Core Components 🧱

These are the reusable building blocks of the interface.

### Buttons

- **Primary Action (Sign In):**
  - **Background:** `bg-[#41824A]`
  - **Text:** `text-white`, `font-semibold`
  - **Hover:** `bg-green-500`, `scale-105` transform
  - **Focus:** Visible outline ring (`focus:ring-green-400`)
- **Tabs (Active):**
  - **Background:** `bg-[#41824A]`
  - **Text:** `text-white`, `font-bold`
- **Tabs (Inactive):**
  - **Background:** Transparent
  - **Text:** `text-gray-300`, `font-bold`
  - **Hover:** `bg-slate-700`

### Form Inputs

- **Background:** `bg-slate-700/50`
- **Text:** `text-white`
- **Placeholder:** `placeholder-gray-400`
- **Border:** `border-slate-600`
- **Focus State:** `ring-2`, `ring-[#41824A]`, `border-[#41824A]`

### Cards & Surfaces

- **Background:** `bg-slate-800` or a semi-transparent `bg-slate-800/20` for glassmorphism effect.
- **Border:** `border`, `border-slate-700` (or `border-white/10` on glassmorphism).
- **Rounding:** `rounded-2xl` for large cards, `rounded-xl` for smaller ones.
- **Shadow:** `shadow-xl` or `shadow-2xl`.

---

## 6. Accessibility (A11Y) ♿

Creating an accessible experience is non-negotiable.

- **Contrast:** Ensure all text meets **WCAG AA** contrast ratios against its background. The chosen palette is designed with this in mind.
- **Semantics:** Use proper semantic HTML (`<nav>`, `<main>`, `<button>`, etc.) to support screen readers.
- **Focus States:** All interactive elements (buttons, links, inputs) **must** have a clear and visible focus state.
- **Labels:** All form inputs must have an associated `<label>`.
