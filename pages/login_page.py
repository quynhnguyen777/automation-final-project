import allure
from playwright.sync_api import Page, expect

from constants.locators import HeaderLocators, LoginLocators as locators
from pages.base_page import BasePage


class LoginPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    @allure.step("Login with ID '{login_id}'")
    def login(self, login_id: str, password: str) -> None:
        self.fill_by_label(locators.ID_LABEL, login_id)
        self.fill_by_label(locators.PASSWORD_LABEL, password)
        self.click_by_role("button", locators.LOGIN_BUTTON_NAME)

    @allure.step("Login and wait until main screen is displayed")
    def login_successfully(self, login_id: str, password: str) -> None:
        self.login(login_id, password)
        expect(self.page.locator(HeaderLocators.MAIN_SECTION)).to_be_visible()

    # -----------------------------------------------------------------------
    # Assertions
    # -----------------------------------------------------------------------

    @allure.step("Expect login error message '{message}' is displayed")
    def expect_login_error(self, message: str) -> None:
        expect(self.page.locator(locators.LOGIN_ERROR)).to_be_visible()
        expect(self.page.locator(locators.LOGIN_ERROR)).to_have_text(message)

    @allure.step("Expect still on login screen (no transition to main screen)")
    def expect_still_on_login_screen(self) -> None:
        expect(self.page.locator(locators.LOGIN_SECTION)).to_be_visible()
        expect(self.page.get_by_role("button", name=locators.LOGIN_BUTTON_NAME, exact=True)).to_be_visible()
        expect(self.page.locator(HeaderLocators.MAIN_SECTION)).to_be_hidden()
