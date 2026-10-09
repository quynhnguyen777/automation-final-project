import random
import string

import allure
from playwright.sync_api import Locator, Page, expect

from constants.locators import CommonLocators, HeaderLocators


class BasePage:
    """Base cho moi Page Object — chi giu cac ham dung chung cho >= 2 man hinh."""

    def __init__(self, page: Page) -> None:
        self.page = page

    # -----------------------------------------------------------------------
    # Navigation
    # -----------------------------------------------------------------------

    @allure.step("Navigate to URL: {url}")
    def navigate_to(self, url: str) -> None:
        self.page.goto(url)
        self.page.wait_for_load_state("domcontentloaded")

    # -----------------------------------------------------------------------
    # Interaction
    # -----------------------------------------------------------------------

    @allure.step("Click element: {selector}")
    def click(self, selector: str) -> None:
        self.page.locator(selector).click()

    @allure.step("Click by role '{role}' with name '{name}'")
    def click_by_role(self, role: str, name: str, exact: bool = True) -> None:
        self.page.get_by_role(role, name=name, exact=exact).click()

    @allure.step("Fill placeholder '{placeholder}' with value")
    def fill_by_placeholder(self, placeholder: str, value: str) -> None:
        self.page.get_by_placeholder(placeholder, exact=True).fill(value)

    @allure.step("Fill label '{label}' with value")
    def fill_by_label(self, label: str, value: str) -> None:
        self.page.get_by_label(label, exact=True).fill(value)

    @allure.step("Resize viewport to {width}x{height}")
    def resize_viewport(self, width: int, height: int) -> None:
        self.page.set_viewport_size({"width": width, "height": height})

    @allure.step("Click header tab: {tab_selector}")
    def click_header_tab(self, tab_selector: str) -> None:
        # nav-tab は <li> で role 無し → id で指定（Rules 4: 優先度3）
        self.page.locator(tab_selector).click()

    def header_layout_elements(self) -> dict[str, Locator]:
        """Others_01: ヘッダー内の主要要素（レイアウト確認用）."""
        return {
            "ヘッダー": self.page.locator(HeaderLocators.APP_HEADER),
            "ロゴ": self.page.locator(HeaderLocators.APP_LOGO),
            "タブ一覧": self.page.locator(HeaderLocators.NAV_TABS),
            "ユーザーメニュー": self.page.locator(HeaderLocators.USER_MENU_ACTIVATOR),
        }

    def header_inner_elements(self) -> dict[str, Locator]:
        """Others_01: ヘッダー内の要素同士（ロゴ / タブ / ユーザーメニュー）の重なり確認用."""
        elements = self.header_layout_elements()
        elements.pop("ヘッダー")
        return elements

    def header_container(self) -> Locator:
        return self.page.locator(HeaderLocators.APP_HEADER)

    # -----------------------------------------------------------------------
    # Assertions
    # -----------------------------------------------------------------------

    @allure.step("Expect element visible: {selector}")
    def expect_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).to_be_visible()

    @allure.step("Expect element NOT visible: {selector}")
    def expect_not_visible(self, selector: str) -> None:
        expect(self.page.locator(selector)).not_to_be_visible()

    @allure.step("Expect toast '{message}' is displayed")
    def expect_toast(self, message: str) -> None:
        expect(self.page.locator(CommonLocators.TOAST_CONTAINER).get_by_text(message, exact=True)).to_be_visible()

    # -----------------------------------------------------------------------
    # Helpers
    # -----------------------------------------------------------------------

    @staticmethod
    def random_chars(length: int) -> str:
        """Random chuoi (Nhat + Viet + ASCII) cho test do dai — khong hardcode 'A' * n."""
        pool = "自動化テストあいうえおかきくけこ" + "Kiểm thử tự động" + string.ascii_letters + string.digits
        return "".join(random.choice(pool) for _ in range(length))

    def elements_outside_viewport(self, named_locators: dict[str, Locator]) -> list[str]:
        """Tra ve ten cac phan tu bi tran ra ngoai chieu ngang viewport."""
        viewport_width = self.page.viewport_size["width"]
        outside: list[str] = []
        for name, locator in named_locators.items():
            box = locator.bounding_box()
            if box is None:
                outside.append(f"{name} (not rendered)")
                continue
            if box["x"] < 0 or box["x"] + box["width"] > viewport_width + 0.5:
                outside.append(
                    f"{name} (x={box['x']:.0f}, right={box['x'] + box['width']:.0f}, viewport={viewport_width})"
                )
        return outside

    def elements_outside_container(self, container: Locator, named_locators: dict[str, Locator]) -> list[str]:
        """Tra ve ten cac phan tu tran ra ngoai container theo chieu doc (vd: chu bi xuong dong, vuot chieu cao header)."""
        outer = container.bounding_box()
        outside: list[str] = []
        if outer is None:
            return ["container (not rendered)"]
        for name, locator in named_locators.items():
            box = locator.bounding_box()
            if box is None:
                continue
            if box["y"] < outer["y"] - 0.5 or box["y"] + box["height"] > outer["y"] + outer["height"] + 0.5:
                outside.append(
                    f"{name} (top={box['y']:.0f}, bottom={box['y'] + box['height']:.0f}, "
                    f"container={outer['y']:.0f}-{outer['y'] + outer['height']:.0f})"
                )
        return outside

    def has_horizontal_page_scroll(self) -> bool:
        return self.page.evaluate(
            "() => document.documentElement.scrollWidth > document.documentElement.clientWidth"
        )

    def overlapping_pairs(self, named_locators: dict[str, Locator]) -> list[str]:
        """Tra ve cac cap phan tu bi chong len nhau (bounding box giao nhau)."""
        boxes = {name: loc.bounding_box() for name, loc in named_locators.items()}
        names = [n for n, b in boxes.items() if b is not None]
        pairs: list[str] = []
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                ba, bb = boxes[a], boxes[b]
                overlap_x = min(ba["x"] + ba["width"], bb["x"] + bb["width"]) - max(ba["x"], bb["x"])
                overlap_y = min(ba["y"] + ba["height"], bb["y"] + bb["height"]) - max(ba["y"], bb["y"])
                if overlap_x > 1 and overlap_y > 1:
                    pairs.append(f"{a} <-> {b}")
        return pairs
