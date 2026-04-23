# Next.js Performance Fix Reference

This reference covers concrete code changes for common Lighthouse findings in Next.js (App Router + Pages Router) projects.

---

## Table of Contents
1. [Images](#images)
2. [JavaScript Bundle](#javascript-bundle)
3. [Fonts](#fonts)
4. [Render-Blocking Resources](#render-blocking-resources)
5. [Caching](#caching)
6. [Core Web Vitals](#core-web-vitals)
7. [SEO & Metadata](#seo--metadata)
8. [Accessibility](#accessibility)
9. [next.config fixes](#nextconfig-fixes)

---

## Images

### Replace `<img>` with `next/image`

```tsx
// ❌ before
<img src="/hero.jpg" alt="Hero" />

// ✅ after (for known dimensions)
import Image from 'next/image';
<Image src="/hero.jpg" alt="Hero" width={1200} height={600} quality={80} />

// ✅ after (fill mode for fluid containers)
<div style={{ position: 'relative', width: '100%', height: '400px' }}>
  <Image src="/hero.jpg" alt="Hero" fill style={{ objectFit: 'cover' }} />
</div>
```

### Add `priority` to LCP image
The largest above-the-fold image should never be lazy-loaded:
```tsx
<Image src="/hero.jpg" alt="Hero" width={1200} height={600} priority />
```

### Set `sizes` for responsive images
```tsx
<Image
  src="/card.jpg"
  alt="Card"
  width={400}
  height={300}
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
/>
```

### External SVG logos — use `<img>` not `next/image`
For external SVG files (e.g., Wikipedia logos), `next/image` struggles with SVG optimization. Use a plain  `<img>` with `loading="lazy"` instead:
```tsx
// eslint-disable-next-line @next/next/no-img-element
<img src={c.url} alt={c.name} className="h-7 w-auto" loading="lazy" />
```

---

## JavaScript Bundle

### Dynamic import for heavy/below-fold components
```tsx
import dynamic from 'next/dynamic';

// Component loaded only when needed
const HeavyChart = dynamic(() => import('../components/HeavyChart'), {
  loading: () => <p>Loading chart…</p>,
  ssr: false, // set false for browser-only libraries
});
```

### Tree-shake lodash / date-fns
```ts
// ❌ imports entire library
import _ from 'lodash';

// ✅ import only what you need
import debounce from 'lodash/debounce';
```

### Analyse bundle size
```bash
ANALYZE=true npm run build
# Requires: npm install @next/bundle-analyzer
```

Add to `next.config.ts`:
```ts
import withBundleAnalyzer from '@next/bundle-analyzer';
export default withBundleAnalyzer({ enabled: process.env.ANALYZE === 'true' })({
  // ...your config
});
```

---

## Fonts

### Use `next/font` instead of Google Fonts CSS imports

```tsx
// ❌ globals.css — causes render-blocking network request
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');

// ✅ layout.tsx — zero layout shift, no external request
import { Inter } from 'next/font/google';
const inter = Inter({ subsets: ['latin'], display: 'swap' });

export default function RootLayout({ children }) {
  return <html className={inter.className}>{children}</html>;
}
```

---

## Render-Blocking Resources

### Third-party scripts
```tsx
import Script from 'next/script';

// ❌ blocks parsing
<script src="https://analytics.example.com/a.js" />

// ✅ deferred — load after page is interactive
<Script src="https://analytics.example.com/a.js" strategy="lazyOnload" />

// ✅ afterInteractive — load after hydration (good for analytics)
<Script src="https://analytics.example.com/a.js" strategy="afterInteractive" />
```

### Inline critical CSS, defer the rest
Next.js automatically inlines critical CSS in production. Ensure your custom CSS isn't loaded via a `<link>` tag inside components — import it at module level instead:
```tsx
// ✅ module-level import (extracted & inlined by Next.js build)
import './Hero.module.css';
```

---

## Caching

### Add Cache-Control headers in `next.config.ts`
```ts
const nextConfig = {
  async headers() {
    return [
      {
        source: '/_next/static/(.*)',
        headers: [{ key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }],
      },
      {
        source: '/fonts/(.*)',
        headers: [{ key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }],
      },
      {
        source: '/(.*)',
        headers: [{ key: 'Cache-Control', value: 'public, max-age=3600, stale-while-revalidate=86400' }],
      },
    ];
  },
};
```

---

## Core Web Vitals

### Fix Cumulative Layout Shift (CLS)
Every image and video must have explicit dimensions to prevent layout shift:
```tsx
<Image src="/hero.jpg" alt="" width={800} height={400} />
// Don't rely on intrinsic dimensions for externally loaded images
```

Reserve space for dynamic content (e.g., ad slots, iframes):
```css
.ad-container {
  min-height: 250px; /* reserve space before content loads */
}
```

### Fix Largest Contentful Paint (LCP)
- Add `priority` to the hero image.
- Preconnect to image CDNs:
  ```html
  <link rel="preconnect" href="https://cdn.example.com" />
  ```
- Use `next/image` with a local image for guaranteed fast delivery.

### Fix Total Blocking Time (TBT) / Interaction to Next Paint (INP)
- Move heavy computations off the main thread using a Web Worker.
- Replace synchronous event handlers with debounced ones:
  ```ts
  import debounce from 'lodash/debounce';
  const handleSearch = debounce((q) => search(q), 300);
  ```
- Split long `useEffect` work into smaller async chunks with `setTimeout(..., 0)`.

---

## SEO & Metadata

### App Router (`app/layout.tsx` or `app/page.tsx`)
```tsx
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Page Title | Site Name',
  description: 'Compelling 150-160 char meta description for the page.',
  openGraph: {
    title: 'Page Title',
    description: 'OG description',
    images: [{ url: '/og-image.png', width: 1200, height: 630 }],
  },
};
```

### Pages Router (`pages/_document.tsx`)
```tsx
import Head from 'next/head';
<Head>
  <title>Page Title | Site Name</title>
  <meta name="description" content="150-160 char description." />
</Head>
```

### Structured Data (JSON-LD)
```tsx
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{
    __html: JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'Course',
      name: 'Data Science Certification',
      provider: { '@type': 'Organization', name: 'AnalytixLabs' },
    }),
  }}
/>
```

---

## Accessibility

### Colour contrast
Text must meet WCAG AA — 4.5:1 for normal text, 3:1 for large text (≥18pt or ≥14pt bold).

Quick check: use a contrast ratio tool or run `axe-core` via:
```bash
npx axe http://localhost:3000 --stdout
```

Common fixes:
```css
/* ❌ low contrast */
color: #9BBAC0; /* on white bg = ~2.5:1 */

/* ✅ adjusted */
color: #5D7A84; /* on white bg = ~4.6:1 */
```

### Image alt text
```tsx
// ❌ missing alt
<Image src="/logo.png" width={180} height={40} />

// ✅ descriptive alt
<Image src="/logo.png" alt="AnalytixLabs logo" width={180} height={40} />

// ✅ decorative image (intentionally empty alt)
<Image src="/divider.svg" alt="" width={100} height={2} aria-hidden="true" />
```

### ARIA labels for icon-only links
```tsx
// ❌
<a href="tel:9555525908"><PhoneIcon /></a>

// ✅
<a href="tel:9555525908" aria-label="Call us at 9555525908"><PhoneIcon /></a>
```

### Heading hierarchy
```html
<!-- ❌ jumps from h1 to h3 -->
<h1>Course Title</h1>
<h3>Module 1</h3>

<!-- ✅ correct hierarchy -->
<h1>Course Title</h1>
<h2>Module 1</h2>
```

### Touch target sizes
Interactive elements must be at least 44×44 CSS pixels:
```css
button, a {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 16px;
}
```

---

## next.config fixes

```ts
const nextConfig: NextConfig = {
  compress: true,              // Enable gzip compression
  poweredByHeader: false,     // Remove X-Powered-By header (security)
  reactStrictMode: true,       // Catch potential issues early
  images: {
    formats: ['image/avif', 'image/webp'],  // Serve modern formats
    minimumCacheTTL: 86400,                 // Cache optimised images 24h
    deviceSizes: [640, 750, 828, 1080, 1200, 1920],
    imageSizes: [16, 32, 48, 64, 96, 128, 256],
    remotePatterns: [
      // ... your patterns
    ],
  },
  experimental: {
    optimizeCss: true,   // Inline critical CSS (requires critters)
  },
};
```
