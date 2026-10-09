# ---------------------------------------------------------------------------
# Test data — gia tri dau vao / so lieu mong doi lay tu spec
# (credentials KHONG de o day: doc tu .env)
# ---------------------------------------------------------------------------

# GD02.8-04: 異常系ログイン
WRONG_PASSWORD = "wrongpass"

# admin の初期データ
ADMIN_TOTAL_TICKETS = 12
ADMIN_TOTAL_NOTIFICATIONS = 3
DEFAULT_PER_PAGE = 10

# GD02.1-02: ページネーション（次へ）
PAGE_2_ROW_COUNT = 2

# GD02.4-02: 優先度絞り込み
PRIORITY_HIGH = "高"
PRIORITY_HIGH_COUNT = 5

# GD02.6-02: キーワード検索（Enterキー）
SEARCH_KEYWORD_LOGIN = "ログイン"
SEARCH_LOGIN_EXPECTED_COUNT = 1

# GD03.1-01 / GD02.7-01 / GD03.2-01: 操作対象チケット
TARGET_TICKET_ID = "T-1001"
TARGET_TICKET_STATUS = "未対応"

# GD03.2-01: iframe 内で選択するステータス
IFRAME_STATUS_TO_APPLY = "完了"

# GD02.7-01: ファイルアップロード（正常） — .png 約1MB
UPLOAD_PNG_NAME = "sample_1mb.png"
UPLOAD_PNG_SIZE_BYTES = 1024 * 1024

# GD02.3-001: 署名 100文字超過
SIGNATURE_MAX_LENGTH = 100
SIGNATURE_OVER_LENGTH = 120

# GD02.1-01: 存在しないキーワード
NOT_EXIST_KEYWORD = "存在しない通知キーワード_zzz"

# Others_01: 画面サイズ（解像度・アスペクト比）
VIEWPORTS = {
    "desktop_1920x1080": {"width": 1920, "height": 1080},
    "laptop_1366x768": {"width": 1366, "height": 768},
    "tablet_768x1024": {"width": 768, "height": 1024},
    "mobile_375x667": {"width": 375, "height": 667},
}
