import allure

from constants.messages import NOTIFICATION_NOT_FOUND_TEMPLATE
from helpers import description_md
from pages.notification_page import NotificationPage
from testdata.test_data import NOT_EXIST_KEYWORD


@allure.feature("通知画面")
@allure.story("GD02.1-Click (get-or-create)")
@description_md("Test cases GD02.1-01 in Automation_Finnal_Project — シート: Testcases_Quynh")
class Test通知画面:

    @allure.title("GD02.1-01: 0-result search → ＋通知を作成する opens the create modal")
    @description_md(
        """
- **前提条件**: 通知一覧画面を表示中
- **テスト手順**:
  1. 存在しないキーワードで検索する
  2. 「検索条件に一致する通知が見つかりません」の下にある「＋通知を作成する」ボタンを押下する
- **期待する結果**: 通知作成モーダルが開く（ツールバーの作成ボタンと同じ動作）
        """
    )
    def test_notification_empty_result_create_button_opens_modal(
        self, access_to_notification_screen: NotificationPage
    ):
        notification = access_to_notification_screen

        notification.search(NOT_EXIST_KEYWORD)
        notification.expect_empty_message(NOTIFICATION_NOT_FOUND_TEMPLATE.format(keyword=NOT_EXIST_KEYWORD))
        notification.click_create_from_empty_result()

        notification.expect_create_modal_opened()

        with allure.step("[PASSED] Notification create modal is opened from the empty-result button"):
            pass

    @allure.title("Rules_08: ensure_notification_exists creates once, then only finds it")
    @description_md(
        """
- **前提条件**: 通知一覧画面を表示中（sheet Rules - mục 8: get-or-create pattern）
- **テスト手順**:
  1. ensure_notification_exists(タイトル) を呼ぶ（存在しない → 新規作成）
  2. 同じタイトルでもう一度呼ぶ（存在する → 何もしない）
- **期待する結果**: 1回目は作成され、2回目は作成されず、一覧に同タイトルの通知が1件だけ存在する
        """
    )
    def test_ensure_notification_exists_creates_only_when_missing(
        self, access_to_notification_screen: NotificationPage
    ):
        notification = access_to_notification_screen
        title = f"自動テスト通知_{notification.random_chars(6)}"

        created_first = notification.ensure_notification_exists(title, "get-or-create パターン確認")
        created_second = notification.ensure_notification_exists(title, "get-or-create パターン確認")

        assert created_first is True, "First call should create the notification"
        assert created_second is False, "Second call should find the existing notification"
        notification.search(title)
        notification.expect_notification_present(title)

        with allure.step("[PASSED] Notification is created once and found on the second call"):
            pass
