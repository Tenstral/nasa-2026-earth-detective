from pathlib import Path

target_file = Path("tests/test_v3_task5_gldas_multimodel.py")
content = target_file.read_text(encoding="utf-8")

new_tests = '''    def test_independent_models_separation_and_range(self):
        self.assertIn("independent_sms_slope_min", self.df_summary.columns)
        self.assertIn("independent_sms_slope_max", self.df_summary.columns)
        self.assertIn("independent_residual_slope_min", self.df_summary.columns)
        self.assertIn("independent_residual_slope_max", self.df_summary.columns)

        for _, row in self.df_summary.iterrows():
            self.assertLessEqual(row["independent_sms_slope_min"], row["independent_sms_slope_max"])
            self.assertLessEqual(row["independent_residual_slope_min"], row["independent_residual_slope_max"])
            self.assertIn("cannot serve as an independent partition", str(row["clsm_independence_note"]))

    def test_homogeneity_interpretation_note(self):
        md_path = OUTPUT_DIR / "gldas_multi_model_summary.md"
        self.assertTrue(md_path.exists())
        md_text = md_path.read_text(encoding="utf-8")
        self.assertIn("Interpretation of Homogeneity Tests Under a Secular Trend", md_text)
        self.assertIn("does not constitute evidence of meteorological data inhomogeneity", md_text.replace("**", ""))

        json_path = OUTPUT_DIR / "gldas_multi_model_summary.json"
        self.assertTrue(json_path.exists())
        import json
        data = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertIn("homogeneity_interpretation_note", data)
'''

target_marker = 'if __name__ == "__main__":'
content = content.replace(target_marker, new_tests + "\n\n" + target_marker)
target_file.write_text(content, encoding="utf-8")
print("Updated test_v3_task5_gldas_multimodel.py")
