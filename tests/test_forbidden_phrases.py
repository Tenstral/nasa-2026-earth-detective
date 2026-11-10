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
    (r"\bstationary\b", "stationary"),
    (r"\bstable\b", "stable"),
    (r"\bunchanged\b", "unchanged"),
    (r"\bconstant\b", "constant"),
    (r"\brecharge_efficiency\b", "recharge_efficiency"),
    (r"\brecharge efficiency\b", "recharge efficiency"),
]

# Legitimate technical use allowlist (mathematical/statistical properties of simulation null models)
TECHNICAL_ALLOWLIST = [
    # Describes the stationary AR(1) null hypothesis noise process in Monte Carlo step-offset simulation
    ("outputs/v3/full_record/epoch_comparison.md", "stationary red noise"),
    ("outputs/v3/full_record/three_way_slopes_and_transition.md", "stationary red noise"),
]


class TestForbiddenPhrases(unittest.TestCase):

    def test_zero_forbidden_phrases_in_outputs_and_readme(self):
        outputs_dir = REPO_ROOT / "outputs"
        readme_file = REPO_ROOT / "README.md"
        notes_file = REPO_ROOT / "NOTES.md"
        project_status_file = REPO_ROOT / "PROJECT_STATUS.md"
        demo_file = REPO_ROOT / "demo.html"
        index_file = REPO_ROOT / "index.html"
        report_file = REPO_ROOT / "report.html"

        self.assertTrue(outputs_dir.exists(), "outputs directory must exist")
        self.assertTrue(readme_file.exists(), "README.md must exist")
        self.assertTrue(notes_file.exists(), "NOTES.md must exist")
        self.assertTrue(project_status_file.exists(), "PROJECT_STATUS.md must exist")
        self.assertTrue(demo_file.exists(), "demo.html must exist")
        self.assertTrue(index_file.exists(), "index.html must exist")
        self.assertTrue(report_file.exists(), "report.html must exist")

        # Scan all .md, .txt, and .html files under outputs/ (excluding archived outputs/v2),
        # plus root deliverables: README.md, NOTES.md, PROJECT_STATUS.md, demo.html, index.html, report.html
        target_files = [
            f for f in outputs_dir.rglob("*")
            if f.suffix in (".md", ".txt", ".html") and "v2" not in f.parts
        ] + [readme_file, notes_file, project_status_file, demo_file, index_file, report_file]

        # Explicitly verify the exploratory seasonal extensions and pairwise region comparisons are scanned
        ratio_md = outputs_dir / "v3" / "seasonal" / "ratio_trend.md"
        drawdown_md = outputs_dir / "v3" / "seasonal" / "dry_season_drawdown.md"
        pairwise_md = outputs_dir / "v3" / "region_comparison" / "pairwise_region_differences.md"
        self.assertIn(ratio_md, target_files, "ratio_trend.md must be included in scan targets")
        self.assertIn(drawdown_md, target_files, "dry_season_drawdown.md must be included in scan targets")
        if pairwise_md.exists():
            self.assertIn(pairwise_md, target_files, "pairwise_region_differences.md must be included in scan targets")

        self.assertGreater(len(target_files), 25, "Expected at least 25 documentation/html files to scan")

        violations = []

        for fpath in target_files:
            text = fpath.read_text(encoding="utf-8", errors="ignore")
            rel_path_str = str(fpath.relative_to(REPO_ROOT)).replace("\\", "/")

            for pattern, label in FORBIDDEN_PATTERNS:
                for m in re.finditer(pattern, text, re.IGNORECASE):
                    # Check technical allowlist
                    start = max(0, m.start() - 30)
                    end = min(len(text), m.end() + 30)
                    context_snippet = text[start:end].lower()

                    is_allowed = False
                    for allowed_file, allowed_phrase in TECHNICAL_ALLOWLIST:
                        if rel_path_str == allowed_file and allowed_phrase.lower() in context_snippet:
                            is_allowed = True
                            break

                    if not is_allowed:
                        violations.append(f"{rel_path_str}: Found '{label}' -> {m.group(0)} (context: {repr(text[start:end])})")

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
                        'Shamsudduha' in line or
                        # Verbatim limits text allowlist for pairwise region differences (PROJECT_STATUS.md & pairwise_region_differences.md)
                        'not a measurement of local aquifer or pumping differences' in line
                    )
                    if not is_quoted_or_citation:
                        rel_path = fpath.relative_to(REPO_ROOT)
                        violations.append(f"{rel_path}:{i}: Found unquoted 'aquifer' -> {line.strip()}")

        if violations:
            msg = "\n".join(["Forbidden phrases detected in deliverables:"] + violations)
            self.fail(msg)


if __name__ == "__main__":
    unittest.main()
