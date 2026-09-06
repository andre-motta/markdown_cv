from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from markdown_cv.builder import parse_source, render_document


class BuilderTests(unittest.TestCase):
    def test_sample_renders_with_contact_and_sections(self) -> None:
        source = (ROOT / "examples" / "sample_cv.md").read_text(encoding="utf-8")
        rendered = render_document(source)
        self.assertIn("CANDIDATE NAME", rendered)
        self.assertIn("mailto:candidate@example.com", rendered)
        self.assertIn("SUMMARY", rendered)

    def test_missing_metadata_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Missing required metadata"):
            parse_source("---\nname: Test\n---\n\n## Summary")


if __name__ == "__main__":
    unittest.main()
