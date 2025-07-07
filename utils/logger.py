import logging
import os
from pathlib import Path
import colorlog
from config import Config


class TestLogger:
    """Enhanced logging utility for the test framework"""

    def __init__(self, name=__name__):
        self.config = Config()
        self.logger = logging.getLogger(name)
        self.setup_logger()

    def setup_logger(self):
        """Set up logger with file and console handlers"""
        # Clear any existing handlers
        self.logger.handlers.clear()

        # Set log level
        log_level = getattr(logging, self.config.LOG_LEVEL, logging.INFO)
        self.logger.setLevel(log_level)

        # Create logs directory if it doesn't exist
        log_dir = Path(self.config.LOG_FILE_PATH).parent
        log_dir.mkdir(exist_ok=True)

        # File handler with detailed formatting
        if self.config.LOG_TO_FILE:
            file_handler = logging.FileHandler(self.config.LOG_FILE_PATH, mode='a', encoding='utf-8')
            file_formatter = logging.Formatter(
                '%(asctime)s | %(name)s | %(levelname)-8s | %(funcName)s:%(lineno)d | %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            file_handler.setLevel(log_level)
            self.logger.addHandler(file_handler)

        # Console handler with colors
        if self.config.LOG_TO_CONSOLE:
            console_handler = colorlog.StreamHandler()
            console_formatter = colorlog.ColoredFormatter(
                '%(log_color)s%(asctime)s | %(levelname)-8s | %(name)s | %(message)s%(reset)s',
                datefmt='%H:%M:%S',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                }
            )
            console_handler.setFormatter(console_formatter)
            console_handler.setLevel(log_level)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        """Get the configured logger instance"""
        return self.logger

    @staticmethod
    def get_test_logger(test_name: str = None):
        """Get a logger for a specific test"""
        if test_name:
            logger_name = f"test.{test_name}"
        else:
            logger_name = "test"
        return TestLogger(logger_name).get_logger()

    @staticmethod
    def log_test_start(test_name: str, **kwargs):
        """Log test start with details"""
        logger = TestLogger.get_test_logger(test_name)
        logger.info(f"🚀 Starting test: {test_name}")

        if kwargs:
            for key, value in kwargs.items():
                logger.info(f"   {key}: {value}")

    @staticmethod
    def log_test_end(test_name: str, status: str, duration: float = None):
        """Log test end with result"""
        logger = TestLogger.get_test_logger(test_name)

        status_icon = {
            'PASSED': '✅',
            'FAILED': '❌',
            'SKIPPED': '⏭️',
            'ERROR': '💥'
        }.get(status.upper(), '❓')

        message = f"{status_icon} Test {status.lower()}: {test_name}"
        if duration:
            message += f" (Duration: {duration:.2f}s)"

        if status.upper() in ['PASSED', 'SKIPPED']:
            logger.info(message)
        else:
            logger.error(message)

    @staticmethod
    def log_step(step_description: str, test_name: str = None):
        """Log a test step"""
        logger = TestLogger.get_test_logger(test_name)
        logger.info(f"📋 Step: {step_description}")

    @staticmethod
    def log_action(action: str, element: str = None, test_name: str = None):
        """Log a page action"""
        logger = TestLogger.get_test_logger(test_name)
        if element:
            logger.debug(f"🎯 Action: {action} on element '{element}'")
        else:
            logger.debug(f"🎯 Action: {action}")

    @staticmethod
    def log_assertion(assertion: str, result: bool, test_name: str = None):
        """Log an assertion result"""
        logger = TestLogger.get_test_logger(test_name)
        icon = "✅" if result else "❌"
        level = logging.INFO if result else logging.ERROR
        logger.log(level, f"{icon} Assertion: {assertion} - {'PASSED' if result else 'FAILED'}")

    @staticmethod
    def log_error(error_message: str, exception: Exception = None, test_name: str = None):
        """Log an error with optional exception details"""
        logger = TestLogger.get_test_logger(test_name)
        logger.error(f"💥 Error: {error_message}")

        if exception:
            logger.error(f"Exception details: {str(exception)}")
            logger.debug(f"Exception type: {type(exception).__name__}")

    @staticmethod
    def log_screenshot(screenshot_path: str, test_name: str = None):
        """Log screenshot capture"""
        logger = TestLogger.get_test_logger(test_name)
        logger.info(f"📸 Screenshot saved: {screenshot_path}")

    @staticmethod
    def log_browser_info(browser: str, device: str = None, headless: bool = True):
        """Log browser and device information"""
        logger = TestLogger.get_test_logger()
        logger.info(f"🌐 Browser: {browser} | Device: {device or 'Desktop'} | Headless: {headless}")

    @staticmethod
    def clear_log_file():
        """Clear the log file"""
        config = Config()
        try:
            if os.path.exists(config.LOG_FILE_PATH):
                with open(config.LOG_FILE_PATH, 'w') as f:
                    f.write("")
                logger = TestLogger().get_logger()
                logger.info("🧹 Log file cleared")
        except Exception as e:
            print(f"Warning: Could not clear log file: {e}")


# Convenience function for quick access
def get_logger(name: str = None):
    """Quick access to logger"""
    return TestLogger(name or __name__).get_logger()