# VectisVerse Website Operations Guide

This guide supports routine maintenance of the static VectisVerse website. It does not replace `SOURCE_OF_TRUTH.md`; where the two differ, `SOURCE_OF_TRUTH.md` takes precedence.

## Production model

- Repository: `rascal1234123/vectisverse`
- Production branch: `main`
- Published directory: `vectisverse-site-v1`
- Cloudflare Pages project: `vectisverse-pages`
- Framework preset: `None`
- Build command: `exit 0`
- Build output directory: `.`

Keep the website as plain HTML, CSS, JavaScript and static assets unless a specific requirement justifies a different approach. Do not introduce a framework, npm build, server function or paid service as routine maintenance.

## Production page inventory

The expected production pages are:

- `index.html` — homepage
- `concepts.html` — Vectis Concepts
- `contact.html` — contact page and FormSubmit form
- `contact-success.html` — transactional success page; must remain `noindex`
- `accessibility.html` — accessibility information
- `404.html` — Cloudflare static error page; must remain `noindex`

Supporting production files include:

- `_headers`
- `robots.txt`
- `sitemap.xml`
- `assets/css/`
- `assets/js/`
- production image and SVG directories under `assets/`

## Required checks before every website change

1. Confirm the target is `main` in `rascal1234123/vectisverse`.
2. Confirm all website edits are inside `vectisverse-site-v1`, except approved repository documentation, QA scripts and GitHub workflows.
3. Read the current file from `main` before replacing it.
4. Change only the files required for the requested outcome.
5. Preserve approved artwork, filenames and cache query strings unless the asset itself is deliberately replaced.
6. Re-read every changed file from `main` after committing.
7. Check the GitHub Actions result or job summary for **VectisVerse Static QA** when available.
8. Check the corresponding public page after Cloudflare has published the commit.

## Shared-element change checklist

The standard VectisVerse header and footer appear in:

- `index.html`
- `contact.html`
- `contact-success.html`
- `accessibility.html`
- `404.html`

`concepts.html` uses its own approved Vectis Concepts presentation and should not be forced into the standard visual structure. It must still retain working Home, Vectis Concepts, Contact and Accessibility routes where applicable.

When changing the standard header, footer or navigation:

- inspect all five standard pages;
- preserve the mobile menu button, `aria-expanded` and `aria-controls` relationship;
- preserve the Home, Vectis Concepts and Contact links;
- preserve social links and their accessible labels;
- set `aria-current="page"` only on the appropriate page;
- preserve the approved `Entertainment` footer descriptor;
- check desktop and mobile menu behaviour.

## Global CSS and JavaScript changes

When changing a shared CSS or JavaScript file:

- identify every HTML page that loads it;
- update the cache-version query wherever that file is referenced, using one consistent value;
- do not update unrelated asset version strings;
- check that the change does not affect the bespoke Concepts page unless intended;
- confirm keyboard navigation and visible focus remain usable;
- confirm the mobile menu still opens, closes and responds to Escape.

The current static approach deliberately uses query-string cache versions. Do not add hashed-file compilation merely for cache control.

## Asset replacement checklist

When replacing an image or SVG:

1. Treat approved Gold Master artwork as locked unless the requested change expressly replaces it.
2. Confirm the new file exists in the intended production asset directory.
3. Update every exact HTML or CSS reference to that asset.
4. Retain or add accurate `width` and `height` only when verified from the source.
5. Keep critical hero imagery eager; use `loading="lazy"` only for below-the-fold imagery.
6. Preserve meaningful alternative text; use `alt=""` for genuinely decorative imagery.
7. Do not delete the previous asset until all references have been checked and its removal is clearly safe.
8. Run or review the static QA workflow after committing.

## Contact-form safeguards

The current Contact form deliberately uses FormSubmit because the preferred Cloudflare-backed implementation was not viable within the chosen service level.

Routine changes must preserve:

- `action="https://formsubmit.co/contact@vectisverse.com"`;
- `method="POST"`;
- `_subject`;
- `_template`;
- `_next` pointing to `https://www.vectisverse.com/contact-success.html`;
- `_url` pointing to `https://www.vectisverse.com/contact.html`;
- the `_honey` field;
- the direct `mailto:` fallback;
- matching labels and field IDs;
- required fields and maximum lengths;
- `noindex,follow` on `contact-success.html`.

Do not replace FormSubmit, add a Worker, add Turnstile or introduce another mail provider unless there is a demonstrated operational need and the service implications have been accepted.

## Search and static housekeeping safeguards

- `robots.txt` must continue to reference `https://www.vectisverse.com/sitemap.xml`.
- `sitemap.xml` should include only indexable production pages.
- Do not include `contact-success.html` or `404.html` in the sitemap.
- Each indexable page should retain its correct absolute canonical URL.
- The success and error pages must remain `noindex,follow`.
- Do not add social preview image metadata until a suitable verified production asset exists.

## Commit conventions

Use short, descriptive commit messages. Recommended forms:

- `fix(contact): correct success-page metadata`
- `fix(navigation): align shared footer links`
- `perf(images): add verified image dimensions`
- `docs(operations): update deployment checklist`
- `chore(qa): extend static reference checks`

Avoid generic messages such as `Add files via upload` where a specific description is possible.

Keep unrelated changes in separate commits so that each repair can be reviewed or reverted independently.

## Post-change assurance checklist

For each changed page:

- the page loads with the expected design;
- header, navigation and footer are present;
- internal links resolve;
- images and SVGs load;
- the mobile menu operates;
- external links retain `target="_blank"` and `rel="noopener noreferrer"` where appropriate;
- active navigation state is correct;
- no obsolete tagline or Cloudflare preview hostname appears;
- Contact form settings remain intact when Contact files are involved;
- no approved artwork has been unintentionally changed.

For site-wide changes, also confirm:

- `robots.txt` is reachable;
- `sitemap.xml` is reachable;
- a deliberately invalid path displays the custom 404 page;
- the **VectisVerse Static QA** workflow reports its findings.

## Cloudflare verification checklist

These checks require access to the Cloudflare dashboard and should be performed after any deployment-source or domain change:

- project is `vectisverse-pages`;
- repository is `rascal1234123/vectisverse`;
- production branch is `main`;
- root directory is `vectisverse-site-v1`;
- framework preset is `None`;
- build command remains `exit 0`;
- output directory remains `.`;
- `vectisverse.com` and `www.vectisverse.com` are attached only to the canonical project;
- the older `vecverse` project has no production domain and no unintended automatic deployment.

Do not delete an older Cloudflare project until the canonical project and both public domains have been verified.

## Conservative rollback procedure

Use rollback only when a committed change has caused a confirmed production problem.

1. Identify the first problematic commit and the last known-good commit.
2. Prefer a new revert commit over rewriting history or force-pushing `main`.
3. Revert only the problematic commit when it is self-contained.
4. When several dependent commits are involved, revert them in reverse order.
5. Confirm the revert does not remove later unrelated fixes.
6. Allow Cloudflare to publish the revert normally from `main`.
7. Recheck the affected public page, navigation, assets and Contact form where relevant.
8. Record the cause and corrected approach in the next repair commit or this guide if it represents a reusable lesson.

Do not force-reset `main`, delete repository history or restore from an old ZIP deployment as a normal rollback method.

## Lightweight QA

The repository includes:

- `.github/workflows/site-qa.yml`
- `scripts/qa_static_site.py`

The checker is informational and uses only the Python standard library. It does not build, rewrite or deploy the website. Cloudflare remains responsible for publishing the static production directory.
