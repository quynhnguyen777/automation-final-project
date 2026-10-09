import allure
import pytest

from helpers import description_md
from pages.ticket_list_page import TicketListPage
from testdata.test_data import VIEWPORTS


@allure.feature("UI・表示")
@allure.story("Others")
@description_md("Test cases Others_01 in Automation_Finnal_Project — シート: Testcases_Quynh")
class TestUI表示_レイアウト:

    @allure.title("Others_01: Layout check on different screen sizes")
    @description_md(
        """
- **前提条件**: チケット一覧画面を表示中
- **テスト手順**:
  1. 異なる解像度・アスペクト比の実端末または実ブラウザで画面を表示する
  2. ヘッダー、テーブル、ボタン、ダイアログ等を確認する
- **期待する結果**: 重要なUI要素が画面外にはみ出さず、重なりや表示崩れが発生しない
- **自動化の範囲**: 実端末の代わりに Chromium の viewport を変更してエミュレートする
        """
    )
    @pytest.mark.parametrize("viewport_name", list(VIEWPORTS.keys()))
    def test_ticket_list_layout_has_no_overflow_or_overlap(
        self, access_to_ticket_list_screen: TicketListPage, viewport_name: str
    ):
        ticket_list = access_to_ticket_list_screen
        size = VIEWPORTS[viewport_name]

        ticket_list.resize_viewport(size["width"], size["height"])

        with allure.step(f"Check elements are inside viewport ({viewport_name})"):
            outside = ticket_list.elements_outside_viewport(ticket_list.layout_elements())
        with allure.step(f"Check header elements fit inside the header height ({viewport_name})"):
            out_of_header = ticket_list.elements_outside_container(
                ticket_list.header_container(), ticket_list.header_inner_elements()
            )
        with allure.step(f"Check header elements do not overlap ({viewport_name})"):
            overlaps = ticket_list.overlapping_pairs(ticket_list.header_inner_elements())
        with allure.step(f"Check page has no horizontal scroll ({viewport_name})"):
            has_scroll = ticket_list.has_horizontal_page_scroll()

        problems = []
        if outside:
            problems.append(f"outside viewport: {outside}")
        if out_of_header:
            problems.append(f"overflowing header: {out_of_header}")
        if overlaps:
            problems.append(f"overlapping: {overlaps}")
        if has_scroll:
            problems.append("page has horizontal scroll")
        assert not problems, f"Layout broken at {viewport_name}: " + "; ".join(problems)

        with allure.step(f"[PASSED] No overflow / overlap at {viewport_name}"):
            pass
