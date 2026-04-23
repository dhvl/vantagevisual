---
name: seo-expert
description: Highly resourceful SEO expert specialized in automating search engine optimization for Next.js 14/15 applications hosted on Vercel. Use this skill when the user wants to improve search visibility, indexability, metadata, sitemaps, robots.txt, or structured data (JSON-LD). Proactively audit the code for SEO gaps and implement best-in-class optimizations using the modern Next.js App Router Metadata API.
---

# SEO Expert

This skill automates the end-to-end technical SEO process for Next.js projects, ensuring they rank better and appear with rich snippets in search results.

## Performance Principles
- **Modern Standards**: Prioritize the Next.js `Metadata` API over manual `<head>` tags.
- **Dynamic indexing**: Automate sitemaps and robots.txt using file-baseed conventions (`sitemap.ts`, `robots.ts`).
- **Rich Presence**: Implement JSON-LD for Organization, Website, and Breadcrumbs.
- **Proactive Auditing**: Search for missing alt tags, duplicate H1s, and missing meta descriptions.

## SEO Automation Workflow

### 1. Project Audit
Search the codebase to identify existing SEO implementation.
- Check `layout.tsx` for global metadata.
- Check for `sitemap.ts` and `robots.ts`.
- Check for accessibility/SEO issues in components (alt tags, semantic HTML).

### 2. Global Metadata Implementation
Implement a robust global metadata object in the root `app/layout.tsx`.
- **Title Template**: Use `%s | Brand Name` for dynamic page titles.
- **Open Graph**: Setup default image, site name, and locale.
- **Twitter**: High-impact large summary cards.

### 3. Sitemaps & Robots.txt
Create or update technical files at the root of `app/`:
- **sitemap.ts**: Dynamically list all static and dynamic routes.
- **robots.ts**: Define crawl rules and link to the sitemap.

### 4. Structured Data (JSON-LD)
Generate and embed JSON-LD scripts for key pages:
- **Organization**: Brand details, logo, contact points.
- **Breadcrumbs**: For better URL display in SERPs.

### 5. Page-Specific Optimization
Use `generateMetadata` for dynamic routes to ensure unique titles and descriptions based on content.

## Helper Scripts
Use the bundled scripts in `./scripts/` for automated verification and generation:
- `seo_audit.py`: Scans files for missing tags.
- `generate_schema.py`: Helps create valid JSON-LD objects.

## Success Criteria
- [ ] Validated `sitemap.xml` and `robots.txt` endpoints work on `localhost`.
- [ ] Metadata is visible in the rendered page source.
- [ ] No missing `alt` tags in prominent images.
- [ ] Structured data passes Google's Rich Results Test logic.
