"""
tests/test_js_parity.py
=======================
Automated Python test runner that executes Node.js tests
verifying mathematical parity between JS assets/js/stats.js and Python v3.
"""

import shutil
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestJsStatsParity(unittest.TestCase):

    def test_node_stats_parity(self):
        node_bin = shutil.which("node")
        if not node_bin:
            self.skipTest("Node.js is not installed on this system; skipping JS parity test.")

        test_file = REPO_ROOT / "tests/js/stats.test.mjs"
        self.assertTrue(test_file.exists(), f"Test file missing: {test_file}")

        res = subprocess.run(
            [node_bin, "--test", str(test_file)],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
        )

        self.assertEqual(
            res.returncode,
            0,
            f"Node.js parity test failed:\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}",
        )


if __name__ == "__main__":
    unittest.main()
