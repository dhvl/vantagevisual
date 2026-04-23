---
name: analyzing-landing-pages
description: Analyzes landing pages for conversion rate optimization (CRO), content quality, and technical performance. Use when the user wants to audit a landing page, improve conversion rates, get feedback on design and messaging, or ensure mobile responsiveness. This skill should be used whenever a landing page URL or design is mentioned for evaluation, even if the user doesn't explicitly ask for an "audit."
---

# Landing Page Analytics

A specialized skill for auditing landing pages based on conversion best practices, UX principles, and technical performance.

## When to use this skill
- When a user provides a landing page URL for feedback.
- When designing or refactoring a landing page for better conversion.
- When troubleshooting high bounce rates or low conversion rates.
- When performing a competitive analysis of landing pages.

## Workflow
- [ ] **Probe for Input**: If the user hasn't provided a landing page URL, screenshot, or code, **stop and ask for it** before proceeding.
- [ ] **Define Goal**: Identify the primary conversion goal (e.g., signup, purchase).
- [ ] **Message Match**: Verify if the headline aligns with the intended traffic source.
- [ ] **Above-the-Fold Audit**: Check for a clear value proposition and CTA in the initial view.
- [ ] **Trust & Credibility**: Evaluate the presence of social proof (testimonials, logos).
- [ ] **Technical Check**: Measure load speed and mobile responsiveness.
- [ ] **Friction Analysis**: Identify distractions or unnecessary form fields.
- [ ] **Final Report**: Generate a prioritized list of improvements.

## Instructions

### 0. Input Validation (Probing)
- **CRITICAL**: Do NOT attempt to analyze a generic page unless the user explicitly asks for "generic best practices."
- If no specific landing page is provided, respond with: "I'd love to help you optimize your landing page! Since I don't see a URL or design yet, could you please provide the link or share a screenshot of the page you'd like me to analyze?"
- Only proceed to the audit once you have a specific target.

### 1. Headline & Value Proposition
- Does the headline clearly explain WHAT the product/service is and WHO it is for?
- Is there a subheadline that addresses a specific pain point?
- Goal: Immediate clarity within 3-5 seconds of landing.

### 2. Call to Action (CTA)
- Is there ONE primary CTA that stands out visually?
- Does the button text use action-oriented and personalized language (e.g., "Start My Trial" vs "Submit")?
- Is the CTA placed above the fold and repeated strategically on long pages?

### 3. Trust Signals
- Look for authentic customer testimonials with names/photos.
- Check for trust badges (security, industry awards, partner logos).
- Ensure the privacy policy and terms are accessible but not distracting.

### 4. Visual Hierarchy & UX
- Is there enough white space to guide the eye?
- Is the most important information the most prominent?
- Remove navigation menus if they distract from the conversion goal.

### 5. Mobile & Performance
- Use `lighthouse` or similar tools to check performance scores.
- Manually inspect the mobile layout for readability and button sizes.
- Ensure forms are easy to fill on small screens (autofill, large inputs).

## Resources
- [Audit Checklist](resources/checklist.md)
- [Example Audit Report](examples/sample_report.md)
- [Performance Check Script](scripts/check_perf.py)
