import allure


def description_md(text: str):
    """
    Allure description decorator — text is rendered as markdown by Allure 2.

    Usage (class level — maps file to spec sheet):
        @description_md("Test cases XXX_001 – XXX_010 in <sheet name>")
        class TestSomething:
            ...

    Usage (method level — one block per test):
        @description_md(\"\"\"
        - **前提条件**: 〇〇画面を表示中
        - **テスト手順**: 1. 〇〇を押下する
        - **期待する結果**: 〇〇が表示されること
        \"\"\")
        def test_something(self, fixture):
            ...
    """
    return allure.description(text.strip())
