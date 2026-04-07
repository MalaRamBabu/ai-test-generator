# AI-Powered Test Generator

Give it a URL → AI analyses the page → generates Playwright tests → runs them → HTML report.

Built with **Playwright + Google Gemini AI + Python + PyTest**.

---

## How It Works

```
URL Input
   ↓
Step 1: Playwright opens page → captures screenshot + extracts all elements
        (inputs, buttons, forms, tables, links, file uploads)
   ↓
Step 2: Gemini AI analyses the elements → generates Playwright test cases
        (login, navigation, form validation, table data, file upload tests)
   ↓
Step 3: Generated test code saved to output/generated_tests/
   ↓
Step 4: PyTest runs the generated tests automatically
   ↓
Step 5: HTML report generated with pass/fail results + screenshot
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.11 | Programming language |
| Playwright | Browser automation + screenshot capture |
| Google Gemini AI | Test case generation from page analysis |
| PyTest | Test execution framework |
| OpenCV / NumPy | Visual validation |
| GitHub Actions | CI/CD pipeline |

---

## Project Structure

```
ai_test_generator/
├── core/
│   └── page_analyser.py         # Playwright page element extraction
├── generator/
│   ├── gemini_generator.py      # Gemini AI test generation
│   └── test_file_writer.py      # Save generated tests to file
├── runner/
│   └── test_runner.py           # PyTest execution
├── reporter/
│   └── report_generator.py      # HTML report generation
├── output/
│   ├── generated_tests/         # AI-generated .py test files
│   ├── screenshots/             # Page screenshots
│   └── reports/                 # HTML reports
├── .github/workflows/
│   └── ai_generator.yml         # GitHub Actions CI/CD
├── main.py                      # Entry point
├── requirements.txt
└── README.md
```

---

## Setup & Run

### 1. Clone the repository
```bash
git clone https://github.com/MalaRamBabu/ai-test-generator.git
cd ai-test-generator
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 3. Set Gemini API key
```bash
# Windows CMD
set GEMINI_API_KEY=your_api_key_here

# Mac / Linux
export GEMINI_API_KEY=your_api_key_here
```
Get free key: https://aistudio.google.com

### 4. Run the generator
```bash
# Generate and run tests for login page
python main.py --url https://automationexercise.com/login --name login

# Generate only, don't run yet
python main.py --url https://automationexercise.com --name home --skip-run

# Products page
python main.py --url https://automationexercise.com/products --name products
```

### 5. View results
```
output/
├── generated_tests/test_login_20240101_120000.py  ← AI-generated tests
├── screenshots/login.png                           ← Page screenshot
└── reports/ai_test_report_login_*.html             ← Full HTML report
```

---

## Example Output

```
╔══════════════════════════════════════════════════════╗
║  AI-POWERED TEST GENERATOR                           ║
╠══════════════════════════════════════════════════════╣
║  URL Analysed   : https://automationexercise.com/login
║  Tests Generated: 12
║  Tests Passed   : 10
║  Tests Failed   : 2
╚══════════════════════════════════════════════════════╝
```

---

## CI/CD — GitHub Actions
On every push: generates tests for login page, runs them, uploads report as artifact.
API key stored as GitHub Secret — never exposed in code.

---

## Author

**Mala Ram Babu**
Senior QA Automation Engineer | 4+ Years Experience
[LinkedIn](https://www.linkedin.com/in/mala-ram-babu) | [GitHub](https://github.com/MalaRamBabu)
