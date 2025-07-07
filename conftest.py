import pytest
from playwright.sync_api import sync_playwright
from config import Config
from utils.logger import TestLogger
import os
import time


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    """Set up logging for the test session"""
    # Clear previous log file at the start of the session
    TestLogger.clear_log_file()

    # Log session start
    logger = TestLogger().get_logger()
    logger.info("=" * 80)
    logger.info("🚀 Starting Test Session")
    logger.info("=" * 80)

    config = Config()
    TestLogger.log_browser_info(config.BROWSER, config.DEVICE, config.HEADLESS)

    yield

    # Log session end
    logger.info("=" * 80)
    logger.info("✅ Test Session Completed")
    logger.info("=" * 80)


@pytest.fixture(autouse=True)
def log_test_execution(request):
    """Log test execution details"""
    test_name = request.node.name
    test_class = request.node.cls.__name__ if request.node.cls else "standalone"

    # Log test start
    TestLogger.log_test_start(
        test_name,
        test_class=test_class,
        test_file=request.node.fspath.basename
    )

    start_time = time.time()

    yield

    # Log test end with duration
    duration = time.time() - start_time

    # Determine test outcome
    if hasattr(request.node, 'rep_call'):
        if request.node.rep_call.passed:
            status = "PASSED"
        elif request.node.rep_call.failed:
            status = "FAILED"
        elif request.node.rep_call.skipped:
            status = "SKIPPED"
        else:
            status = "ERROR"
    else:
        status = "UNKNOWN"

    TestLogger.log_test_end(test_name, status, duration)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for logging"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture(scope="session")
def playwright():
    """Playwright fixture for the entire test session"""
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser_type(playwright):
    """Get browser type based on config"""
    config = Config()
    if config.BROWSER == 'firefox':
        return playwright.firefox
    elif config.BROWSER == 'webkit':
        return playwright.webkit
    else:
        return playwright.chromium


@pytest.fixture(scope="session")
def browser(browser_type):
    """Browser fixture for the entire test session"""
    config = Config()
    browser = browser_type.launch(
        headless=config.HEADLESS,
        slow_mo=50 if not config.HEADLESS else 0
    )
    yield browser
    browser.close()


@pytest.fixture(scope="function")
def context(browser, playwright):
    """Browser context fixture for each test"""
    config = Config()

    # Set up device emulation if specified
    context_options = {
        'viewport': {'width': 1920, 'height': 1080},
        'ignore_https_errors': True,
        'record_video_dir': 'test-results/videos/' if os.getenv('RECORD_VIDEO') else None
    }

    # Apply device emulation if specified
    if config.DEVICE and config.DEVICE in config.DEVICES and config.DEVICES[config.DEVICE]:
        device_name = config.DEVICES[config.DEVICE]
        if device_name in playwright.devices:
            device = playwright.devices[device_name]
            context_options.update(device)

    context = browser.new_context(**context_options)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """Page fixture for each test"""
    page = context.new_page()

    # Set default timeout
    config = Config()
    page.set_default_timeout(config.TIMEOUT)

    yield page
    page.close()


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Set up test environment before each test"""
    # Create directories if they don't exist
    os.makedirs('screenshots', exist_ok=True)
    os.makedirs('test-results', exist_ok=True)
    os.makedirs('test-results/videos', exist_ok=True)
    os.makedirs('logs', exist_ok=True)

    yield

    # Cleanup after test if needed
    pass


def pytest_configure(config):
    """Configure pytest"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    # Add markers based on test names
    for item in items:
        if "smoke" in item.name.lower():
            item.add_marker(pytest.mark.smoke)
        if "login" in item.name.lower():
            item.add_marker(pytest.mark.regression)