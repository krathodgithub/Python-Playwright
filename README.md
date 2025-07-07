# Playwright Test Framework

A simple, beginner-friendly Python + Playwright test automation framework with Page Object Model (POM), parallel execution, and comprehensive reporting.

## Features

- ✅ **Page Object Model (POM)** - Clean, maintainable test structure
- ✅ **Parallel Test Execution** - Run tests faster with pytest-xdist
- ✅ **Multi-browser Support** - Chrome, Firefox, Safari/WebKit
- ✅ **Device Emulation** - Test on different devices and screen sizes
- ✅ **HTML Reports** - Beautiful test reports with pytest-html
- ✅ **Screenshots** - Automatic screenshots on test execution
- ✅ **Environment Configuration** - Easy configuration with .env files
- ✅ **Test Runner** - Simple command-line test runner

## Quick Start

### 1. Install Dependencies

```bash
# Install Python packages and Playwright browsers
python test_runner.py --install
```

### 2. Run Tests

```bash
# Run all tests
python test_runner.py

# Run tests in parallel
python test_runner.py --parallel

# Run specific test markers
python test_runner.py --markers smoke

# Run with specific browser
python test_runner.py --browser firefox

# Run in headless mode
python test_runner.py --headless true
```

## Project Structure

```
playwright-framework/
├── pages/                  # Page Object Model classes
│   ├── base_page.py       # Base page with common methods
│   ├── home_page.py       # Home page object
│   └── login_page.py      # Login page object
├── tests/                 # Test files
│   ├── test_home_page.py  # Home page tests
│   └── test_login_page.py # Login page tests
├── test-results/          # Test reports and artifacts
├── screenshots/           # Test screenshots
├── .env                   # Environment variables
├── config.py              # Configuration settings
├── conftest.py            # Pytest configuration and fixtures
├── pytest.ini             # Pytest settings
├── requirements.txt       # Python dependencies
├── test_runner.py           # Test runner script
└── README.md              # This file
```

## Configuration

### Environment Variables (.env)

```bash
# Test Configuration
BASE_URL=https://example.com
TIMEOUT=30000
HEADLESS=true

# Browser Configuration
BROWSER=chromium
DEVICE=Desktop Chrome

# Test Environment
TEST_ENV=dev
TEST_USER=testuser@example.com
TEST_PASSWORD=testpassword123
```

### Supported Browsers
- **chromium** - Chrome/Chromium
- **firefox** - Firefox
- **webkit** - Safari/WebKit

### Supported Devices
- **Desktop Chrome** - Standard desktop
- **iPhone 12** - Mobile iPhone
- **iPad** - Tablet iPad
- **Pixel 5** - Mobile Android

## Running Tests

### Basic Commands

```bash
# Run all tests
python test_runner.py

# Run tests in parallel (auto-detect CPU cores)
python test_runner.py --parallel

# Run tests with 4 workers
python test_runner.py --parallel --workers 4

# Run only smoke tests
python test_runner.py --markers smoke

# Run only regression tests
python test_runner.py --markers regression

# Run specific test file
python test_runner.py --test-file tests/test_home_page.py
```

### Browser and Device Options

```bash
# Run tests in Firefox
python test_runner.py --browser firefox

# Run tests in WebKit (Safari)
python test_runner.py --browser webkit

# Run tests with iPhone 12 emulation
python test_runner.py --device "iPhone 12"

# Run tests in headed mode (see browser)
python test_runner.py --headless false
```

### Advanced Options

```bash
# Run tests with Allure reporting
python test_runner.py --allure

# Combine multiple options
python test_runner.py --parallel --browser firefox --markers smoke --headless false
```

## Direct Pytest Commands

You can also run tests directly with pytest:

```bash
# Basic test run
pytest tests/ -v

# Run in parallel
pytest tests/ -n auto

# Run with HTML report
pytest tests/ --html=test-results/report.html

# Run specific markers
pytest tests/ -m smoke

# Run with specific browser (set environment variable)
BROWSER=firefox pytest tests/ -v
```

## Test Reports

### HTML Reports
- Generated automatically at: `test-results/report.html`
- Self-contained HTML file with test results, logs, and screenshots

### JUnit XML Reports
- Generated at: `test-results/junit.xml`
- Compatible with CI/CD systems

### Screenshots
- Automatically saved to: `screenshots/`
- Captured during test execution for debugging

## Writing Tests

### Basic Test Structure

```python
import pytest
from pages.home_page import HomePage

class TestHomePage:
    def test_home_page_loads(self, page):
        # Arrange
        home_page = HomePage(page)
        
        # Act
        home_page.open()
        
        # Assert
        home_page.verify_page_loaded()
```

### Using Page Objects

```python
from pages.login_page import LoginPage

def test_login_functionality(page):
    # Create page object
    login_page = LoginPage(page)
    
    # Use page methods
    login_page.open()
    login_page.login("user@example.com", "password")
    
    # Assert results
    assert login_page.is_login_successful()
```

### Test Markers

```python
@pytest.mark.smoke
def test_critical_functionality(page):
    # This test will run when using --markers smoke
    pass

@pytest.mark.regression
def test_detailed_functionality(page):
    # This test will run when using --markers regression
    pass
```

## Adding New Tests

### 1. Create New Page Object

```python
# pages/new_page.py
from pages.base_page import BasePage

class NewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.element_selector = "[data-testid='element']"
    
    def perform_action(self):
        self.click_element(self.element_selector)
        return self
```

### 2. Create Test File

```python
# tests/test_new_page.py
import pytest
from pages.new_page import NewPage

class TestNewPage:
    def test_new_functionality(self, page):
        new_page = NewPage(page)
        new_page.open()
        new_page.perform_action()
        # Add assertions
```

## Troubleshooting

### Common Issues

1. **Browser not found**
   ```bash
   # Install Playwright browsers
   python -m playwright install
   ```

2. **Tests failing due to timeouts**
   - Increase timeout in `.env` file: `TIMEOUT=60000`
   - Or use `--headless false` to debug visually

3. **Element not found**
   - Check element selectors in page objects
   - Use `page.pause()` for debugging
   - Take screenshots to verify page state

### Debug Mode

```bash
# Run in headed mode to see browser
python test_runner.py --headless false

# Run single test for debugging
python test_runner.py --test-file tests/test_home_page.py::TestHomePage::test_home_page_loads
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Playwright Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    - name: Install dependencies
      run: python test_runner.py --install
    - name: Run tests
      run: python test_runner.py --parallel
    - name: Upload test results
      uses: actions/upload-artifact@v3
      if: always()
      with:
        name: test-results
        path: test-results/
```

## Best Practices

1. **Use Page Object Model** - Keep test logic separate from page interactions
2. **Use Data-TestId** - Prefer `data-testid` attributes for stable element selection
3. **Keep Tests Independent** - Each test should be able to run in isolation
4. **Use Meaningful Names** - Test and method names should be descriptive
5. **Take Screenshots** - Capture screenshots for debugging and documentation
6. **Use Fixtures** - Leverage pytest fixtures for test setup and teardown

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License.