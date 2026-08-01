#!/usr/bin/env python3
"""Lightweight QA checks for the static VectisVerse production directory.

Uses only the Python standard library. It does not build, rewrite, or deploy the site.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SITE_DIR = Path("vectisverse-site-v1")
REQUIRED_FILES = {
    "index.html",
    "concepts.html",
    "contact.html",
    "contact-success.html",
    "accessibility.html",
    "404.html",
    "robots.txt",
    "sitemap.xml",
    "_headers",
}
REQUIRED_NAV_TARGETS = {"index.html", "concepts.html", "contact.html"}
OBSOLETE_TEXT = {
    "One Island. Endless Stories.": "obsolete tagline",
    "vecverse.pages.dev": "obsolete deployment host",
    "vectisverse-pages.pages.dev": "Pages preview host used in production content",
}
SUCCESS_PAGE = "contact-success.html"
WARN_SIZE_BYTES = 5 * 1024 * 1024
CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)(.*?)\1\s*\)", re.IGNORECASE)
SRCSET_SPLIT_RE = re.compile(r"\s*,\s*")


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.references: list[tuple[str, str]] = []
        self.links: set[str] = set()
        self.meta_robots: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): value for key, value in attrs if value is not None}
        for attribute in ("src", "href", "poster"):
            value = values.get(attribute)
            if value:
                self.references.append((attribute, value))
                if tag.lower() == "a" and attribute == "href":
                    self.links.add(value)
        srcset = values.get("srcset")
        if srcset:
            for candidate in SRCSET_SPLIT_RE.split(srcset):
                url = candidate.strip().split()[0] if candidate.strip() else ""
                if url:
                    self.references.append(("srcset", url))
        if tag.lower() == "meta" and values.get("name", "").lower() == "robots":
            self.meta_robots.append(values.get("content", "").lower())


def local_path(raw_reference: str, source: Path) -> Path | None:
    value = raw_reference.strip()
    if not value or value.startswith(("#", "mailto:", "tel:", "data:", "javascript:")):
        return None
    parsed = urlsplit(value)
    if parsed.scheme or parsed.netloc:
        return None
    path_text = unquote(parsed.path)
    if not path_text:
        return None
    if path_text.startswith("/"):
        candidate = SITE_DIR / path_text.lstrip("/")
    else:
        candidate = source.parent / path_text
    try:
        return candidate.resolve().relative_to(Path.cwd().resolve())
    except ValueError:
        return Path("__outside_site__")


def report(kind: str, message: str) -> None:
    print(f"::{kind}::{message}")


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not SITE_DIR.is_dir():
        errors.append(f"Production directory is missing: {SITE_DIR}")
    else:
        for relative in sorted(REQUIRED_FILES):
            if not (SITE_DIR / relative).is_file():
                errors.append(f"Required production file is missing: {SITE_DIR / relative}")

    html_files = sorted(SITE_DIR.rglob("*.html")) if SITE_DIR.is_dir() else []
    text_files = []
    if SITE_DIR.is_dir():
        text_files = sorted(
            path for path in SITE_DIR.rglob("*")
            if path.is_file() and path.suffix.lower() in {".html", ".css", ".js", ".txt", ".xml"}
        )

    for page in html_files:
        text = page.read_text(encoding="utf-8")
        parser = ReferenceParser()
        parser.feed(text)

        for attribute, reference in parser.references:
            candidate = local_path(reference, page)
            if candidate is None:
                continue
            if candidate == Path("__outside_site__"):
                errors.append(f"{page}: {attribute} escapes the repository site directory: {reference}")
                continue
            absolute = Path.cwd() / candidate
            if not absolute.exists():
                errors.append(f"{page}: missing local {attribute} target: {reference}")

        if page.name in {"index.html", "concepts.html", "contact.html", "accessibility.html", "404.html"}:
            normalised_links = {
                unquote(urlsplit(link).path).lstrip("./")
                for link in parser.links
                if not urlsplit(link).scheme and not urlsplit(link).netloc
            }
            missing_nav = sorted(REQUIRED_NAV_TARGETS - normalised_links)
            if missing_nav:
                errors.append(f"{page}: missing expected navigation links: {', '.join(missing_nav)}")

        if page.name == SUCCESS_PAGE:
            robots = " ".join(parser.meta_robots)
            if "noindex" not in robots:
                errors.append(f"{page}: success page must include a noindex robots directive")

    for stylesheet in sorted(SITE_DIR.rglob("*.css")) if SITE_DIR.is_dir() else []:
        text = stylesheet.read_text(encoding="utf-8")
        for match in CSS_URL_RE.finditer(text):
            reference = match.group(2).strip()
            candidate = local_path(reference, stylesheet)
            if candidate is None:
                continue
            if candidate == Path("__outside_site__"):
                errors.append(f"{stylesheet}: CSS url escapes the repository site directory: {reference}")
                continue
            if not (Path.cwd() / candidate).exists():
                errors.append(f"{stylesheet}: missing local CSS asset: {reference}")

    for text_file in text_files:
        text = text_file.read_text(encoding="utf-8")
        for needle, label in OBSOLETE_TEXT.items():
            if needle in text:
                errors.append(f"{text_file}: contains {label}: {needle}")

    if SITE_DIR.is_dir():
        for asset in sorted(path for path in SITE_DIR.rglob("*") if path.is_file()):
            size = asset.stat().st_size
            if size > WARN_SIZE_BYTES:
                warnings.append(
                    f"Large production file ({size / (1024 * 1024):.1f} MiB): {asset}"
                )

    for message in errors:
        report("error", message)
    for message in warnings:
        report("warning", message)

    print("\nVectisVerse static QA summary")
    print(f"HTML pages inspected: {len(html_files)}")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors:
        print("\nThe site was not modified. Resolve the errors above and rerun the check.")
        return 1
    print("\nAll required structural checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
