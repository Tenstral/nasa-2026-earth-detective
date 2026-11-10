"""
Unit and Integration Test: Enforce Zero Forbidden Phrases in Documentation and Reports
======================================================================================
Scans all markdown and text deliverables under outputs/ (excluding archived outputs/v2),
demo.html, index.html, README.md, and PROJECT_STATUS.md to strictly assert zero occurrences
of forbidden, causal, or unscientific wording:
  - "flat" / "Corrected to Flat"
  - "Hydrologically Steady"
  - "proving" / "proven" / "proves"
  - "despite normal rainfall"
  - "paradox"
  - "cannot be attributed"
  - "completely decoupled"
  - "disproving"
  - "corroborat*"
  - "demonstrat*"
  - "confirmed"
  - "concentrated in"
  - "aquifer" (except in quoted source titles, citations, or bibliography entries)
"""

import re
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_PATTERNS = [
    (r"\bflat\b", "flat"),
    (r"\bCorrected to Flat\b", "Corrected to Flat"),
    (r"\bHydrologically Steady\b", "Hydrologically Steady"),
    (r"\bprov(ing|en|es)\b", "proving/proven/proves"),
    (r"\bdespite normal rainfall\b", "despite normal rainfall"),
    (r"\bparadox\w*\b", "paradox"),
    (r"\bcannot be attributed\b", "cannot be attributed"),
    (r"\bcompletely decoupled\b", "completely decoupled"),
    (r"\bdisproving\b", "disproving"),
    (r"\bcorroborat\w*", "corroborat*"),
    (r"\bdemonstrat\w*", "demonstrat*"),
    (r"\bconfirmed\b", "confirmed"),
    (r"\bconcentrated in\b", "concentrated in"),
]


class TestForbiddenPhrases(unittest.TestCase):

    def test_zero_forbidden_phrases_in_outputs_and_readme(self):
        outputs_dir = REPO_ROOT / "outputs"
        readme_file = REPO_ROOT / "README.md"
        project_status_file = REPO_ROOT / "PROJECT_STATUS.md"
        demo_file = REPO_ROOT / "demo.html"
        index_file = REPO_ROOT / "index.html"

        self.assertTrue(outputs_dir.exists(), "outputs directory must exist")
        self.assertTrue(readme_file.exists(), "README.md must exist")
        self.assertTrue(project_status_file.exists(), "PROJECT_STATUS.md must exist")
        self.assertTrue(demo_file.exists(), "demo.html must exist")
        self.assertTrue(index_file.exists(), "index.html must exist")

        # Scan all .md, .txt, and .html files under outputs/ (excluding archived outputs/v2),
        # plus root deliverables: README.md, PROJECT_STATUS.md, demo.html, index.html
        target_files = [
            f for f in outputs_dir.rglob("*")
            if f.suffix in (".md", ".txt", ".html") and "v2" not in f.parts
        ] + [readme_file, project_status_file, demo_file, index_file]

        # Explicitly verify the exploratory seasonal extensions are scanned
        ratio_md = outputs_dir / "v3" / "seasonal" / "ratio_trend.md"
        drawdown_md = outputs_dir / "v3" / "seasonal" / "dry_season_drawdown.md"
        self.assertIn(ratio_md, target_files, "ratio_trend.md must be included in scan targets")
        self.assertIn(drawdown_md, target_files, "dry_season_drawdown.md must be included in scan targets")

        self.assertGreater(len(target_files), 25, "Expected at least 25 documentation/html files to scan")

        violations = []

        for fpath in target_files:
            text = fpath.read_text(encoding="utf-8", errors="ignore")
            for pattern, label in FORBIDDEN_PATTERNS:
                matches = list(re.finditer(pattern, text, re.IGNORECASE))
                if matches:
                    rel_path = fpath.relative_to(REPO_ROOT)
                    matched_words = [m.group(0) for m in matches]
                    violations.append(f"{rel_path}: Found {len(matches)} occurrence(s) of '{label}' -> {matched_words}")

            # Check "aquifer" rule: forbidden except in quoted source titles, citations, or bibliography
            for i, line in enumerate(text.splitlines(), 1):
                if re.search(r"\baquifers?\b", line, re.IGNORECASE):
                    is_quoted_or_citation = (
                        '"' in line or
                        '\u201c' in line or
                        '\u201d' in line or
                        '| **PUB-' in line or
                        '### [PUB-' in line or
                        'Taylor' in line or
                        'Shamsudduha' in line
                    )
                    if not is_quoted_or_citation:
                        rel_path = fpath.relative_to(REPO_ROOT)
                        violations.append(f"{rel_path}:{i}: Found unquoted 'aquifer' -> {line.strip()}")

        if violations:
            msg = "\n".join(["Forbidden phrases detected in deliverables:"] + violations)
            self.fail(msg)


if __name__ == "__main__":
    unittest.main()
