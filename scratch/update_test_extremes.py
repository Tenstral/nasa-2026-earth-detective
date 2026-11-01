from pathlib import Path

target_file = Path("tests/test_v3_task6_extremes.py")
content = target_file.read_text(encoding="utf-8")

new_tests = '''    def test_ci_p_value_duality_and_bounds(self):
        df = pd.read_csv(self.trends_csv)
        for _, row in df.iterrows():
            p = row["p_value"]
            ci_low = row["slope_ci_low"]
            ci_high = row["slope_ci_high"]
            slope = row["slope"]
            idx = row["index_name"]
            reg = row["region"]

            ci_excludes_zero = (ci_low > 0 and ci_high > 0) or (ci_low < 0 and ci_high < 0)

            # Strict duality: if p > 0.05, CI MUST include zero
            if p > 0.05:
                self.assertFalse(ci_excludes_zero,
                                 f"CI excludes zero [{ci_low}, {ci_high}] but p={p} > 0.05 for {reg} {idx}")

            # Physical slope bounds check: annual total slope must not be erroneously multiplied by 12
            if "total" in idx:
                self.assertLess(abs(slope), 50.0,
                                f"Implausibly large total rainfall slope ({slope} mm/yr) for {reg} {idx}")
            elif "rx" in idx:
                self.assertLess(abs(slope), 20.0,
                                f"Implausibly large extreme rainfall slope ({slope} mm/yr) for {reg} {idx}")

    def test_spatial_aggregation_and_cross_check_documentation(self):
        md_text = self.trends_md.read_text(encoding="utf-8")
        self.assertIn("Spatial Aggregation Protocol", md_text)
        self.assertIn("Daily vs. Monthly IMERG Hand Cross-Check", md_text)
        self.assertIn("2,010.0", md_text)
        self.assertIn("1,732.8", md_text)

        json_file = EXTREMES_DIR / "imerg_extreme_indices_summary.json"
        self.assertTrue(json_file.exists())
        import json
        data = json.loads(json_file.read_text(encoding="utf-8"))
        self.assertIn("spatial_aggregation_protocol", data)
        self.assertIn("hand_cross_check_2010", data)
'''

target_marker = 'if __name__ == "__main__":'
content = content.replace(target_marker, new_tests + "\n\n" + target_marker)
target_file.write_text(content, encoding="utf-8")
print("Updated test_v3_task6_extremes.py")
