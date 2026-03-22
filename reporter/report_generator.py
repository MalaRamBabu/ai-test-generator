import os
from datetime import datetime


class ReportGenerator:
    """
    Step 5: Generates a beautiful HTML summary report
    showing what AI generated, what ran, and what passed/failed.
    """

    REPORTS_DIR = "output/reports"

    def __init__(self):
        os.makedirs(self.REPORTS_DIR, exist_ok=True)

    def generate(self, page_analysis, generated_code, run_summary):
        """
        Generate full HTML report combining:
        - Page analysis results
        - Generated test code preview
        - Test run pass/fail summary
        """
        timestamp   = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_path = os.path.join(
            self.REPORTS_DIR,
            f"ai_test_report_{page_analysis['page_name']}_{timestamp}.html"
        )

        html = self._build_html(page_analysis, generated_code, run_summary)

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html)

        print(f"[ReportGenerator] Report saved: {report_path}")
        return report_path

    def _build_html(self, analysis, code, summary):
        url        = analysis["url"]
        title      = analysis["title"]
        page_name  = analysis["page_name"]
        elements   = analysis["elements"]
        screenshot = analysis.get("screenshot_path", "")
        passed     = summary.get("passed",   0)
        failed     = summary.get("failed",   0)
        total      = summary.get("total",    0)
        duration   = summary.get("duration", 0)
        pass_rate  = round((passed / total * 100), 1) if total > 0 else 0

        status_color = "#27ae60" if failed == 0 else "#e74c3c"
        status_text  = "ALL PASSED" if failed == 0 else f"{failed} FAILED"

        # Count test functions in generated code
        import re
        test_count = len(re.findall(r"def test_", code))

        elements_html = ""
        for key, items in elements.items():
            if items:
                elements_html += f"""
                <div class="elem-card">
                    <div class="elem-title">{key.replace('_', ' ').title()}</div>
                    <div class="elem-count">{len(items)}</div>
                </div>"""

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI Test Report — {title}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: Arial, sans-serif; background: #f0f2f5; color: #1a1a1a; }}
  .header {{ background: #1B3A6B; color: white; padding: 24px 40px; }}
  .header h1 {{ font-size: 24px; margin-bottom: 4px; }}
  .header p {{ font-size: 14px; opacity: 0.8; }}
  .container {{ max-width: 1100px; margin: 30px auto; padding: 0 20px; }}
  .card {{ background: white; border-radius: 10px; padding: 24px;
           margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }}
  .card h2 {{ font-size: 16px; color: #1B3A6B; margin-bottom: 16px;
              padding-bottom: 8px; border-bottom: 2px solid #EEF3FA; }}
  .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }}
  .stat {{ text-align: center; padding: 16px; border-radius: 8px; }}
  .stat .num {{ font-size: 36px; font-weight: bold; }}
  .stat .lbl {{ font-size: 12px; margin-top: 4px; opacity: 0.8; }}
  .stat.pass {{ background: #d4edda; color: #155724; }}
  .stat.fail {{ background: #f8d7da; color: #721c24; }}
  .stat.total {{ background: #EEF3FA; color: #1B3A6B; }}
  .stat.rate  {{ background: #fff3cd; color: #856404; }}
  .status-badge {{ display: inline-block; padding: 6px 16px; border-radius: 20px;
                   font-weight: bold; font-size: 13px; color: white;
                   background: {status_color}; margin-bottom: 16px; }}
  .elem-grid {{ display: flex; flex-wrap: wrap; gap: 10px; }}
  .elem-card {{ background: #EEF3FA; border-radius: 8px; padding: 10px 16px;
                text-align: center; min-width: 100px; }}
  .elem-title {{ font-size: 11px; color: #666; text-transform: uppercase; }}
  .elem-count {{ font-size: 24px; font-weight: bold; color: #1B3A6B; }}
  .code-block {{ background: #1a1a2e; color: #abb2bf; font-family: monospace;
                 font-size: 12px; padding: 20px; border-radius: 8px;
                 overflow-x: auto; white-space: pre; max-height: 400px;
                 overflow-y: auto; line-height: 1.6; }}
  .info-row {{ display: flex; gap: 8px; margin-bottom: 8px; font-size: 14px; }}
  .info-label {{ font-weight: bold; color: #1B3A6B; min-width: 100px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ background: #1B3A6B; color: white; padding: 10px; text-align: left; }}
  td {{ padding: 10px; border-bottom: 1px solid #eee; }}
  tr:hover td {{ background: #f8f9fa; }}
  .tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px;
          font-size: 11px; font-weight: bold; }}
  .tag.pass {{ background: #d4edda; color: #155724; }}
  .tag.fail {{ background: #f8d7da; color: #721c24; }}
  img {{ max-width: 100%; border-radius: 8px; border: 1px solid #ddd; }}
  footer {{ text-align: center; padding: 20px; color: #888; font-size: 12px; }}
</style>
</head>
<body>

<div class="header">
  <h1>🤖 AI-Powered Test Generator — Report</h1>
  <p>Generated at: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} &nbsp;|&nbsp;
     Page: {title} &nbsp;|&nbsp; URL: {url}</p>
</div>

<div class="container">

  <!-- Test Run Summary -->
  <div class="card">
    <h2>Test Run Summary</h2>
    <div class="status-badge">{status_text}</div>
    <div class="stats">
      <div class="stat total">
        <div class="num">{total}</div>
        <div class="lbl">Total Tests</div>
      </div>
      <div class="stat pass">
        <div class="num">{passed}</div>
        <div class="lbl">Passed</div>
      </div>
      <div class="stat fail">
        <div class="num">{failed}</div>
        <div class="lbl">Failed</div>
      </div>
      <div class="stat rate">
        <div class="num">{pass_rate}%</div>
        <div class="lbl">Pass Rate</div>
      </div>
    </div>
  </div>

  <!-- Page Analysis -->
  <div class="card">
    <h2>Page Analysis Results</h2>
    <div class="info-row">
      <span class="info-label">URL:</span>
      <span>{url}</span>
    </div>
    <div class="info-row">
      <span class="info-label">Title:</span>
      <span>{title}</span>
    </div>
    <div class="info-row">
      <span class="info-label">AI Generated:</span>
      <span>{test_count} test cases</span>
    </div>
    <div class="info-row">
      <span class="info-label">Duration:</span>
      <span>{duration}s</span>
    </div>
    <br>
    <div class="elem-grid">
      {elements_html}
    </div>
  </div>

  <!-- Screenshot -->
  <div class="card">
    <h2>Page Screenshot</h2>
    <img src="../../{screenshot}" alt="Page Screenshot"
         onerror="this.style.display='none'">
  </div>

  <!-- Generated Code -->
  <div class="card">
    <h2>AI-Generated Test Code</h2>
    <div class="code-block">{code[:3000]}{"..." if len(code) > 3000 else ""}</div>
  </div>

</div>

<footer>
  AI-Powered Test Generator &nbsp;|&nbsp;
  Playwright + Gemini AI + Python &nbsp;|&nbsp;
  Mala Ram Babu
</footer>

</body>
</html>"""
