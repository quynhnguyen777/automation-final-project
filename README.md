# Automation Final Project — Bài tập 17.08.2026

Automation test (Python + Playwright + pytest + Allure) cho trang
[サポートチケット管理 | Bài tập 17.08.2026](https://bsv-nhungnguyen.github.io/bai_tap_17082026.html).

Phạm vi: **13 testcase tối thiểu — mỗi Category 1 case** (+1 case bonus GD02.1-01 và 1 test luyện
pattern get-or-create theo Rules mục 8). Kết quả được ghi trong sheet `Testcases_Quynh`.

## Cấu trúc

```text
├── pages/            # Page Object (kế thừa BasePage)
├── constants/        # locators.py (kèm comment tiếng Nhật), messages.py
├── testdata/         # Dữ liệu test / số liệu mong đợi
├── tests/            # Test file theo màn hình
├── conftest.py       # Fixture login admin/guest, screenshot + video cho Allure
├── pytest.ini
└── .github/workflows/playwright-tests.yml   # CI chạy trên GitHub Actions
```

## Mapping testcase ↔ hàm test

| Category | ID | 関数名 | File |
|---|---|---|---|
| GD01-Navigation | GD01_004 | `test_notification_tab_click_shows_three_notifications` | tests/test_header_navigation.py |
| GD02.1-Click | GD02.1-02 | `test_pagination_click_next_shows_page_two_and_enables_prev` | tests/test_ticket_list.py |
| GD02.2-Check | GD02.2-001 | `test_select_all_checkbox_checks_all_rows_and_shows_bulk_bar` | tests/test_ticket_list.py |
| GD02.3-Fill | GD02.3-001 | `test_signature_over_max_length_is_truncated_and_counter_stops` | tests/test_settings.py |
| GD02.4-SelectOption | GD02.4-02 | `test_priority_filter_high_shows_only_high_priority_tickets` | tests/test_ticket_list.py |
| GD02.5-Hover | GD02.5-001 | `test_created_date_help_icon_hover_shows_tooltip` | tests/test_ticket_list.py |
| GD02.6-Keyboard | GD02.6-02 | `test_search_with_enter_key_matches_search_button_result` | tests/test_ticket_list.py |
| GD02.7-FileUpload | GD02.7-01 | `test_detail_upload_png_shows_preview_and_delete_icon` | tests/test_ticket_detail.py |
| GD02.8-Assertion | GD02.8-04 | `test_login_with_wrong_password_shows_error_and_stays_on_login` | tests/test_login.py |
| GD03.1-Dialog | GD03.1-01 | `test_delete_ticket_accept_confirm_removes_row_and_shows_toast` | tests/test_ticket_list.py |
| GD03.2-Iframe | GD03.2-01 | `test_iframe_apply_status_shows_result_only_inside_iframe` | tests/test_ticket_list.py |
| GD03.3-TabWindow | GD03.3-01 | `test_print_preview_opens_popup_with_ticket_count` | tests/test_ticket_list.py |
| Others | Others_01 | `test_ticket_list_layout_has_no_overflow_or_overlap` | tests/test_layout.py |
| (bonus) GD02.1-Click | GD02.1-01 | `test_notification_empty_result_create_button_opens_modal` | tests/test_notification.py |
| (bonus) Rules mục 8 | — | `test_ensure_notification_exists_creates_only_when_missing` | tests/test_notification.py |

> **Others_01 = NG (có chủ đích giữ test fail):** ở viewport 375×667, logo / tab / tên user trên
> header bị xuống dòng từng ký tự và tràn khỏi header cao 56px (trang không có responsive).
> Theo rule "app khác spec thì test phải fail", test giữ nguyên trạng thái fail để team confirm spec.

## Các "bẫy" trong Rules đã xử lý

- Nút trùng tên (詳細 / 削除 / 前へ / 次へ) → luôn scope theo dòng (`row_of(ticket_id)`) hoặc container `#pagination_top`.
- Checkbox thật `opacity:0` → `check()` trực tiếp vào `<input>` qua `get_by_role("checkbox", name="全て選択")`.
- Input file `display:none` → `set_input_files` (buffer 1MB, không cần file thật trong repo).
- Header 作成日 lẫn text icon/tooltip → không assert innerText, dùng `#th_created` + `.tooltip-content`.
- confirm / popup → đăng ký `page.once("dialog")` / `expect_popup()` **trước** khi click.
- get-or-create → `NotificationPage.ensure_notification_exists()`. Lưu ý: dòng message 0件 cũng chứa keyword,
  nên phải match đúng ô tiêu đề (`get_by_role("cell", name=title, exact=True)`), không dùng `has_text`.

## Chạy local

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium
cp .env.example .env          # điền ADMIN_ID / ADMIN_PASSWORD / GUEST_ID / GUEST_PASSWORD
pytest                         # hoặc: bash run_and_open_allure_report.sh
```

## CI/CD (GitHub Actions)

Workflow `.github/workflows/playwright-tests.yml` chạy khi push lên `develop` / `feature/**`, khi mở PR vào
`develop`, hoặc chạy tay (Actions → Run workflow, có thể chọn file / `-k`).

Cần khai báo trong **Settings → Secrets and variables → Actions**:

| Loại | Tên |
|---|---|
| Secret | `ADMIN_ID`, `ADMIN_PASSWORD`, `GUEST_ID`, `GUEST_PASSWORD` |
| Variable (tuỳ chọn) | `APP_URL` (mặc định: trang bài tập) |

Allure report được upload thành artifact `allure-report` và publish lên nhánh `gh-pages/<run_number>`.
