from pages.base_page import BasePage
from playwright.sync_api import expect


class LoginPage(BasePage):
    """Login page object following Page Object Model"""

    def __init__(self, page):
        super().__init__(page)

        # Page elements
        self.product_logo = ".login_logo"
        self.username_input = "#user-name"
        self.password_input = "#password"
        self.login_button = "#login-button"
        self.req_error = "//h3[@data-test='error']"
        self.product_title = "//*[@data-test='title']"

    def open(self):
        """Open the login page"""
        login_url = f"{self.config.BASE_URL}"
        self.navigate_to(login_url)
        self.wait_for_page_load()
        return self

    def enter_username(self, username):
        self.wait_for_element(self.username_input)
        self.fill_input(self.username_input, username)

    def enter_password(self, password):
        self.wait_for_element(self.password_input)
        self.fill_input(self.password_input, password)

    def click_login_button(self):
        self.click_element(self.login_button)

    def verify_login_page_loaded(self):
        expect(self.page).to_have_url(f"{self.config.BASE_URL}")

        # Check if login form elements are visible
        if self.is_element_visible(self.username_input):
            expect(self.page.locator(self.username_input)).to_be_visible()
        if self.is_element_visible(self.password_input):
            expect(self.page.locator(self.password_input)).to_be_visible()

        return self

    def login(self, email: str = None, password: str = None):
        """Perform login with credentials"""
        username = email or self.config.TEST_USER
        password = password or self.config.TEST_PASSWORD

        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()

        return self

    def get_error_message(self) -> str:
        """Get error message if present"""
        if self.is_element_visible(self.req_error):
            return self.get_text(self.req_error)
        return ""

    def is_login_successful(self) -> bool:
        """Check if login was successful"""
        # Check if we're redirected away from login page
        self.is_element_visible(self.product_title)  # Wait a bit for redirect
        current_url = self.page.url
        return "/inventory.html" in current_url
