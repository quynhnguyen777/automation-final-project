import allure

from helpers import description_md
from pages.notification_page import NotificationPage
from testdata.test_data import ADMIN_TOTAL_NOTIFICATIONS


@allure.feature("ヘッダー・画面遷移")
@allure.story("GD01-Navigation")
@description_md("Test cases GD01_004 in Automation_Finnal_Project — シート: Testcases_Quynh")
class Test通知画面_遷移:

    @allure.title("GD01_004: Click 通知 tab navigates to notification list with 3 items")
    @description_md(
        """
- **前提条件**: admin/admin123でログイン済み
- **テスト手順**: 1. ヘッダーの「通知」タブを押下する
- **期待する結果**: 通知一覧画面に遷移し、3件の通知が表示される
        """
    )
    def test_notification_tab_click_shows_three_notifications(
        self, access_to_notification_screen: NotificationPage
    ):
        # fixture: admin ログイン → 「通知」タブ押下 → 画面表示＋タブ active を確認済み
        access_to_notification_screen.expect_screen_displayed()
        access_to_notification_screen.expect_row_count(ADMIN_TOTAL_NOTIFICATIONS)

        with allure.step("[PASSED] 通知一覧 is displayed with 3 notifications"):
            pass
