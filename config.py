import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Configuration settings for the test framework"""

    # Base URLs
    BASE_URL = os.getenv('BASE_URL', 'https://example.com')

    # Timeouts
    try:
        TIMEOUT = int(os.getenv('TIMEOUT', '30000'))
    except ValueError:
        TIMEOUT = 30000

    # Browser settings
    BROWSER = os.getenv('BROWSER', 'chromium')
    HEADLESS = os.getenv('HEADLESS', 'true').lower() in ('true', '1', 'yes', 'on')
    DEVICE = os.getenv('DEVICE', 'Desktop Chrome')

    # Test environment
    TEST_ENV = os.getenv('TEST_ENV', 'dev')
    TEST_USER = os.getenv('TEST_USER', 'standard_user')
    TEST_PASSWORD = os.getenv('TEST_PASSWORD', 'secret_sauce')

    # Logging configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
    LOG_TO_FILE = os.getenv('LOG_TO_FILE', 'true').lower() in ('true', '1', 'yes', 'on')
    LOG_TO_CONSOLE = os.getenv('LOG_TO_CONSOLE', 'true').lower() in ('true', '1', 'yes', 'on')
    LOG_FILE_PATH = os.getenv('LOG_FILE_PATH', 'logs/test_execution.log')

    # Supported browsers
    BROWSERS = ['chromium', 'firefox', 'webkit']

    # Common devices for testing
    DEVICES = {
        'Desktop Chrome': None,
        'iPhone 12': 'iPhone 12',
        'iPad': 'iPad',
        'Pixel 5': 'Pixel 5'
    }