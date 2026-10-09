import allure
from playwright.sync_api import Locator, Page, expect

from constants.locators import SettingsLocators as locators
from pages.base_page import BasePage


class SettingsPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @property
    def signature(self) -> Locator:
        return self.page.locator(locators.PANEL).get_by_placeholder(locators.SIGNATURE_PLACEHOLDER, exact=True)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    @allure.step("Type text into 署名")
    def type_signature(self, text: str) -> None:
        # 「入力しようとする」→ キー入力として1文字ずつ送る（maxlength の挙動を実際の入力で確認）
        self.signature.press_sequentially(text)

    # -----------------------------------------------------------------------
    # Assertions
    # -----------------------------------------------------------------------

    @allure.step("Expect 設定 screen is displayed")
    def expect_screen_displayed(self) -> None:
        expect(self.page.locator(locators.PANEL)).to_be_visible()

    @allure.step("Expect 署名 keeps only the first {max_length} characters")
    def expect_signature_truncated(self, typed_text: str, max_length: int) -> None:
        expect(self.signature).to_have_value(typed_text[:max_length])

    @allure.step("Expect 署名 counter shows '{text}'")
    def expect_signature_counter(self, text: str) -> None:
        expect(self.page.locator(locators.SIGNATURE_COUNTER)).to_have_text(text)
