import re

import allure
from playwright.sync_api import Locator, Page, expect

from constants.locators import HeaderLocators, NotificationLocators as locators
from pages.base_page import BasePage


class NotificationPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @property
    def panel(self) -> Locator:
        return self.page.locator(locators.PANEL)

    @property
    def rows(self) -> Locator:
        return self.page.locator(locators.TABLE_BODY).get_by_role("row")

    def row_with_title(self, title: str) -> Locator:
        # filter(has_text=title) だと 0件メッセージ「…見つかりません（title）。」の行にも
        # マッチしてしまうため、タイトルのセルが完全一致する行に限定する
        return self.rows.filter(has=self.page.get_by_role("cell", name=title, exact=True))

    @property
    def create_modal(self) -> Locator:
        return self.page.get_by_role("dialog", name=locators.CREATE_MODAL_NAME)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    @allure.step("Search notifications by keyword '{keyword}'")
    def search(self, keyword: str) -> None:
        self.panel.get_by_placeholder(locators.SEARCH_PLACEHOLDER, exact=True).fill(keyword)
        self.panel.get_by_role("button", name=locators.SEARCH_BUTTON_NAME, exact=True).click()

    @allure.step("Click ＋通知を作成する under the empty-result message")
    def click_create_from_empty_result(self) -> None:
        self.panel.get_by_role("button", name=locators.CREATE_FROM_EMPTY_BUTTON_NAME, exact=True).click()

    @allure.step("Ensure notification '{title}' exists (get-or-create)")
    def ensure_notification_exists(self, title: str, content: str) -> bool:
        """Pattern get-or-create (sheet Rules - muc 8).

        1. Tim kiem tieu de trong danh sach thong bao
        2. Neu khong thay → bam 「＋通知を作成する」 ngay duoi message 0件 de tao moi
        3. Neu da thay → khong lam gi them

        Tra ve True neu vua tao moi, False neu da ton tai san.
        """
        self.search(title)
        if self.row_with_title(title).count() > 0:
            return False

        self.click_create_from_empty_result()
        expect(self.create_modal).to_be_visible()
        self.create_modal.get_by_placeholder(locators.MODAL_TITLE_PLACEHOLDER, exact=True).fill(title)
        self.create_modal.get_by_placeholder(locators.MODAL_CONTENT_PLACEHOLDER, exact=True).fill(content)
        self.create_modal.get_by_role("button", name=locators.MODAL_SUBMIT_BUTTON_NAME, exact=True).click()
        expect(self.create_modal).to_be_hidden()
        return True

    # -----------------------------------------------------------------------
    # Assertions
    # -----------------------------------------------------------------------

    @allure.step("Expect 通知一覧 screen is displayed and 通知 tab is active")
    def expect_screen_displayed(self) -> None:
        expect(self.panel).to_be_visible()
        expect(self.panel.get_by_role("heading", name=locators.HEADING_NAME, exact=True)).to_be_visible()
        expect(self.page.locator(HeaderLocators.NAV_TAB_NOTIFICATIONS)).to_have_class(
            re.compile(HeaderLocators.NAV_TAB_ACTIVE_CLASS)
        )

    @allure.step("Expect notification list shows {count} row(s)")
    def expect_row_count(self, count: int) -> None:
        expect(self.rows).to_have_count(count)

    @allure.step("Expect empty-result message '{message}'")
    def expect_empty_message(self, message: str) -> None:
        expect(self.panel.get_by_text(message, exact=True)).to_be_visible()

    @allure.step("Expect notification create modal is opened")
    def expect_create_modal_opened(self) -> None:
        expect(self.create_modal).to_be_visible()

    @allure.step("Expect notification '{title}' is in the list")
    def expect_notification_present(self, title: str) -> None:
        expect(self.row_with_title(title)).to_have_count(1)
