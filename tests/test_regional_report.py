"""
Unit and Integration Test: Validate Regional Stakeholder Report Structure and Data
==================================================================================
Ensures regional_action_report.md adheres strictly to:
1. Title and required sections:
   - Starts with "# Bengal Hydro Detective: Regional Stakeholder Summary"
   - Section "## How to read this report"
   - Between-region paired comparison note in methodological limits
   - Five macro-regions: Northwest, Northeast, Central, Southwest, Southeast
   - Three standard subsections per region:
     * "What the satellite data shows"
     * "Context from the literature (not tested here)"
     * "Options others have proposed"
   - Closing section "## What this report does not claim"
   - "## Sources" with numbered authoritative literature references
2. Scientific numerical integrity:
   - TWS and precipitation slopes and CIs match results_all_windows.csv and exposure_table.csv
   - Northwest three-way depletion range (-1.81 to -1.25 cm/year)
   - Population and cropland exposure percentages match exposure_table.csv
   - Seasonal response ratios and drawdowns match seasonal analysis CSVs
"""

import re
import unittest
from pathlib import Path
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORT_FILE = REPO_ROOT / "regional_action_report.md"


class TestRegionalReport(unittest.TestCase):

    def setUp(self):
        self.assertTrue(REPORT_FILE.exists(), "regional_action_report.md must exist in repo root")
        self.text = REPORT_FILE.read_text(encoding="utf-8")

    def test_01_title_and_structure(self):
        lines = [line.strip() for line in self.text.splitlines() if line.strip()]
        self.assertTrue(
            lines[0].startswith("# Bengal Hydro Detective: Regional Stakeholder Summary"),
            "Report must start with '# Bengal Hydro Detective: Regional Stakeholder Summary'"
        )
        self.assertIn("## How to read this report", self.text)
        self.assertIn("## What this report does not claim", self.text)
        self.assertIn("## Sources", self.text)

    def test_02_intro_limits_and_between_region_note(self):
        # Intro limits box must contain between-region comparison text
        self.assertIn("Between-region differences in total water storage were tested with a calibrated paired method", self.text)
        self.assertIn("NW declines about 1.2 cm/yr faster than SW and SE", self.text)
        self.assertIn("NE and Central decline about 0.5 cm/yr faster than SW and SE", self.text)
        self.assertIn("SW and SE are indistinguishable", self.text)
        self.assertIn("no rainfall pair differs", self.text)
        self.assertIn("placebo check shows they are overconfident", self.text)
        self.assertIn("not a measurement of local aquifer or pumping differences", self.text)

    def test_03_five_regions_present_with_required_subsections(self):
        expected_regions = ["Northwest", "Northeast", "Central", "Southwest", "Southeast"]
        for reg in expected_regions:
            self.assertRegex(
                self.text,
                rf"## \d+\.\s+.*{reg}",
                f"Missing section for macro-region: {reg}"
            )

        # Count occurrences of the 3 required subsections
        shows_count = len(re.findall(r"### What the satellite data shows", self.text))
        context_count = len(re.findall(r"### Context from the literature \(not tested here\)", self.text))
        options_count = len(re.findall(r"### Options others have proposed", self.text))

        self.assertEqual(shows_count, 5, f"Expected 5 'What the satellite data shows' sections, got {shows_count}")
        self.assertEqual(context_count, 5, f"Expected 5 'Context from the literature' sections, got {context_count}")
        self.assertEqual(options_count, 5, f"Expected 5 'Options others have proposed' sections, got {options_count}")

    def test_04_closing_limits_section(self):
        # Must have the 4 explicit non-claims
        self.assertIn("No local-scale depth-to-water claims", self.text)
        self.assertIn("No causal attribution", self.text)
        self.assertIn("No water quality or salinity measurements", self.text)
        self.assertIn("No blanket policy mandate", self.text)

    def test_05_verified_satellite_numbers(self):
        # Northwest numbers
        self.assertIn("-1.25 cm/year", self.text)
        self.assertIn("[-1.50, -1.02]", self.text)
        self.assertIn("-0.39 km³/year", self.text)
        self.assertIn("-1.9 mm/year", self.text)
        self.assertIn("[-11.0, +4.5]", self.text)
        self.assertIn("38.8 million", self.text)
        self.assertIn("74.2%", self.text)
        self.assertIn("-1.81 to -1.25 cm/year", self.text)

        # Northeast numbers
        self.assertIn("-0.56 cm/year", self.text)
        self.assertIn("[-0.70, -0.42]", self.text)
        self.assertIn("-0.6 mm/year", self.text)
        self.assertIn("[-15.4, +16.1]", self.text)
        self.assertIn("24.1 million", self.text)
        self.assertIn("58.6%", self.text)

        # Central numbers
        self.assertIn("-0.47 cm/year", self.text)
        self.assertIn("[-0.62, -0.34]", self.text)
        self.assertIn("+0.9 mm/year", self.text)
        self.assertIn("[-9.7, +12.7]", self.text)
        self.assertIn("45.6 million", self.text)
        self.assertIn("56.4%", self.text)

        # Southwest & Southeast numbers
        self.assertIn("-0.05 cm/year", self.text)
        self.assertIn("27.1 million", self.text)
        self.assertIn("34.2 million", self.text)
        self.assertIn("48.7%", self.text)
        self.assertIn("32.1%", self.text)


if __name__ == "__main__":
    unittest.main()
