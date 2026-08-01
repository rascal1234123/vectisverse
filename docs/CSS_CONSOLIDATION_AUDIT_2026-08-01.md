# VectisVerse CSS Consolidation Audit — 1 August 2026

## Purpose

Prepare a controlled path toward simpler stylesheet loading without redesigning the website or altering the established static Cloudflare build.

## Current standard-page cascade

The standard VectisVerse pages currently depend on this order:

1. `assets/css/site.css`
2. `assets/css/approved-layout-fixes.css`
3. `assets/css/riptide-logo-fix.css`
4. `assets/css/ftw-hero-v2.css`
5. `assets/css/visual-refinements-v1.css`, injected by `assets/js/site.js`

The later files intentionally override earlier rules. Removing or reordering them without rendered comparison could change hero composition, panel framing, navigation, accessibility targets, promotional modules, Contact sizing or responsive behaviour.

## Current Concepts cascade

The Vectis Concepts page currently depends on this order:

1. `assets/css/concepts-structure-v1.css`
2. `assets/css/concepts-local-overrides.css`
3. `assets/css/concepts-visual-refinements-v1.css`, injected by `assets/js/concepts-stage-2.js`

## Audit findings

- The website contains valid historical and corrective CSS layers rather than one clean authoritative stylesheet.
- The cascade currently produces the approved design, so immediate rule deletion would create more risk than value.
- Several legacy selectors remain useful as fallback protection for older cached markup.
- A true rule-level consolidation requires rendered desktop, tablet and mobile comparison before activation.
- The current static build does not require npm, preprocessing or a framework to improve stylesheet governance.

## Candidate replacement stylesheets

Two non-active candidates have been created:

- `vectisverse-site-v1/assets/css/site-production-consolidated-candidate.css`
- `vectisverse-site-v1/assets/css/concepts-production-consolidated-candidate.css`

Each candidate imports the current production stylesheets in their exact established order. This provides a single-reference test target while retaining visual equivalence.

The candidates are deliberately not linked from production HTML. Activating them without rendered comparison would provide little benefit and could introduce import-loading or cache differences.

## Safe activation workflow

1. Create a rollback branch from the current `main` commit.
2. Replace the multiple stylesheet references on one test branch with the appropriate candidate stylesheet.
3. Capture screenshots at 1440 × 900, 1024 × 768, 768 × 1024 and 390 × 844.
4. Compare homepage hero, comic panels, promotional cards, navigation, footer, Contact form and Concepts gallery.
5. Confirm focus states, mobile menus and reduced-motion behaviour.
6. Activate only if the screenshots are visually equivalent.
7. After equivalence is proven, copy the computed final rules into a genuinely flattened stylesheet in a separate later phase.
8. Retain the original files until the flattened stylesheet has passed live QA.

## Changes made during this refinement batch

- Reduced the Contact hero footprint while retaining its position above the form.
- Increased small Vectis Concepts service, gallery and footer typography.
- Added social controls to the standard mobile menu.
- Standardised Concepts gallery lazy loading and asynchronous decoding.
- Added browser-verified image dimensions when intrinsic dimensions become available.
- Reduced the Concepts mobile footer minimum height using non-clipping `min-height` rules.

## Decision

The candidate bundle stage is complete. Rule-level deletion or flattening is not authorised until rendered visual-equivalence testing is available.
