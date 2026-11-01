"""
NASA Space Apps 2026 – Bengal Hydro Detective
Unit Tests for Task 7: Benchmark Table and Novelty Statement Integrity
========================================================================
Verifies:
  1. Strict comparability rule: Only PUB-02 (Purdy et al., 2019) is marked 'Comparable: Yes'.
  2. All other studies (PUB-01, PUB-03, PUB-04, PUB-05, PUB-06) are marked 'Comparable: No' with documented reasons.
  3. All deliverables exist and are non-empty.
  4. Proper scientific labeling and no forbidden phrases.
"""

import unittest
import pandas as pd
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BENCHMARK_DIR = REPO_ROOT / "outputs" / "v3" / "benchmark"


class TestTask7Benchmark(unittest.TestCase):

    def setUp(self):
        self.csv_path = BENCHMARK_DIR / "benchmark_table.csv"
        self.md_path = BENCHMARK_DIR / "benchmark_table.md"
        self.novelty_path = BENCHMARK_DIR / "novelty_statement.md"
        self.register_path = BENCHMARK_DIR / "unaccessed_or_excluded_register.md"

        self.assertTrue(self.csv_path.exists(), f"Missing {self.csv_path}")
        self.assertTrue(self.md_path.exists(), f"Missing {self.md_path}")
        self.assertTrue(self.novelty_path.exists(), f"Missing {self.novelty_path}")
        self.assertTrue(self.register_path.exists(), f"Missing {self.register_path}")

        self.df = pd.read_csv(self.csv_path)

    def test_comparability_rule_strictness(self):
        # Exactly one study must be 'Yes': PUB-02 (Purdy et al., 2019)
        yes_entries = self.df[self.df["comparable"] == "Yes"]
        self.assertEqual(len(yes_entries), 1, "Only one study must be marked Comparable: Yes")
        self.assertEqual(yes_entries.iloc[0]["id"], "PUB-02", "Only Purdy et al. (2019) matches variable, period, and domain")

        # All other studies must be 'No'
        no_entries = self.df[self.df["comparable"] == "No"]
        self.assertEqual(len(no_entries), len(self.df) - 1, "All other studies must be marked Comparable: No")
        self.assertEqual(set(no_entries["id"].unique()), {"PUB-01", "PUB-03", "PUB-04", "PUB-05", "PUB-06"})

    def test_comparability_reasons_documented(self):
        for _, row in self.df.iterrows():
            reason = str(row["comparable_reason"])
            self.assertTrue(len(reason) > 10, f"Missing detailed comparability reason for {row['id']}")

    def test_novelty_statement_terminology(self):
        content = self.novelty_path.read_text(encoding="utf-8")
        # Forbidden terminology checks
        self.assertNotIn("aquifer storage", content.lower())
        self.assertNotIn("recharge efficiency", content.lower())
        self.assertNotIn("caused by", content.lower())
        self.assertIn("total water storage", content.lower())
        self.assertIn("seasonal storage response ratio", content.lower())


if __name__ == "__main__":
    unittest.main()
