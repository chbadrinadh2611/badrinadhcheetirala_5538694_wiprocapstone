# Nykaa BDD Automation Framework

Enterprise-grade BDD test automation for Nykaa Baby Care using Python, Behave, Selenium, and Allure Reports.

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core language |
| Behave | BDD framework |
| Selenium | Browser automation |
| Allure | Reporting |
| WebDriverManager | Driver management |
| CSV | Data-driven tests |
| Page Object Model | Architecture |

---

## Project Structure

```
BDD/
├── config/              # Configuration
├── features/
│   ├── positive/        # Positive test scenarios
│   ├── negative/        # Negative test scenarios
│   ├── e2e/             # End-to-end scenarios
│   ├── steps/           # Step definitions
│   └── environment.py   # Behave hooks
├── pages/               # Page Objects + Locators
├── testdata/            # CSV test data
├── utils/               # Helpers (logger, waits, screenshots, csv)
├── reports/             # Screenshots + Allure results
├── logs/                # Execution logs
├── behave.ini
├── requirements.txt
└── run_tests.py
```

---

## Setup

### 1. Create virtual environment
```bash
python -m venv .venv
```

### 2. Activate
```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Allure CLI
```bash
# Mac
brew install allure

# Windows (Scoop)
scoop install allure
```

---

## Run Tests

```bash
python run_tests.py
```

This will:
1. Clean previous allure-results
2. Execute all Behave scenarios
3. Generate Allure HTML report
4. Open the report automatically in your browser

---

## Run Specific Tags

```bash
# Positive only
behave --tags=positive

# Smoke tests
behave --tags=smoke

# E2E only
behave --tags=e2e

# Brand filter only
behave --tags=brand
```

---

## Test Coverage

### Positive Tests
- Brand filter: Mamaearth, Himalaya, Cetaphil
- Rating filter: 4 Stars & Above, 3 Stars & Above
- Product validation: URL, title, product count, card display

### Negative Tests
- Invalid brand search
- Unavailable filter combinations
- Empty search result handling

### E2E Tests
- Add to Cart flow
- Guest Checkout flow

---

## Reports

| Artifact | Location |
|----------|----------|
| Allure Results | `reports/allure-results/` |
| Allure Report | `reports/allure-report/` |
| Screenshots | `reports/screenshots/` |
| Logs | `logs/execution.log` |

---

## CSV Data

`testdata/testdata.csv` drives brand and rating test combinations:

```csv
brand,rating
Mamaearth,4 Stars & Above
Himalaya,3 Stars & Above
Cetaphil,4 Stars & Above
```
