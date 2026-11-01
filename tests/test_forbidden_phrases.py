"""
Unit and Integration Test: Enforce Zero Forbidden Phrases in Documentation and Reports
======================================================================================
Scans all markdown and text deliverables under outputs/ (excluding archived outputs/v2)
and root README.md to strictly assert zero occurrences of forbidden, causal, or unscientific wording:
  - "flat" / "Corrected to Flat"
  - "Hydrologically Steady"
  - "proving" / "proven" / "proves"
  - "despite normal rainfall"
  - "Paradox confirmed" / "Paradox validated"
  - "cannot be attributed"
  - "completely decoupled"
  - "disproving"
  - "corroborat*"
  - "demonstrat*"
  - "confirmed"
  - "concentrated in"
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
    (r"\bParadox (confirmed|validated)\b", "Paradox confirmed/validated"),
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

        self.assertTrue(outputs_dir.exists(), "outputs directory must exist")
        self.assertTrue(readme_file.exists(), "README.md must exist")

        # Scan all .md and .txt files under outputs/ (excluding archived outputs/v2) and README.md
        target_files = [
            f for f in outputs_dir.rglob("*")
            if f.suffix in (".md", ".txt") and "v2" not in f.parts
        ] + [readme_file]

        self.assertGreater(len(target_files), 15, "Expected at least 15 documentation files to scan")

        violations = []

        for fpath in target_files:
            text = fpath.read_text(encoding="utf-8", errors="ignore")
            for pattern, label in FORBIDDEN_PATTERNS:
                matches = list(re.finditer(pattern, text, re.IGNORECASE))
                if matches:
                    rel_path = fpath.relative_to(REPO_ROOT)
                    matched_words = [m.group(0) for m in matches]
                    violations.append(f"{rel_path}: Found {len(matches)} occurrence(s) of '{label}' -> {matched_words}")

        if violations:
            msg = "\n".join(["Forbidden phrases detected in deliverables:"] + violations)
            self.fail(msg)


if __name__ == "__main__":
    unittest.main()
