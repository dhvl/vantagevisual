---
name: lighthouse-audit
description: Runs a Google Lighthouse audit on ANY web URL — local (localhost) or live (any https:// domain) — analyses the results, and applies code fixes to the project when source files are available. Use this skill whenever the user mentions: page load speed, performance score, Lighthouse, Core Web Vitals (LCP, CLS, FID, INP, TBT, FCP, TTFB), slow website, low performance score, images not optimised, missing meta tags, accessibility issues, or any request to "optimise", "speed up", or "audit" a website — local or live. Trigger even for vague phrases like "make my site faster", "check the performance of my site", "can you run lighthouse on this URL", or when a user pastes a URL and asks about speed or performance.
---

# Lighthouse Audit & Performance Upgrade Skill

Runs a Lighthouse audit against **any URL** — local dev server or live production domain — parses the findings, and applies code fixes when source files are reachable.

---

## Step 0 — Determine Mode

First, classify the URL the user gives you. This determines which steps to run.

| URL type | Example | Mode |
|---|---|---|
| Local dev server | `http://localhost:3000` | **Local** — audit + code fixes |
| Local production build | `http://localhost:4000` | **Local** — audit + code fixes |
| Live site (https) | `https://my-site.vercel.app` | **Live** — audit + recommendations report |
| Any other http/https URL | `https://competitor.com` | **Live** — audit + recommendations report |

**Local mode**: You have access to the source code, so apply fixes directly and re-audit.

**Live mode**: You are auditing a deployed site. You cannot edit its source directly. Produce a detailed recommendations report. If the user also tells you the local project root, offer to apply the fixes there so they can redeploy.

Ask the user for:
1. The URL to audit (or use the one they provided)
2. *(Live mode only)* — Is there a local project root you can edit? If yes, where?

---

## Step 1 — Run the Lighthouse Audit

Install the CLI if not present:
```bash
npx lighthouse --version 2>/dev/null || npm install -g lighthouse
```

Run the audit (works for **any** URL — local or live):
```bash
npx lighthouse <URL> \
  --output json \
  --output-path /tmp/lh-report.json \
  --chrome-flags="--headless --no-sandbox --disable-gpu" \
  --only-categories=performance,accessibility,best-practices,seo \
  --quiet
```

**Tips for live URLs:**
- Live audits reflect real CDN, caching, and server response time — often more accurate than local.
- If the site requires authentication (login wall), note this to the user — Lighthouse can't audit gated pages without a session cookie.
- If the URL redirects (e.g. `http://` → `https://`), use the final URL directly.

**Tips for local URLs:**
- Prefer a production build (`npm run build && npm start`) over `npm run dev` — dev mode disables optimisations and inflates bundle sizes. If the user is on dev, note the caveat.
- If the local server isn't running, ask the user to start it first.

Then parse the output:
```bash
python <skill-dir>/scripts/parse_lh_report.py /tmp/lh-report.json
```

---

## Step 2 — Parse and Prioritise Results

Read `/tmp/lh-report.json` and extract:

```
scores:
  performance: .categories.performance.score × 100
  accessibility: .categories.accessibility.score × 100
  best-practices: .categories["best-practices"].score × 100
  seo: .categories.seo.score × 100

failing audits (score < 0.9):
  for each audit in .audits where .score != null and .score < 0.9:
    - id, title, description, score, displayValue, details
```

Group by impact tier:
- 🔴 **Critical** (score < 0.5) — must fix
- 🟡 **Warning** (0.5 ≤ score < 0.9) — should fix
- 🟢 **Pass** (score ≥ 0.9) — skip

Print a clear prioritised summary **before** making any code changes.

---

## Step 3 — Apply Fixes (Local mode) or Write Recommendations (Live mode)

### 🖥 Local Mode — Apply code fixes directly

Read `references/nextjs-perf-fixes.md` for detailed patterns. Quick reference:

| Lighthouse Audit ID | What to fix |
|---|---|
| `render-blocking-resources` | Move scripts to `<Script strategy="lazyOnload">`, defer non-critical CSS |
| `uses-optimized-images` / `uses-webp-images` | Replace `<img>` with `next/image`, add `quality={80}` |
| `uses-responsive-images` | Add `sizes` prop to `next/image` |
| `unminified-javascript` / `unminified-css` | Ensure production build; add `compress: true` to `next.config.ts` |
| `unused-javascript` | Add dynamic imports (`next/dynamic`) for heavy components |
| `uses-long-cache-ttl` | Add `Cache-Control` headers via `next.config.ts headers()` |
| `dom-size` | Paginate or virtualise large lists |
| `largest-contentful-paint-element` | Add `priority` prop to hero image |
| `cumulative-layout-shift` | Set explicit `width`/`height` on all images and embeds |
| `total-blocking-time` | Debounce heavy handlers; lazy-load non-critical scripts |
| `color-contrast` | Fix text/background pairs to meet WCAG AA (4.5:1 ratio) |
| `meta-description` | Add `<meta name="description">` |
| `document-title` | Add unique `<title>` per page |
| `image-alt` | Add meaningful `alt` text to all images |
| `link-name` | Add `aria-label` to icon-only buttons/links |
| `heading-order` | Fix h1 → h2 → h3 hierarchy |
| `tap-targets` | Ensure interactive elements are at least 44×44 px |
| `no-vulnerable-libraries` | Run `npm audit fix` |

Apply fixes one audit group at a time. After each batch run `npx tsc --noEmit` to verify no new TypeScript errors.

### 🌐 Live Mode — Recommendations report

When source code is not available (or the user hasn't provided a project root), produce a structured report instead of making edits:

```
## Lighthouse Audit — [URL]
Audited: [date/time]

### Scores
| Category       | Score |
|----------------|-------|
| Performance    |  xx   |
| Accessibility  |  xx   |
| Best Practices |  xx   |
| SEO            |  xx   |

### Recommended Fixes (by priority)
#### 🔴 Critical
- **[Audit title]** — [what to change, with specific code/config example]
  Lighthouse ID: `[audit-id]` | Estimated impact: [LCP / CLS / TBT etc.]

#### 🟡 Warnings
- ...

### Key Metrics
| Metric | Value  |
|--------|--------|
| LCP    |        |
| TBT    |        |
| CLS    |        |
| FCP    |        |
| TTFB   |        |

### Deploy-only improvements
These require server/CDN config changes, not code changes:
- [cache headers, HTTP/2, compression, etc.]
```

If the user then provides their local project root, pivot to Local mode and apply the fixes code-side.

---

## Step 4 — Re-run the Audit (Local mode only)

After applying fixes, re-audit the same URL:

```bash
npx lighthouse <URL> \
  --output json \
  --output-path /tmp/lh-report-after.json \
  --chrome-flags="--headless --no-sandbox --disable-gpu" \
  --only-categories=performance,accessibility,best-practices,seo \
  --quiet

python <skill-dir>/scripts/parse_lh_report.py /tmp/lh-report.json \
  --compare /tmp/lh-report-after.json
```

If a score regressed, investigate and revert that specific change.

---

## Step 5 — Final Summary

Present this structure at the end (both modes):

```
## Lighthouse Audit Results — [URL]

### Score Comparison
| Category       | Before | After | Delta |
|----------------|--------|-------|-------|
| Performance    |   xx   |  xx   |  +xx  |
| Accessibility  |   xx   |  xx   |  +xx  |
| Best Practices |   xx   |  xx   |  +xx  |
| SEO            |   xx   |  xx   |  +xx  |

(Live mode: show "Before" only with a "Recommended" column)

### Fixes Applied / Recommended
- [fix]: [what was changed and why it helps]

### Remaining Issues
- [issue]: [reason not addressed — e.g., needs server config, authenticated page]

### Key Metrics
| Metric | Before | After |
|--------|--------|-------|
| LCP    |        |       |
| TBT    |        |       |
| CLS    |        |       |
| FCP    |        |       |
```

---

## Important notes

- This skill works on **any URL** — localhost, staging, or production.
- For **live URLs without a codebase**: produce a recommendation report; don't make up fixes you can't verify.
- Live Lighthouse scores can vary run-to-run due to network conditions. If scores look unexpectedly low, mention this.
- Some audits (`uses-long-cache-ttl`, `uses-http2`) require server/CDN config — note these as deploy-only fixes.
- For Next.js projects, read `references/nextjs-perf-fixes.md` before making changes.
- Never modify a file without reading its current content first.
- After all code changes, run the TypeScript compiler check: `npx tsc --noEmit`.
