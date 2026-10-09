import allure

from constants.locators import TicketListLocators
from constants.messages import (
    CREATED_DATE_TOOLTIP,
    DELETE_CONFIRM_MESSAGE,
    IFRAME_RESULT_TEMPLATE,
    PRINT_PREVIEW_COUNT_TEMPLATE,
    PRINT_PREVIEW_TITLE,
    SELECTED_COUNT_TEMPLATE,
    TICKET_DELETED_TOAST,
)
from helpers import description_md
from pages.ticket_list_page import TicketListPage
from testdata.test_data import (
    ADMIN_TOTAL_TICKETS,
    DEFAULT_PER_PAGE,
    IFRAME_STATUS_TO_APPLY,
    PAGE_2_ROW_COUNT,
    PRIORITY_HIGH,
    PRIORITY_HIGH_COUNT,
    SEARCH_KEYWORD_LOGIN,
    SEARCH_LOGIN_EXPECTED_COUNT,
    TARGET_TICKET_ID,
    TARGET_TICKET_STATUS,
)


@allure.feature("チケット一覧画面")
@allure.story("Click / Check / SelectOption / Hover / Keyboard / Dialog / Iframe / TabWindow")
@description_md(
    "Test cases GD02.1-02, GD02.2-001, GD02.4-02, GD02.5-001, GD02.6-02, GD03.1-01, GD03.2-01, "
    "GD03.3-01 in Automation_Finnal_Project — シート: Testcases_Quynh"
)
class Testチケット一覧:

    # -------------------------------------------------------------------
    # GD02.1-Click
    # -------------------------------------------------------------------
    @allure.title("GD02.1-02: Click 次へ shows page 2 (2 items) and enables 前へ")
    @description_md(
        """
- **前提条件**: 1ページの表示件数が10件（デフォルト）
- **テスト手順**: 1. 「次へ」ボタンを押下する
- **期待する結果**: 2ページ目（残り2件）が表示され、「前へ」ボタンが活性化する
        """
    )
    def test_pagination_click_next_shows_page_two_and_enables_prev(
        self, access_to_ticket_list_screen: TicketListPage
    ):
        ticket_list = access_to_ticket_list_screen
        with allure.step("Precondition: page 1 shows 10 items and 前へ is disabled"):
            ticket_list.expect_row_count(DEFAULT_PER_PAGE)
            ticket_list.expect_prev_disabled()

        # 「次へ」は上下2箇所にある → 上部ページネーションに scope して押下
        ticket_list.click_next_page(TicketListLocators.PAGINATION_TOP)

        ticket_list.expect_row_count(PAGE_2_ROW_COUNT)
        ticket_list.expect_active_page(2)
        ticket_list.expect_prev_enabled()

        with allure.step("[PASSED] Page 2 shows remaining 2 items and 前へ is enabled"):
            pass

    # -------------------------------------------------------------------
    # GD02.2-Check
    # -------------------------------------------------------------------
    @allure.title("GD02.2-001: Select-all checkbox checks every row and shows bulk action bar")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**: 1. テーブルヘッダーの全選択チェックボックスを押下する
- **期待する結果**: 表示中の全行のチェックボックスがチェックされ、一括操作バーが表示される
        """
    )
    def test_select_all_checkbox_checks_all_rows_and_shows_bulk_bar(
        self, access_to_ticket_list_screen: TicketListPage
    ):
        ticket_list = access_to_ticket_list_screen

        ticket_list.check_select_all()

        ticket_list.expect_all_rows_checked(DEFAULT_PER_PAGE)
        ticket_list.expect_bulk_bar_visible(SELECTED_COUNT_TEMPLATE.format(count=DEFAULT_PER_PAGE))

        with allure.step("[PASSED] All 10 visible rows are checked and bulk action bar is displayed"):
            pass

    # -------------------------------------------------------------------
    # GD02.4-SelectOption
    # -------------------------------------------------------------------
    @allure.title("GD02.4-02: Priority filter 高 shows only 5 high-priority tickets")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**: 1. 優先度プルダウンで「高」を選択する
- **期待する結果**: 優先度が「高」のチケットのみ表示される（5件）
        """
    )
    def test_priority_filter_high_shows_only_high_priority_tickets(
        self, access_to_ticket_list_screen: TicketListPage
    ):
        ticket_list = access_to_ticket_list_screen

        ticket_list.select_priority(PRIORITY_HIGH)

        ticket_list.expect_row_count(PRIORITY_HIGH_COUNT)
        priorities = ticket_list.visible_priorities()
        assert priorities == [PRIORITY_HIGH] * PRIORITY_HIGH_COUNT, (
            f"Priorities shown are {priorities}, expected only '{PRIORITY_HIGH}'"
        )

        with allure.step("[PASSED] Only 5 tickets with priority 高 are displayed"):
            pass

    # -------------------------------------------------------------------
    # GD02.5-Hover
    # -------------------------------------------------------------------
    @allure.title("GD02.5-001: Hover 作成日 help icon shows tooltip text")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**: 1. 「作成日」列見出し横のヘルプアイコン（?）にカーソルを合わせる
- **期待する結果**: 「チケットが作成された日付を表示します」という説明テキストが表示される
        """
    )
    def test_created_date_help_icon_hover_shows_tooltip(
        self, access_to_ticket_list_screen: TicketListPage
    ):
        ticket_list = access_to_ticket_list_screen
        with allure.step("Precondition: tooltip is hidden before hover"):
            ticket_list.expect_tooltip_hidden(CREATED_DATE_TOOLTIP)

        ticket_list.hover_created_date_help_icon()

        ticket_list.expect_tooltip_visible(CREATED_DATE_TOOLTIP)

        with allure.step("[PASSED] Tooltip text is displayed on hover"):
            pass

    # -------------------------------------------------------------------
    # GD02.6-Keyboard
    # -------------------------------------------------------------------
    @allure.title("GD02.6-02: Enter key in search box gives same result as 検索 button")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**:
  1. 検索欄に「ログイン」と入力する
  2. Enterキーを押下する
- **期待する結果**: 「検索」ボタン押下時と同じ結果が表示される
        """
    )
    def test_search_with_enter_key_matches_search_button_result(
        self, access_to_ticket_list_screen: TicketListPage
    ):
        ticket_list = access_to_ticket_list_screen

        ticket_list.fill_search_keyword(SEARCH_KEYWORD_LOGIN)
        ticket_list.press_enter_in_search()
        ticket_list.expect_row_count(SEARCH_LOGIN_EXPECTED_COUNT)
        ids_by_enter = ticket_list.visible_ticket_ids()

        with allure.step("Compare with result of 検索 button (same keyword)"):
            ticket_list.click_search_button()
            ticket_list.expect_row_count(SEARCH_LOGIN_EXPECTED_COUNT)
            ids_by_button = ticket_list.visible_ticket_ids()

        assert ids_by_enter == ids_by_button, (
            f"Result by Enter {ids_by_enter} differs from result by 検索 button {ids_by_button}"
        )

        with allure.step("[PASSED] Enter key returns the same 1 result as 検索 button"):
            pass

    # -------------------------------------------------------------------
    # GD03.1-Dialog
    # -------------------------------------------------------------------
    @allure.title("GD03.1-01: Delete row and accept confirm removes row and shows toast")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**:
  1. 任意の行の「削除」ボタンを押下する
  2. 確認ダイアログ（confirm）で「OK」を押下する
- **期待する結果**: 該当行が一覧から削除され、トースト通知「チケットを削除しました。」が表示される
        """
    )
    def test_delete_ticket_accept_confirm_removes_row_and_shows_toast(
        self, access_to_ticket_list_screen: TicketListPage
    ):
        ticket_list = access_to_ticket_list_screen

        ticket_list.delete_ticket(TARGET_TICKET_ID, action="accept")

        ticket_list.expect_toast(TICKET_DELETED_TOAST)
        ticket_list.expect_ticket_absent(TARGET_TICKET_ID)
        assert ticket_list.last_dialog_type == "confirm", (
            f"Dialog type is {ticket_list.last_dialog_type}, expected 'confirm'"
        )
        assert ticket_list.last_dialog_message == DELETE_CONFIRM_MESSAGE, (
            f"Confirm message is '{ticket_list.last_dialog_message}'"
        )

        with allure.step("[PASSED] Row is deleted and toast チケットを削除しました。 is displayed"):
            pass

    # -------------------------------------------------------------------
    # GD03.2-Iframe
    # -------------------------------------------------------------------
    @allure.title("GD03.2-01: Apply status inside iframe shows result only in iframe")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**:
  1. 埋め込みプレビュー内のプルダウンでステータスを選択する
  2. 埋め込みプレビュー内の「適用」ボタンを押下する
- **期待する結果**: iframe内にのみ結果メッセージが表示され、親ページの一覧には影響しない
        """
    )
    def test_iframe_apply_status_shows_result_only_inside_iframe(
        self, access_to_ticket_list_screen: TicketListPage
    ):
        ticket_list = access_to_ticket_list_screen
        expected_message = IFRAME_RESULT_TEMPLATE.format(status=IFRAME_STATUS_TO_APPLY)
        ids_before = ticket_list.visible_ticket_ids()

        ticket_list.apply_status_in_iframe(IFRAME_STATUS_TO_APPLY)

        ticket_list.expect_iframe_result(expected_message)
        with allure.step("Parent page list is not affected"):
            ticket_list.expect_text_not_in_parent_page(expected_message)
            ticket_list.expect_ticket_status(TARGET_TICKET_ID, TARGET_TICKET_STATUS)
            assert ticket_list.visible_ticket_ids() == ids_before, "Parent ticket list changed after iframe apply"

        with allure.step("[PASSED] Result message is shown only inside iframe; parent list unchanged"):
            pass

    # -------------------------------------------------------------------
    # GD03.3-TabWindow
    # -------------------------------------------------------------------
    @allure.title("GD03.3-01: Print preview opens new popup window with ticket count")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**: 1. 「印刷プレビューを開く（新しいウィンドウ）」ボタンを押下する
- **期待する結果**: 新しいポップアップウィンドウが開き、印刷プレビュー内容（対象チケット数）が表示される
        """
    )
    def test_print_preview_opens_popup_with_ticket_count(
        self, access_to_ticket_list_screen: TicketListPage
    ):
        ticket_list = access_to_ticket_list_screen

        popup = ticket_list.open_print_preview()

        ticket_list.expect_print_preview_popup(
            popup,
            PRINT_PREVIEW_TITLE,
            PRINT_PREVIEW_COUNT_TEMPLATE.format(count=ADMIN_TOTAL_TICKETS),
        )
        popup.close()

        with allure.step("[PASSED] Popup window shows 印刷プレビュー with 対象チケット数：12件"):
            pass
