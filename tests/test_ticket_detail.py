import allure

from constants.messages import FILE_PREVIEW_TEMPLATE
from helpers import description_md
from pages.ticket_list_page import TicketListPage
from testdata.test_data import TARGET_TICKET_ID, UPLOAD_PNG_NAME, UPLOAD_PNG_SIZE_BYTES


@allure.feature("チケット詳細ダイアログ")
@allure.story("GD02.7-FileUpload")
@description_md("Test cases GD02.7-01 in Automation_Finnal_Project — シート: Testcases_Quynh")
class Testチケット詳細ダイアログ:

    @allure.title("GD02.7-01: Upload ~1MB .png shows file name, size and delete icon")
    @description_md(
        """
- **前提条件**: 詳細ダイアログを表示中
- **テスト手順**: 1. ドロップゾーンに.pngファイル（1MB程度）をアップロードする
- **期待する結果**: ファイル名とサイズがプレビュー表示され、削除アイコンが表示される
        """
    )
    def test_detail_upload_png_shows_preview_and_delete_icon(
        self, access_to_ticket_list_screen: TicketListPage
    ):
        detail = access_to_ticket_list_screen.open_detail(TARGET_TICKET_ID)

        detail.upload_file(UPLOAD_PNG_NAME, "image/png", UPLOAD_PNG_SIZE_BYTES)

        detail.expect_file_preview(
            FILE_PREVIEW_TEMPLATE.format(name=UPLOAD_PNG_NAME, size_kb=UPLOAD_PNG_SIZE_BYTES // 1024)
        )
        detail.expect_remove_file_icon_visible()
        detail.expect_no_file_error()

        with allure.step("[PASSED] File name + size preview and delete icon are displayed"):
            pass
