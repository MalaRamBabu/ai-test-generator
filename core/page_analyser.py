import os
import json
from playwright.sync_api import sync_playwright


class PageAnalyser:
    """
    Step 1: Opens a URL with Playwright.
    Captures screenshot and extracts all interactive elements
    (forms, buttons, inputs, links, tables) from the page.
    This data is sent to Gemini AI for test case generation.
    """

    SCREENSHOTS_DIR = "output/screenshots"

    def __init__(self):
        os.makedirs(self.SCREENSHOTS_DIR, exist_ok=True)

    def analyse(self, url, page_name="page"):
        """
        Full page analysis:
        - Opens URL in browser
        - Takes screenshot
        - Extracts all interactive elements
        - Returns structured analysis dict
        """
        print(f"\n[PageAnalyser] Analysing: {url}")

        with sync_playwright() as p:
<<<<<<< HEAD
            browser = p.chromium.launch(headless=False)
=======
            browser = p.chromium.launch(headless=True)
>>>>>>> c221bcef957e7aa598125f97e4af93d22424f819
            context = browser.new_context(
                viewport={"width": 1280, "height": 720}
            )
            page = context.new_page()

            # Navigate
            page.goto(url, wait_until="networkidle", timeout=30000)
            page_title = page.title()

            # Screenshot
            screenshot_path = os.path.join(
                self.SCREENSHOTS_DIR, f"{page_name}.png"
            )
            page.screenshot(path=screenshot_path, full_page=False)

            # Extract elements
            elements = self._extract_elements(page)

            browser.close()

        analysis = {
            "url":             url,
            "page_name":       page_name,
            "title":           page_title,
            "screenshot_path": screenshot_path,
            "elements":        elements,
        }

        print(f"[PageAnalyser] Title: {page_title}")
        print(f"[PageAnalyser] Found: {self._count_summary(elements)}")
        return analysis

    def _extract_elements(self, page):
        """Extract all interactive elements from the page"""
        elements = {}

        # ── Input Fields ──────────────────────────────────────────────────────
        elements["inputs"] = page.evaluate("""
            () => Array.from(document.querySelectorAll('input')).map(el => ({
                type:        el.type || 'text',
                name:        el.name || '',
                id:          el.id   || '',
                placeholder: el.placeholder || '',
                required:    el.required,
                value:       el.value || ''
            })).filter(el => el.type !== 'hidden')
        """)

        # ── Buttons ───────────────────────────────────────────────────────────
        elements["buttons"] = page.evaluate("""
            () => Array.from(document.querySelectorAll(
                'button, input[type="submit"], input[type="button"], a.btn'
            )).map(el => ({
                text:  (el.innerText || el.value || '').trim().substring(0, 50),
                type:  el.type  || 'button',
                id:    el.id    || '',
                class: el.className || ''
            })).filter(el => el.text !== '')
        """)

        # ── Links / Navigation ────────────────────────────────────────────────
        elements["links"] = page.evaluate("""
            () => Array.from(document.querySelectorAll('nav a, header a, .navbar a'))
            .map(el => ({
                text: (el.innerText || '').trim().substring(0, 40),
                href: el.href || ''
            })).filter(el => el.text !== '' && el.href !== '')
            .slice(0, 15)
        """)

        # ── Forms ─────────────────────────────────────────────────────────────
        elements["forms"] = page.evaluate("""
<<<<<<< HEAD
        () => {
            return Array.from(document.querySelectorAll("form")).map(f => ({
                action: f.action || "",
                method: f.method || "",
                id: f.id || "",
                name: f.name || ""
            }));
        }
=======
            () => Array.from(document.querySelectorAll('form')).map((form, i) => ({
                id:     form.id     || f'form_{i}',
                action: form.action || '',
                method: form.method || 'get',
                fields: Array.from(form.querySelectorAll('input, textarea, select'))
                    .map(f => f.name || f.id || f.placeholder || f.type)
                    .filter(Boolean)
            }))
>>>>>>> c221bcef957e7aa598125f97e4af93d22424f819
        """)

        # ── Tables ────────────────────────────────────────────────────────────
        elements["tables"] = page.evaluate("""
            () => Array.from(document.querySelectorAll('table')).map((table, i) => ({
                index:   i,
                headers: Array.from(table.querySelectorAll('th'))
                    .map(th => th.innerText.trim()).filter(Boolean),
                rows:    table.querySelectorAll('tr').length
            }))
        """)

        # ── File Inputs ───────────────────────────────────────────────────────
        elements["file_inputs"] = page.evaluate("""
            () => Array.from(document.querySelectorAll('input[type="file"]'))
            .map(el => ({
                name:   el.name   || '',
                id:     el.id     || '',
                accept: el.accept || ''
            }))
        """)

        # ── Page headings (for context) ───────────────────────────────────────
        elements["headings"] = page.evaluate("""
            () => Array.from(document.querySelectorAll('h1, h2, h3'))
            .map(h => h.innerText.trim())
            .filter(Boolean)
            .slice(0, 8)
        """)

        return elements

    def _count_summary(self, elements):
        """Generate a readable summary of found elements"""
        return (
            f"{len(elements.get('inputs', []))} inputs, "
            f"{len(elements.get('buttons', []))} buttons, "
            f"{len(elements.get('links', []))} nav links, "
            f"{len(elements.get('forms', []))} forms, "
            f"{len(elements.get('tables', []))} tables"
        )
