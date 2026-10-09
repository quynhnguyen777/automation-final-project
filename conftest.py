import os
import glob
import pytest
from datetime import datetime
from playwright.sync_api import Page
from dotenv import load_dotenv
import allure

load_dotenv()

from pages.login_page import LoginPage
from pages.notification_page import NotificationPage
from pages.settings_page import SettingsPage
from pages.ticket_list_page import TicketListPage

# Globals — updated by pytest_configure before any test runs
_MAX_RERUNS: int = 0
_RERUN_FAIL_VIDEO_HOLD_MS: int = 1500


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _extract_page_from_item(item) -> "Page | None":
    """Return the Playwright Page from test fixtures, however it is nested."""
    page = item.funcargs.get("page")
    if page:
        return page
    # Them ten fixture moi vao tuple duoi day de hook van chup duoc screenshot/video.
    for name in (
        "access_to_login_screen",
        "access_to_ticket_list_screen",
        "access_to_ticket_list_screen_as_guest",
        "access_to_notification_screen",
        "access_to_settings_screen",
    ):
        fixture = item.funcargs.get(name)
        if fixture and hasattr(fixture, "page"):
            return fixture.page
    return None


def _is_rerun_enabled() -> bool:
    return _MAX_RERUNS > 0


def _is_event_loop_closed_error(e: Exception) -> bool:
    msg = str(e).lower()
    return any(k in msg for k in ("event loop is closed", "connection closed", "target closed"))


def _get_video_path_without_rpc(video) -> "str | None":
    """Extract video path from internal Playwright object without making an RPC call."""
    impl = getattr(video, "_impl_obj", None)
    if impl:
        return getattr(impl, "_artifact_path", None)
    return None


def _find_recent_video_file_for_item(item_name: str) -> "str | None":
    """Find the most recently written video file, preferring files whose path contains item_name."""
    for pattern in ("videos/**/*.webm", "videos/**/*.mp4", ".videos/**/*.webm"):
        candidates = sorted(glob.glob(pattern, recursive=True), key=os.path.getmtime, reverse=True)
        named = [c for c in candidates if item_name in c]
        if named:
            return named[0]
        if candidates:
            return candidates[0]
    return None


# ---------------------------------------------------------------------------
# pytest hooks
# ---------------------------------------------------------------------------

def pytest_configure(config):
    """Apply HEADED setting from .env and capture --reruns count."""
    global _MAX_RERUNS
    headed = os.getenv("HEADED", "false").strip().lower() == "true"
    try:
        config.option.headed = headed
    except AttributeError:
        pass  # playwright plugin not yet loaded
    try:
        _MAX_RERUNS = int(getattr(config.option, "reruns", 0) or 0)
    except (AttributeError, TypeError, ValueError):
        _MAX_RERUNS = 0


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):  # `call` is required by pytest hook signature
    """Attach screenshot (pass+fail) and video (fail only) to Allure and pytest-html."""
    outcome = yield
    result = outcome.get_result()

    if result.when == "call":
        setattr(item, "rep_call", result)

    if result.when == "call" and result.failed:
        page = _extract_page_from_item(item)
        if page and _is_rerun_enabled():
            try:
                page.wait_for_timeout(_RERUN_FAIL_VIDEO_HOLD_MS)
            except Exception:
                pass

    # ── Screenshot on every call (pass + fail) — dùng làm bằng chứng đính kèm MR ──
    if result.when == "call":
        page = _extract_page_from_item(item)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        status = "FAILED" if result.failed else "PASSED"

        if page:
            try:
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name=f"{item.name}_{timestamp}_{status}",
                    attachment_type=allure.attachment_type.PNG,
                )
                print(f"📸 Screenshot captured for {item.name} ({status})")
            except Exception as e:
                allure.attach(
                    body=f"Could not capture screenshot: {e}",
                    name=f"{item.name}_{timestamp}_SCREENSHOT_ERROR",
                    attachment_type=allure.attachment_type.TEXT,
                )

    # ── Video on teardown (failed tests only) ───────────────────────────────
    if result.when == "teardown" and getattr(item, "rep_call", None) and item.rep_call.failed:
        current_attempt = getattr(item, "execution_count", 1)
        is_intermediate_rerun = _MAX_RERUNS > 0 and current_attempt <= _MAX_RERUNS

        page = _extract_page_from_item(item)
        video = getattr(page, "video", None) if page else None

        if video:
            try:
                video_path = video.path()
                if video_path and os.path.exists(video_path):
                    allure.attach.file(
                        video_path,
                        name=f"{item.name}_FAILED_VIDEO",
                        attachment_type=allure.attachment_type.MP4,
                    )
                    print(f"🎥 Video attached for {item.name}: {video_path}")
            except Exception as e:
                if _is_event_loop_closed_error(e):
                    fallback = (
                        _get_video_path_without_rpc(video)
                        or _find_recent_video_file_for_item(item.name)
                    )
                    if fallback and os.path.exists(fallback):
                        allure.attach.file(
                            fallback,
                            name=f"{item.name}_FAILED_VIDEO_FALLBACK",
                            attachment_type=allure.attachment_type.WEBM,
                        )
                        print(f"🎥 Video (fallback) attached for {item.name}: {fallback}")
                else:
                    allure.attach(
                        body=f"Could not attach video: {e}",
                        name=f"{item.name}_VIDEO_ERROR",
                        attachment_type=allure.attachment_type.TEXT,
                    )

        if is_intermediate_rerun:
            print(f"🔁 Rerun attempt {current_attempt}/{_MAX_RERUNS + 1} failed — deferred to final attempt.")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"{name} chưa được set — thêm vào file .env (xem .env.example).")
    return value


@pytest.fixture(scope="session")
def app_url() -> str:
    """URL trang bài tập (bai_tap_17082026.html)."""
    return _require_env("APP_URL")


@pytest.fixture(scope="session")
def admin_credentials() -> tuple[str, str]:
    """Tài khoản 1 (có sẵn data)."""
    return _require_env("ADMIN_ID"), _require_env("ADMIN_PASSWORD")


@pytest.fixture(scope="session")
def guest_credentials() -> tuple[str, str]:
    """Tài khoản 2 (không có data) — bắt buộc cho nhóm デフォルトアカウント（guestユーザー）."""
    return _require_env("GUEST_ID"), _require_env("GUEST_PASSWORD")


@pytest.fixture
def access_to_login_screen(page: Page, app_url: str) -> LoginPage:
    """Mở trang, dừng ở màn ログイン."""
    login = LoginPage(page)
    login.navigate_to(app_url)
    return login


@pytest.fixture
def access_to_ticket_list_screen(
    access_to_login_screen: LoginPage, admin_credentials: tuple[str, str]
) -> TicketListPage:
    """Login admin → màn チケット一覧 (mỗi lần login data được reset lại)."""
    access_to_login_screen.login_successfully(*admin_credentials)
    return TicketListPage(access_to_login_screen.page)


@pytest.fixture
def access_to_ticket_list_screen_as_guest(
    access_to_login_screen: LoginPage, guest_credentials: tuple[str, str]
) -> TicketListPage:
    """Login guest → màn チケット一覧 (trạng thái mặc định, 0 data)."""
    access_to_login_screen.login_successfully(*guest_credentials)
    return TicketListPage(access_to_login_screen.page)


@pytest.fixture
def access_to_notification_screen(access_to_ticket_list_screen: TicketListPage) -> NotificationPage:
    """Login admin → mở tab 通知."""
    notification = access_to_ticket_list_screen.open_notifications_tab()
    notification.expect_screen_displayed()
    return notification


@pytest.fixture
def access_to_settings_screen(access_to_ticket_list_screen: TicketListPage) -> SettingsPage:
    """Login admin → mở tab 設定."""
    settings = access_to_ticket_list_screen.open_settings_tab()
    settings.expect_screen_displayed()
    return settings
