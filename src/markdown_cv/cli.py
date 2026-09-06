"""Command line interface for markdown-cv."""

from __future__ import annotations

import argparse
from pathlib import Path

from markdown_cv.builder import build_pdf


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="markdown-cv",
        description="Build a polished PDF resume from Markdown.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    build = subparsers.add_parser("build", help="Build a PDF")
    build.add_argument("source", type=Path, help="Markdown CV source")
    build.add_argument("--output", "-o", type=Path, required=True, help="Output PDF")
    build.add_argument("--style", type=Path, help="Optional CSS override")
    build.add_argument("--html-output", type=Path, help="Keep the rendered HTML")
    args = parser.parse_args()

    if args.command == "build":
        result = build_pdf(
            args.source,
            args.output,
            stylesheet=args.style,
            html_output=args.html_output,
        )
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
