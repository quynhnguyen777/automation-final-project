import allure
from playwright.sync_api import Locator, Page, expect

from constants.locators import TicketDetailLocators as locators
from pages.base_page import BasePage


class TicketDetailDialog(BasePage):

    def __init__(self, page: Page) -> None:
        super().__init__(page)

    @property
    def dialog(self) -> Locator:
        return self.page.get_by_role("dialog", name=locators.DIALOG_NAME)

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    @allure.step("Upload file '{file_name}' ({size_bytes} bytes) to drop zone")
    def upload_file(self, file_name: str, mime_type: str, size_bytes: int) -> None:
        # input[type=file] は display:none → クリックで OS ダイアログを開かず、
        # set_input_files で直接ファイルを渡す（Rules 罠#2）
        self.dialog.locator(locators.FILE_INPUT).set_input_files(
            files=[{"name": file_name, "mimeType": mime_type, "buffer": self._dummy_bytes(size_bytes)}]
        )

    @staticmethod
    def _dummy_bytes(size_bytes: int) -> bytes:
        png_signature = b"\x89PNG\r\n\x1a\n"
        return png_signature + b"\x00" * (size_bytes - len(png_signature))

    # -----------------------------------------------------------------------
    # Assertions
    # -----------------------------------------------------------------------

    @allure.step("Expect detail dialog is displayed")
    def expect_opened(self) -> None:
        expect(self.dialog).to_be_visible()

    @allure.step("Expect file preview shows '{expected_text}'")
    def expect_file_preview(self, expected_text: str) -> None:
        expect(self.dialog.locator(locators.FILE_NAME)).to_be_visible()
        expect(self.dialog.locator(locators.FILE_NAME)).to_have_text(expected_text)

    @allure.step("Expect remove-file icon is displayed")
    def expect_remove_file_icon_visible(self) -> None:
        expect(self.dialog.get_by_role("button", name=locators.REMOVE_FILE_BUTTON_NAME, exact=True)).to_be_visible()

    @allure.step("Expect no file error is displayed")
    def expect_no_file_error(self) -> None:
        expect(self.dialog.locator(locators.FILE_ERROR)).to_be_hidden()
