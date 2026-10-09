import re

import allure
from playwright.sync_api import Dialog, Locator, Page, expect

from constants.locators import HeaderLocators, TicketListLocators as locators
from pages.base_page import BasePage
from pages.notification_page import NotificationPage
from pages.settings_page import SettingsPage
from pages.ticket_detail_dialog import TicketDetailDialog


class TicketListPage(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.last_dialog_type: str | None = None
        self.last_dialog_message: str | None = None

    # -----------------------------------------------------------------------
    # Scoped locators
    # -----------------------------------------------------------------------

    @property
    def panel(self) -> Locator:
        return self.page.locator(locators.PANEL)

    @property
    def rows(self) -> Locator:
        return self.page.locator(locators.TABLE_BODY).get_by_role("row")

    def row_of(self, ticket_id: str) -> Locator:
        # 各行に同じ「詳細」「削除」ボタンがあるため、まずチケットIDで行を特定する（Rules 罠#1）
        return self.rows.filter(has_text=ticket_id)

    def _pagination(self, container: str) -> Locator:
        return self.page.locator(container)

    def _row_checkboxes(self) -> Locator:
        return self.page.locator(locators.TABLE_BODY).get_by_role("checkbox")

    def _select_all_checkbox(self) -> Locator:
        return self.panel.get_by_role("checkbox", name=locators.SELECT_ALL_CHECKBOX_NAME, exact=True)

    # -----------------------------------------------------------------------
    # Navigation (header)
    # -----------------------------------------------------------------------

    @allure.step("Open 通知 tab from header")
    def open_notifications_tab(self) -> NotificationPage:
        self.click_header_tab(HeaderLocators.NAV_TAB_NOTIFICATIONS)
        return NotificationPage(self.page)

    @allure.step("Open 設定 tab from header")
    def open_settings_tab(self) -> SettingsPage:
        self.click_header_tab(HeaderLocators.NAV_TAB_SETTINGS)
        return SettingsPage(self.page)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    @allure.step("Click 次へ in {container}")
    def click_next_page(self, container: str = locators.PAGINATION_TOP) -> None:
        self._pagination(container).get_by_role("button", name=locators.NEXT_BUTTON_NAME, exact=True).click()

    @allure.step("Check 全て選択 checkbox")
    def check_select_all(self) -> None:
        # 本物の <input> は opacity:0 で .cb-box の下にある → input に直接 check()（Rules 罠#1）
        self._select_all_checkbox().check()

    @allure.step("Select priority filter: {priority}")
    def select_priority(self, priority: str) -> None:
        self.panel.get_by_label(locators.PRIORITY_FILTER_LABEL, exact=True).select_option(value=priority)

    @allure.step("Type keyword '{keyword}' into search box")
    def fill_search_keyword(self, keyword: str) -> None:
        self.panel.get_by_placeholder(locators.SEARCH_PLACEHOLDER, exact=True).fill(keyword)

    @allure.step("Press Enter in search box")
    def press_enter_in_search(self) -> None:
        self.panel.get_by_placeholder(locators.SEARCH_PLACEHOLDER, exact=True).press("Enter")

    @allure.step("Click 検索 button")
    def click_search_button(self) -> None:
        self.panel.get_by_role("button", name=locators.SEARCH_BUTTON_NAME, exact=True).click()

    @allure.step("Hover help icon next to 作成日 header")
    def hover_created_date_help_icon(self) -> None:
        self.page.locator(locators.CREATED_HEADER).locator(locators.CREATED_TOOLTIP_TRIGGER).hover()

    @allure.step("Delete ticket {ticket_id} and {action} the confirm dialog")
    def delete_ticket(self, ticket_id: str, action: str = "accept") -> None:
        def _handle(dialog: Dialog) -> None:
            self.last_dialog_type = dialog.type
            self.last_dialog_message = dialog.message
            dialog.accept() if action == "accept" else dialog.dismiss()

        # ネイティブ confirm はクリック前にハンドラ登録が必要
        self.page.once("dialog", _handle)
        self.row_of(ticket_id).get_by_role("button", name=locators.DELETE_BUTTON_NAME, exact=True).click()

    @allure.step("Open detail dialog of ticket {ticket_id}")
    def open_detail(self, ticket_id: str) -> TicketDetailDialog:
        self.row_of(ticket_id).get_by_role("button", name=locators.DETAIL_BUTTON_NAME, exact=True).click()
        detail = TicketDetailDialog(self.page)
        detail.expect_opened()
        return detail

    @allure.step("Apply status '{status}' inside embedded preview iframe")
    def apply_status_in_iframe(self, status: str) -> None:
        frame = self.page.frame_locator(locators.PREVIEW_IFRAME)
        frame.get_by_role("combobox").select_option(label=status)
        frame.get_by_role("button", name=locators.FRAME_APPLY_BUTTON_NAME, exact=True).click()

    @allure.step("Open print preview in a new window")
    def open_print_preview(self) -> Page:
        with self.page.expect_popup() as popup_info:
            self.click_by_role("button", locators.PRINT_PREVIEW_BUTTON_NAME)
        popup = popup_info.value
        popup.wait_for_load_state()
        return popup

    # -----------------------------------------------------------------------
    # Getters
    # -----------------------------------------------------------------------

    def visible_ticket_ids(self) -> list[str]:
        ids: list[str] = []
        for row in self.rows.all():
            ids.append(row.get_attribute("data-id") or "")
        return ids

    def visible_priorities(self) -> list[str]:
        return self.page.locator(locators.TABLE_BODY).locator(locators.PRIORITY_CHIP).all_inner_texts()

    def layout_elements(self) -> dict[str, Locator]:
        """Others_01: チケット一覧画面の主要UI要素."""
        elements = self.header_layout_elements()
        elements.update({
            "新規チケット作成ボタン": self.panel.get_by_role("button", name=locators.NEW_TICKET_BUTTON_NAME),
            "検索欄": self.panel.get_by_placeholder(locators.SEARCH_PLACEHOLDER, exact=True),
            "検索ボタン": self.panel.get_by_role("button", name=locators.SEARCH_BUTTON_NAME, exact=True),
            "テーブル領域": self.panel.locator(locators.TABLE_WRAP),
        })
        return elements

    # -----------------------------------------------------------------------
    # Assertions
    # -----------------------------------------------------------------------

    @allure.step("Expect ticket list shows {count} row(s)")
    def expect_row_count(self, count: int) -> None:
        expect(self.rows).to_have_count(count)

    @allure.step("Expect page {page_no} is active in {container}")
    def expect_active_page(self, page_no: int, container: str = locators.PAGINATION_TOP) -> None:
        expect(
            self._pagination(container).get_by_role("button", name=str(page_no), exact=True)
        ).to_have_class(re.compile(locators.PAGE_BUTTON_ACTIVE_CLASS))

    @allure.step("Expect 前へ is enabled in top and bottom pagination")
    def expect_prev_enabled(self) -> None:
        for container in (locators.PAGINATION_TOP, locators.PAGINATION_BOTTOM):
            expect(
                self._pagination(container).get_by_role("button", name=locators.PREV_BUTTON_NAME, exact=True)
            ).to_be_enabled()

    @allure.step("Expect 前へ is disabled in top and bottom pagination")
    def expect_prev_disabled(self) -> None:
        for container in (locators.PAGINATION_TOP, locators.PAGINATION_BOTTOM):
            expect(
                self._pagination(container).get_by_role("button", name=locators.PREV_BUTTON_NAME, exact=True)
            ).to_be_disabled()

    @allure.step("Expect all row checkboxes are checked")
    def expect_all_rows_checked(self, expected_count: int) -> None:
        checkboxes = self._row_checkboxes()
        expect(checkboxes).to_have_count(expected_count)
        for checkbox in checkboxes.all():
            expect(checkbox).to_be_checked()
        expect(self._select_all_checkbox()).to_be_checked()

    @allure.step("Expect bulk action bar is displayed with '{selected_text}'")
    def expect_bulk_bar_visible(self, selected_text: str) -> None:
        expect(self.page.locator(locators.BULK_ACTION_BAR)).to_be_visible()
        expect(self.page.locator(locators.SELECTED_COUNT)).to_have_text(selected_text)

    @allure.step("Expect tooltip '{text}' is NOT displayed")
    def expect_tooltip_hidden(self, text: str) -> None:
        tooltip = self.page.locator(locators.CREATED_HEADER).locator(locators.CREATED_TOOLTIP_CONTENT)
        expect(tooltip).to_be_hidden()
        expect(tooltip).to_have_text(text)

    @allure.step("Expect tooltip '{text}' is displayed")
    def expect_tooltip_visible(self, text: str) -> None:
        tooltip = self.page.locator(locators.CREATED_HEADER).locator(locators.CREATED_TOOLTIP_CONTENT)
        expect(tooltip).to_be_visible()
        expect(tooltip).to_have_text(text)

    @allure.step("Expect ticket {ticket_id} is NOT in the list")
    def expect_ticket_absent(self, ticket_id: str) -> None:
        expect(self.row_of(ticket_id)).to_have_count(0)

    @allure.step("Expect ticket {ticket_id} has status '{status}'")
    def expect_ticket_status(self, ticket_id: str, status: str) -> None:
        expect(self.row_of(ticket_id).locator(locators.STATUS_CHIP)).to_have_text(status)

    @allure.step("Expect iframe result message '{message}'")
    def expect_iframe_result(self, message: str) -> None:
        frame = self.page.frame_locator(locators.PREVIEW_IFRAME)
        expect(frame.locator(locators.FRAME_RESULT)).to_have_text(message)

    @allure.step("Expect message '{message}' is NOT rendered in parent page")
    def expect_text_not_in_parent_page(self, message: str) -> None:
        expect(self.page.get_by_text(message)).to_have_count(0)

    @allure.step("Expect popup window shows '{title}' and '{count_text}'")
    def expect_print_preview_popup(self, popup: Page, title: str, count_text: str) -> None:
        assert popup is not self.page, "Print preview did not open in a new window"
        expect(popup.get_by_role("heading", name=title, exact=True)).to_be_visible()
        expect(popup.get_by_text(count_text, exact=True)).to_be_visible()
