# ---------------------------------------------------------------------------
# Locator constants — chia class theo man hinh (screen name)
# Moi entry co comment ten field/element bang tieng Nhat
#
# Thu tu uu tien (theo sheet Rules - muc 4):
#   1. role + ten hien thi   (get_by_role)
#   2. label / placeholder   (get_by_label / get_by_placeholder)
#   3. id                    (#...)
#   4. class (BEM)           (.btn-detail, .row-checkbox, ...)
# Trang khong co data-testid; khong dung XPath theo vi tri.
# ---------------------------------------------------------------------------


class CommonLocators:
    TOAST_CONTAINER = "#toast_container"              # トースト通知の表示領域（全画面共通）


class LoginLocators:
    ID_LABEL = "ID"                     # ID入力欄（<label for="login_id">）
    PASSWORD_LABEL = "パスワード"         # パスワード入力欄（<label for="login_password">）
    LOGIN_BUTTON_NAME = "ログイン"        # ログインボタン
    LOGIN_SECTION = "#login_section"    # ログイン画面全体（role/label が無いため id）
    LOGIN_ERROR = "#login_error"        # ログインエラーメッセージ（role 無しのため id）


class HeaderLocators:
    # nav-tab は <li> で role/aria-label が無いため id を使用
    NAV_TAB_TICKETS = "#nav_tab_tickets"              # ヘッダー: 「チケット一覧」タブ
    NAV_TAB_NOTIFICATIONS = "#nav_tab_notifications"  # ヘッダー: 「通知」タブ
    NAV_TAB_SETTINGS = "#nav_tab_settings"            # ヘッダー: 「設定」タブ
    NAV_TAB_ACTIVE_CLASS = "nav-tab--active"          # タブのアクティブ状態クラス
    HEADER_USERNAME = "#header_username"              # ヘッダー右上のユーザー名
    MAIN_SECTION = "#main_section"                    # ログイン後のメイン画面

    # レイアウト確認（Others_01）用: ヘッダー内の主要要素
    APP_HEADER = "#app_header"                        # ヘッダー全体
    APP_LOGO = "#app_logo"                            # 左上ロゴ（🎫 サポートチケット管理）
    NAV_TABS = "#nav_tabs"                            # タブ一覧
    USER_MENU_ACTIVATOR = "#user_menu_activator"      # ユーザーメニューボタン（名前がユーザーで変わるため id）


class TicketListLocators:
    PANEL = "#panel_tickets"                          # チケット一覧パネル（スコープ用）
    NEW_TICKET_BUTTON_NAME = "新規チケット作成"         # ツールバー: 「＋新規チケット作成」ボタン
    SEARCH_PLACEHOLDER = "件名または担当者で検索"        # キーワード検索欄
    SEARCH_BUTTON_NAME = "検索"                        # 「検索」ボタン
    PRIORITY_FILTER_LABEL = "優先度で絞り込み"           # 優先度プルダウン（aria-label）
    PER_PAGE_LABEL = "表示件数"                         # 表示件数プルダウン（aria-label）

    # 「前へ」「次へ」は上下2箇所にあるため、必ずコンテナで scope する（Rules 罠#1）
    PAGINATION_TOP = "#pagination_top"                # 上部ページネーション
    PAGINATION_BOTTOM = "#pagination_bottom"          # 下部ページネーション
    NEXT_BUTTON_NAME = "次へ"                          # 「次へ」ボタン
    PREV_BUTTON_NAME = "前へ"                          # 「前へ」ボタン
    PAGE_BUTTON_ACTIVE_CLASS = "page-btn--active"     # 現在ページ番号ボタンのクラス

    TABLE_BODY = "#ticket_tbody"                      # チケット一覧テーブルの tbody
    SELECT_ALL_CHECKBOX_NAME = "全て選択"               # ヘッダーの全選択チェックボックス（aria-label）
    BULK_ACTION_BAR = "#bulk_action_bar"              # 一括操作バー
    SELECTED_COUNT = "#selected_count"                # 一括操作バー: 「n件選択中」

    # 行内ボタン（各行に同じ文言があるため行で scope する）
    DETAIL_BUTTON_NAME = "詳細"                        # 行: 「詳細」ボタン
    DELETE_BUTTON_NAME = "削除"                        # 行: 「削除」ボタン（ケバブ内の「削除」と区別するため exact）
    # 優先度チップは role/label が無いため class（BEM: priority-high/mid/low）
    PRIORITY_CHIP = ".chip[class*='priority-']"       # 行: 優先度チップ
    STATUS_CHIP = ".chip[class*='status-']"           # 行: ステータスチップ

    # 「作成日」見出し: innerText に sort/tooltip のアイコン文字が混ざるため id で取得（Rules 罠#2）
    CREATED_HEADER = "#th_created"                    # 列見出し「作成日」
    CREATED_TOOLTIP_TRIGGER = ".tooltip-wrap"         # 「作成日」横のヘルプアイコン（?）
    CREATED_TOOLTIP_CONTENT = ".tooltip-content"      # ツールチップ本文

    TABLE_WRAP = ".table-wrap"                        # テーブルのスクロールコンテナ（レイアウト確認用）

    # 埋め込みプレビュー（iframe）
    PREVIEW_IFRAME = "#preview_iframe"                # 埋め込みプレビュー iframe
    FRAME_APPLY_BUTTON_NAME = "適用"                   # iframe内: 「適用」ボタン
    FRAME_RESULT = "#frame_result"                    # iframe内: 結果メッセージ（role 無しのため id）

    # 外部リンク（新しいタブ / 新しいウィンドウ）
    PRINT_PREVIEW_BUTTON_NAME = "印刷プレビューを開く（新しいウィンドウ）"  # 印刷プレビューボタン


class TicketDetailLocators:
    DIALOG_NAME = "チケット詳細"                         # 詳細ダイアログ（aria-labelledby）
    # input[type=file] は display:none → set_input_files で直接指定する（Rules 罠#2）
    FILE_INPUT = "#detail_file_input"                 # 添付ファイル input（非表示）
    FILE_NAME = "#detail_file_name"                   # 添付プレビュー: ファイル名＋サイズ
    REMOVE_FILE_BUTTON_NAME = "ファイルを削除"           # 添付プレビュー: 削除アイコン（aria-label）
    FILE_ERROR = "#detail_file_error"                 # 添付エラーメッセージ
    CLOSE_BUTTON_NAME = "閉じる"                        # 「閉じる」ボタン


class NotificationLocators:
    PANEL = "#panel_notifications"                    # 通知一覧パネル（スコープ用）
    HEADING_NAME = "通知一覧"                           # 見出し「通知一覧」
    SEARCH_PLACEHOLDER = "タイトルまたは内容で検索"       # 通知検索欄
    SEARCH_BUTTON_NAME = "検索"                         # 「検索」ボタン
    TABLE_BODY = "#notification_tbody"                # 通知一覧テーブルの tbody
    CREATE_FROM_EMPTY_BUTTON_NAME = "＋通知を作成する"   # 0件メッセージの下の作成ボタン
    CREATE_MODAL_NAME = "通知を作成"                     # 通知作成モーダル（aria-labelledby）
    # label は「タイトル*」のように必須マーク付きのため placeholder で指定
    MODAL_TITLE_PLACEHOLDER = "例：メンテナンスのお知らせ"   # モーダル: タイトル入力欄
    MODAL_CONTENT_PLACEHOLDER = "通知内容を入力"            # モーダル: 内容入力欄
    MODAL_SUBMIT_BUTTON_NAME = "作成する"                 # モーダル: 「作成する」ボタン


class SettingsLocators:
    PANEL = "#panel_settings"                         # 設定パネル（スコープ用）
    SIGNATURE_PLACEHOLDER = "返信メールに付与する署名を入力"  # 署名入力欄（textarea, maxlength=100）
    SIGNATURE_COUNTER = "#signature_counter"          # 署名の文字数カウンター
