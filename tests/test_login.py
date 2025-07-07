import pytest
from pages.login_page import LoginPage
from utils.logger import TestLogger

class TestLoginPage:

    @pytest.mark.smoke
    def test_login_page_loads_successfully(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.verify_login_page_loaded()


    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.login()

        assert login_page.is_login_successful() is True

    @pytest.mark.smoke
    def test_login_with_invalid_credentials(self, page):
        login_page = LoginPage(page)
        login_page.open()
        login_page.enter_username("standard_user")
        login_page.click_login_button()

        assert "Password is required" in login_page.get_error_message()
