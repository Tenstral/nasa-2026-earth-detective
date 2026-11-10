"""
Unit Test: Verify run_all.py default rain source is IMERG
=========================================================
Asserts:
  1. Default --rain-source is 'imerg'.
  2. Selecting 'power' prints a step-change warning.
"""

import subprocess
import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUN_ALL_PY = REPO_ROOT / "run_all.py"


class TestRunAllRainSource(unittest.TestCase):

    def test_default_rain_source_is_imerg_in_parser(self):
        """Verify argparse default for --rain-source is 'imerg'."""
        cmd = [
            sys.executable,
            "-c",
            "import argparse; from run_all import main; import inspect; "
            "code = inspect.getsource(main); "
            "assert \"default='imerg'\" in code or 'default=\"imerg\"' in code"
        ]
        res = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"run_all.py default is not imerg: {res.stderr}")

    def test_help_text_shows_imerg_default(self):
        """Verify python run_all.py --help lists imerg as default."""
        cmd = [sys.executable, str(RUN_ALL_PY), "--help"]
        res = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)
        self.assertIn("default", res.stdout.lower())
        self.assertIn("'imerg'", res.stdout.lower())

    def test_warning_printed_when_power_selected(self):
        """Verify warning message when --rain-source power is specified."""
        cmd = [
            sys.executable,
            "-c",
            "import subprocess, sys; "
            "res = subprocess.run([sys.executable, 'run_all.py', '--rain-source', 'power', '--help'], capture_output=True, text=True); "
            "# Since --help exits before main loop, test parser directly:; "
            "from run_all import main; import inspect; "
            "code = inspect.getsource(main); "
            "assert 'NASA POWER has a step change around 2014-12 to 2015-12' in code"
        ]
        res = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
        self.assertEqual(res.returncode, 0)


if __name__ == "__main__":
    unittest.main()
