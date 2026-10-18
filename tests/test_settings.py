import allure

from constants.messages import SIGNATURE_COUNTER_TEMPLATE
from helpers import description_md
from pages.settings_page import SettingsPage
from testdata.test_data import SIGNATURE_MAX_LENGTH


@allure.feature("設定画面")
@allure.story("GD02.3-Fill")
@description_md("Test cases GD02.3-001 in Automation_Finnal_Project — シート: Testcases_Quynh")
class Test設定画面:

    @allure.title("GD02.3-001: Signature accepts max 100 chars and counter stops at 100/100文字")
    @description_md(
        """
- **前提条件**: 設定画面を表示中
- **テスト手順**: 1. 署名欄に100文字を超えるテキストを入力しようとする
- **期待する結果**: 最大100文字までしか入力できず、カウンター表示が「100/100文字」で止まる
        """
    )
    def test_signature_over_max_length_is_truncated_and_counter_stops(
        self, access_to_settings_screen: SettingsPage
    ):
        #over_length_text = access_to_settings_screen.random_chars(SIGNATURE_OVER_LENGTH)
        ###NNTT: nếu được nên tách hàm random_chars ra hàm riêng để test, mục đích để ở report allure sẽ hiển thị được là mình đã nhập bao nhiêu text ở đó. 
        ###Ngoài ra sẽ tốt hơn nếu viết hàm random vượt quá số lượng SIGNATURE_MAX_LENGTH thay vì phải tạo thêm 1 biến quy định SIGNATURE_MAX_LENGTH 

        over_length_text = access_to_settings_screen.random_text_over_max(SIGNATURE_MAX_LENGTH)
        access_to_settings_screen.type_signature(over_length_text)

        access_to_settings_screen.expect_signature_truncated(over_length_text, SIGNATURE_MAX_LENGTH)
        access_to_settings_screen.expect_signature_counter(
            SIGNATURE_COUNTER_TEMPLATE.format(count=SIGNATURE_MAX_LENGTH)
        )

        with allure.step("[PASSED] Only 100 chars are accepted and counter shows 100/100文字"):
            pass
