"""
Unit and Integration Test: Enforce Zero Forbidden Phrases in Documentation and Reports
======================================================================================
Scans all markdown and text deliverables under outputs/v3/ and root README.md
to strictly assert zero occurrences of forbidden, causal, or unscientific wording:
  - "flat" / "Corrected to Flat"
  - "Hydrologically Steady"
  - "proving" / "proven" / "proves"
  - "despite normal rainfall"
  - "Paradox confirmed" / "Paradox validated"
  - "cannot be attributed to meteorological drought"
  - "completely decoupled"
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
    (r"\bcannot be attributed to meteorological drought\b", "cannot be attributed to meteorological drought"),
    (r"\bcompletely decoupled\b", "completely decoupled"),
]


class TestForbiddenPhrases(unittest.TestCase):

    def test_zero_forbidden_phrases_in_outputs_v3_and_readme(self):
        v3_dir = REPO_ROOT / "outputs" / "v3"
        readme_file = REPO_ROOT / "README.md"

        self.assertTrue(v3_dir.exists(), "outputs/v3 directory must exist")
        self.assertTrue(readme_file.exists(), "README.md must exist")

        target_files = list(v3_dir.rglob("*.md")) + list(v3_dir.rglob("*.txt")) + [readme_file]
        self.assertGreater(len(target_files), 10, "Expected at least 10 documentation files to scan")

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
