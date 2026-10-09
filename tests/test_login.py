import allure

from constants.messages import LOGIN_ERROR_MESSAGE
from helpers import description_md
from pages.login_page import LoginPage
from testdata.test_data import WRONG_PASSWORD


@allure.feature("ログイン画面")
@allure.story("GD02.8-Assertion")
@description_md("Test cases GD02.8-04 in Automation_Finnal_Project — シート: Testcases_Quynh")
class Testログイン画面:

    @allure.title("GD02.8-04: Wrong password shows login error and stays on login screen")
    @description_md(
        """
- **前提条件**: ログイン画面を表示中
- **テスト手順**:
  1. IDに「admin」を入力する
  2. パスワードに「wrongpass」を入力する
  3. 「ログイン」ボタンを押下する
- **期待する結果**: 「IDまたはパスワードが正しくありません。」というエラーメッセージが表示され、画面遷移しない
        """
    )
    def test_login_with_wrong_password_shows_error_and_stays_on_login(
        self, access_to_login_screen: LoginPage, admin_credentials: tuple[str, str]
    ):
        admin_id, _ = admin_credentials
        access_to_login_screen.login(admin_id, WRONG_PASSWORD)

        access_to_login_screen.expect_login_error(LOGIN_ERROR_MESSAGE)
        access_to_login_screen.expect_still_on_login_screen()

        with allure.step("[PASSED] Error message is shown and screen does not change"):
            pass
