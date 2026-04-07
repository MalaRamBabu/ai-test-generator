import os
import subprocess
import json
from datetime import datetime


class TestRunner:
    """
    Step 4: Runs the AI-generated test file using PyTest.
    Captures pass/fail results and returns summary.
    """

    REPORTS_DIR = "output/reports"

    def __init__(self):
        os.makedirs(self.REPORTS_DIR, exist_ok=True)

    def run(self, test_filepath, page_name="test"):
        """
        Run a test file with PyTest.
        Returns result dict with pass/fail counts and output.
        """
        timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(
            self.REPORTS_DIR, f"report_{page_name}_{timestamp}.html"
        )
        json_path   = os.path.join(
            self.REPORTS_DIR, f"results_{page_name}_{timestamp}.json"
        )

        print(f"\n[TestRunner] Running: {test_filepath}")

        # Build pytest command
        cmd = [
            "pytest",
            test_filepath,
            "-v",
            "--tb=short",
            f"--html={report_path}",
            "--self-contained-html",
            f"--json-report",
            f"--json-report-file={json_path}",
            "--timeout=30",
        ]

        # Run tests
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True
        )

        # Parse results
        summary = self._parse_results(result, json_path, report_path)

        print(f"[TestRunner] Passed: {summary['passed']} | "
              f"Failed: {summary['failed']} | "
              f"Total: {summary['total']}")
        print(f"[TestRunner] Report: {report_path}")

        return summary

    def _parse_results(self, result, json_path, report_path):
        """Parse pytest output and return structured summary"""
        summary = {
            "passed":      0,
            "failed":      0,
            "error":       0,
            "total":       0,
            "duration":    0,
            "report_path": report_path,
            "output":      result.stdout,
            "returncode":  result.returncode,
        }

        # Try reading JSON report for detailed results
        if os.path.exists(json_path):
            try:
                with open(json_path) as f:
                    data = json.load(f)
                summary["passed"]   = data.get("summary", {}).get("passed",  0)
                summary["failed"]   = data.get("summary", {}).get("failed",  0)
                summary["error"]    = data.get("summary", {}).get("error",   0)
                summary["total"]    = data.get("summary", {}).get("total",   0)
                summary["duration"] = round(
                    data.get("duration", 0), 2
                )
            except Exception:
                pass

        # Fallback: parse from stdout
        if summary["total"] == 0:
            import re
            match = re.search(
                r"(\d+) passed(?:, (\d+) failed)?", result.stdout
            )
            if match:
                summary["passed"] = int(match.group(1))
                summary["failed"] = int(match.group(2) or 0)
                summary["total"]  = summary["passed"] + summary["failed"]

        return summary
