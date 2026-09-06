"""HTML and PDF rendering for Markdown CV files."""

from __future__ import annotations

import html
import shutil
import subprocess
import tempfile
from importlib.resources import files
from pathlib import Path

import yaml
from markdown_it import MarkdownIt


PAGE_BREAK = "<!-- pagebreak -->"


def parse_source(text: str) -> tuple[dict[str, str], str]:
    """Return YAML metadata and Markdown body from a CV source."""
    if not text.startswith("---\n"):
        raise ValueError("CV source must begin with YAML front matter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("CV source has an unterminated YAML front matter block")
    metadata = yaml.safe_load(parts[1]) or {}
    required = {"name", "location", "phone", "email"}
    missing = required.difference(metadata)
    if missing:
        raise ValueError(f"Missing required metadata: {', '.join(sorted(missing))}")
    return metadata, parts[2]


def _header(metadata: dict[str, str]) -> str:
    email = html.escape(str(metadata["email"]))
    label = html.escape(str(metadata.get("linkedin_label", "LinkedIn")))
    url = str(metadata.get("linkedin_url", "")).strip()
    link = (
        f'<a href="{html.escape(url, quote=True)}">{label}</a>'
        if url
        else f'<span class="link-label">{label}</span>'
    )
    return f"""
      <header class="resume-header">
        <h1 class="resume-name">{html.escape(str(metadata['name']))}</h1>
        <p class="contact">{html.escape(str(metadata['location']))} |
          {html.escape(str(metadata['phone']))} |
          <a href="mailto:{email}">{email}</a> | {link}</p>
      </header>
    """


def default_stylesheet() -> str:
    """Load the bundled default stylesheet."""
    return files("markdown_cv.styles").joinpath("default.css").read_text(encoding="utf-8")


def render_document(source_text: str, stylesheet: str | None = None) -> str:
    """Render a complete, print-ready HTML document from Markdown CV text."""
    metadata, body = parse_source(source_text)
    markdown = MarkdownIt("commonmark", {"html": True}).enable("table")
    header = _header(metadata)
    page_html = []
    for number, page in enumerate(body.split(PAGE_BREAK), start=1):
        content = markdown.render(page.strip())
        page_html.append(
            f'<section class="page page-{number}">{header}'
            f'<main class="content">{content}</main></section>'
        )
    css = stylesheet if stylesheet is not None else default_stylesheet()
    title = html.escape(str(metadata["name"]).title() + " Resume")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>{css}</style>
</head>
<body>
{''.join(page_html)}
</body>
</html>
"""


def find_browser() -> str:
    """Return a supported Chromium-family browser executable."""
    for candidate in ("google-chrome", "chromium", "chromium-browser", "chrome"):
        executable = shutil.which(candidate)
        if executable:
            return executable
    raise RuntimeError("Google Chrome or Chromium is required to render a PDF")


def build_pdf(
    source: Path,
    output: Path,
    *,
    stylesheet: Path | None = None,
    html_output: Path | None = None,
    browser: str | None = None,
) -> Path:
    """Build a PDF and optionally retain the intermediate HTML file."""
    source = source.resolve()
    output = output.resolve()
    css = stylesheet.read_text(encoding="utf-8") if stylesheet else None
    document = render_document(source.read_text(encoding="utf-8"), css)
    rendered_html = html_output.resolve() if html_output else output.with_suffix(".html")
    rendered_html.parent.mkdir(parents=True, exist_ok=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    rendered_html.write_text(document, encoding="utf-8")

    with tempfile.TemporaryDirectory(prefix="markdown-cv-chrome-") as profile:
        command = [
            browser or find_browser(),
            "--headless",
            "--disable-gpu",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--no-pdf-header-footer",
            f"--user-data-dir={profile}",
            f"--print-to-pdf={output}",
            rendered_html.as_uri(),
        ]
        completed = subprocess.run(command, check=False, text=True, capture_output=True)
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or "Browser PDF rendering failed")
    if html_output is None:
        rendered_html.unlink(missing_ok=True)
    return output
