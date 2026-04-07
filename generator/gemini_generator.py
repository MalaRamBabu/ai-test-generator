import os
import re
import json
import requests


class GeminiTestGenerator:
    """
    Step 2: Sends page analysis to Google Gemini AI.
    Gemini analyses the page structure and generates
    Playwright test cases covering all key scenarios.
    """

    API_URL = (
    "https://generativelanguage.googleapis.com"
    "/v1beta/models/gemini-2.5-flash:generateContent"
)

    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY not set!\n"
                "Windows: set GEMINI_API_KEY=your_key\n"
                "Mac/Linux: export GEMINI_API_KEY=your_key"
            )


    def generate_tests(self, page_analysis):
        """
        Takes page analysis dict and returns
        generated Playwright test code as a string.
        """
        url       = page_analysis["url"]
        title     = page_analysis["title"]
        elements  = page_analysis["elements"]

        print(f"\n[GeminiGenerator] Generating tests for: {title}")

        prompt = self._build_prompt(url, title, elements)
        code   = self._call_gemini(prompt)
        code   = self._clean_code(code)

        print(f"[GeminiGenerator] Generated {self._count_tests(code)} test cases")
        return code

    def _build_prompt(self, url, title, elements):
        """Build a detailed prompt for Gemini to generate test cases"""

        inputs      = elements.get("inputs",      [])
        buttons     = elements.get("buttons",     [])
        links       = elements.get("links",       [])
        forms       = elements.get("forms",       [])
        tables      = elements.get("tables",      [])
        file_inputs = elements.get("file_inputs", [])
        headings    = elements.get("headings",    [])

        return f"""
You are an expert QA automation engineer. Generate professional Playwright Python test cases.

PAGE INFORMATION:
- URL: {url}
- Title: {title}
- Headings: {headings}

ELEMENTS FOUND ON PAGE:
- Input fields: {json.dumps(inputs[:10], indent=2)}
- Buttons: {json.dumps(buttons[:10], indent=2)}
- Navigation links: {json.dumps(links[:10], indent=2)}
- Forms: {json.dumps(forms[:5], indent=2)}
- Tables: {json.dumps(tables[:3], indent=2)}
- File inputs: {json.dumps(file_inputs[:3], indent=2)}

INSTRUCTIONS:
Generate a complete Python file with Playwright test cases using PyTest.
Follow these rules STRICTLY:

1. Use Page Object Model — create a simple PageObject class at the top
2. Each test must have a clear docstring explaining what it tests
3. Cover these scenario types:
   - Page load and title verification
   - Navigation tests (if nav links found)
   - Form validation — empty fields, invalid inputs
   - Form submission flows
   - Button click tests
   - Table data validation (if tables found)
   - File upload tests (if file inputs found)
   - Positive and negative test cases
4. Use pytest fixtures — page fixture using Playwright sync API
5. Add clear comments in code
6. Use data-qa attributes OR fallback to CSS selectors
7. Handle page load waits properly
8. Generate minimum 10 test cases maximum 15 test cases

OUTPUT FORMAT — Return ONLY Python code, no explanation, no markdown, no backticks:

import pytest
from playwright.sync_api import sync_playwright

# (rest of the code)
"""

    def _call_gemini(self, prompt):
        url = f"{self.API_URL}?key={self.api_key}"

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 4096,
            }
        }

        response = requests.post(url, json=payload, timeout=60)

        if response.status_code != 200:
            print("ERROR RESPONSE:", response.text)
            response.raise_for_status()

        data = response.json()

        return data["candidates"][0]["content"]["parts"][0]["text"]

    def _clean_code(self, code):
        """Remove markdown code blocks if Gemini added them"""
        code = re.sub(r"```python\s*", "", code)
        code = re.sub(r"```\s*",       "", code)
        return code.strip()

    def _count_tests(self, code):
        """Count number of test functions generated"""
        return len(re.findall(r"def test_", code))
