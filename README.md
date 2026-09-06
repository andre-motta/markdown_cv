# markdown_cv

`markdown_cv` turns an editable Markdown resume into a polished Letter-size PDF. It supports YAML contact metadata, Markdown tables, explicit page breaks, bundled resume styling, and optional CSS overrides.

[![PyPI](https://img.shields.io/pypi/v/markdown-cv.svg)](https://pypi.org/project/markdown-cv/)

## Requirements

- Python 3.10 or newer
- Google Chrome or Chromium

## Install

```bash
python3 -m pip install .
```

## Build a resume

```bash
markdown-cv build examples/sample_cv.md --output sample_cv.pdf
```

Use `<!-- pagebreak -->` on its own line to start a new PDF page. Contact information belongs in the YAML block at the top of the source. The sample contains only fictional placeholder information.

To keep the intermediate HTML for browser inspection:

```bash
markdown-cv build examples/sample_cv.md --output sample_cv.pdf --html-output sample_cv.html
```

To override the bundled layout:

```bash
markdown-cv build cv.md --output cv.pdf --style custom.css
```

## Development

```bash
python3 -m pip install -e .
python3 -m unittest discover -s tests
```
