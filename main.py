#!/usr/bin/env python3
"""
AI-Powered Test Generator
=========================
Give it a URL → AI analyses the page → generates Playwright tests → runs them → report

Usage:
    python main.py --url https://automationexercise.com --name home
    python main.py --url https://automationexercise.com/login --name login
    python main.py --url https://automationexercise.com/products --name products
    python main.py --help
"""

import os
import sys
import argparse

from core.page_analyser          import PageAnalyser
from generator.gemini_generator  import GeminiTestGenerator
from generator.test_file_writer  import TestFileWriter
from runner.test_runner          import TestRunner
from reporter.report_generator   import ReportGenerator


def print_banner():
    print("""
╔══════════════════════════════════════════════════════╗
║          AI-POWERED TEST GENERATOR                   ║
║  Playwright + Google Gemini AI + Python + PyTest     ║
║  Author: Mala Ram Babu | Senior QA Automation Eng.   ║
╚══════════════════════════════════════════════════════╝
""")


def print_step(step, total, message):
    print(f"\n{'─'*55}")
    print(f"  Step {step}/{total}: {message}")
    print(f"{'─'*55}")


def run(url, page_name, skip_run=False):
    """
    Main pipeline:
    1. Analyse page
    2. Generate tests with AI
    3. Save to file
    4. Run with PyTest
    5. Generate report
    """
    print_banner()
    print(f"Target URL  : {url}")
    print(f"Page Name   : {page_name}")
    print(f"Skip Run    : {skip_run}")

    # ── Step 1: Analyse Page ──────────────────────────────────────────────────
    print_step(1, 5, "Analysing page with Playwright")
    analyser  = PageAnalyser()
    analysis  = analyser.analyse(url, page_name)

    # ── Step 2: Generate Tests with Gemini AI ─────────────────────────────────
    print_step(2, 5, "Generating test cases with Gemini AI")
    generator = GeminiTestGenerator()
    code      = generator.generate_tests(analysis)

    # ── Step 3: Save Generated Tests ─────────────────────────────────────────
    print_step(3, 5, "Saving generated test file")
    writer    = TestFileWriter()
    test_path = writer.save(code, page_name)
    print(f"\nGenerated test file:\n{test_path}")
    print("\n--- Preview (first 20 lines) ---")
    lines = code.split("\n")[:20]
    print("\n".join(lines))
    print("...")

    # ── Step 4: Run Tests ─────────────────────────────────────────────────────
    run_summary = {"passed": 0, "failed": 0, "total": 0, "duration": 0}
    if not skip_run:
        print_step(4, 5, "Running tests with PyTest")
        runner      = TestRunner()
        run_summary = runner.run(test_path, page_name)
    else:
        print_step(4, 5, "Skipping test run (--skip-run flag set)")
        print("Tests saved but not executed.")

    # ── Step 5: Generate Report ───────────────────────────────────────────────
    print_step(5, 5, "Generating HTML report")
    reporter    = ReportGenerator()
    report_path = reporter.generate(analysis, code, run_summary)

    # ── Final Summary ─────────────────────────────────────────────────────────
    print(f"""
╔══════════════════════════════════════════════════════╗
║  GENERATION COMPLETE!                                ║
╠══════════════════════════════════════════════════════╣
║  URL Analysed   : {url[:35]:<35} ║
║  Tests Generated: {run_summary.get('total', '?'):<35} ║
║  Tests Passed   : {run_summary.get('passed', '?'):<35} ║
║  Tests Failed   : {run_summary.get('failed', '?'):<35} ║
╠══════════════════════════════════════════════════════╣
║  Test File : {test_path[:42]:<42} ║
║  Report    : {report_path[:42]:<42} ║
╚══════════════════════════════════════════════════════╝
""")
    return report_path


def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered Test Generator — Give URL, get Playwright tests!",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --url https://automationexercise.com --name home
  python main.py --url https://automationexercise.com/login --name login
  python main.py --url https://automationexercise.com/products --name products --skip-run
        """
    )
    parser.add_argument(
        "--url",
        required=True,
        help="URL of the page to analyse and generate tests for"
    )
    parser.add_argument(
        "--name",
        required=True,
        help="Short name for the page (used in filenames, e.g. 'login', 'home')"
    )
    parser.add_argument(
        "--skip-run",
        action="store_true",
        help="Generate tests but skip running them (useful for review first)"
    )

    args = parser.parse_args()
    run(args.url, args.name, skip_run=args.skip_run)


if __name__ == "__main__":
    main()
