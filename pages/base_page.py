from playwright.sync_api import Page, expect
from config import Config
from utils.logger import TestLogger


class BasePage:
    """Base page class that all page objects inherit from"""

    def __init__(self, page: Page):
        self.page = page
        self.config = Config()
        self.logger = TestLogger.get_test_logger(self.__class__.__name__)

    def navigate_to(self, url: str = None):
        """Navigate to a URL or base URL"""
        target_url = url or self.config.BASE_URL
        self.logger.info(f"🌐 Navigating to: {target_url}")
        self.page.goto(target_url)
        TestLogger.log_action(f"Navigate to {target_url}")

    def wait_for_page_load(self):
        """Wait for the page to load completely"""
        self.logger.debug("⏳ Waiting for page to load...")
        self.page.wait_for_load_state('networkidle')
        TestLogger.log_action("Page loaded completely")

    def click_element(self, selector: str):
        """Click an element by selector"""
        self.logger.debug(f"🖱️ Clicking element: {selector}")
        try:
            self.page.click(selector)
            TestLogger.log_action("Click", selector)
        except Exception as e:
            TestLogger.log_error(f"Failed to click element: {selector}", e)
            raise

    def fill_input(self, selector: str, text: str):
        """Fill an input field"""
        self.logger.debug(f"⌨️ Filling input {selector} with: {text}")
        try:
            self.page.fill(selector, text)
            TestLogger.log_action(f"Fill input with '{text}'", selector)
        except Exception as e:
            TestLogger.log_error(f"Failed to fill input: {selector}", e)
            raise

    def get_text(self, selector: str) -> str:
        """Get text content of an element"""
        self.logger.debug(f"📝 Getting text from: {selector}")
        try:
            text = self.page.locator(selector).text_content()
            TestLogger.log_action(f"Get text: '{text}'", selector)
            return text
        except Exception as e:
            TestLogger.log_error(f"Failed to get text from: {selector}", e)
            raise

    def is_element_visible(self, selector: str) -> bool:
        """Check if element is visible"""
        try:
            visible = self.page.locator(selector).is_visible()
            self.logger.debug(f"👁️ Element {selector} visible: {visible}")
            return visible
        except Exception as e:
            self.logger.debug(f"Element {selector} not found or error: {e}")
            return False

    def wait_for_element(self, selector: str, timeout: int = None):
        """Wait for element to be visible"""
        timeout = timeout or self.config.TIMEOUT
        self.logger.debug(f"⏱️ Waiting for element: {selector} (timeout: {timeout}ms)")
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            TestLogger.log_action(f"Element appeared", selector)
        except Exception as e:
            TestLogger.log_error(f"Element did not appear within timeout: {selector}", e)
            raise

    def take_screenshot(self, name: str = "screenshot"):
        """Take a screenshot"""
        screenshot_path = f"screenshots/{name}.png"
        self.logger.info(f"📸 Taking screenshot: {screenshot_path}")
        try:
            self.page.screenshot(path=screenshot_path)
            TestLogger.log_screenshot(screenshot_path)
        except Exception as e:
            TestLogger.log_error(f"Failed to take screenshot: {screenshot_path}", e)

    def get_page_title(self) -> str:
        """Get the page title"""
        title = self.page.title()
        self.logger.debug(f"📄 Page title: {title}")
        return title