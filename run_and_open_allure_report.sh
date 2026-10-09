#!/bin/bash
# ============================================================
# 🧾 Script Name: run_and_open_allure_report.sh
# Run cmd: bash run_and_open_allure_report.sh
# ------------------------------------------------------------
# 🎯 Purpose:
#   - Chạy pytest testcase và generate Allure report
#   - Tìm testcase theo @allure.title (fallback sang pytest -k)
#   - Nếu có ALLURE_PATH trong .env → dùng path đó
#   - Nếu không → dùng lệnh `allure` trong PATH
# ============================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Activate Python virtual environment if it exists
if [[ -f "${SCRIPT_DIR}/.venv/bin/activate" ]]; then
    source "${SCRIPT_DIR}/.venv/bin/activate"
elif [[ -f "${SCRIPT_DIR}/venv/bin/activate" ]]; then
    source "${SCRIPT_DIR}/venv/bin/activate"
fi

# Tự động load Java từ Homebrew (Apple Silicon) để Allure chạy được
if [[ -d "/opt/homebrew/opt/openjdk/bin" ]]; then
    export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
    export JAVA_HOME="/opt/homebrew/opt/openjdk"
fi

# 🧹 Cleanup video cũ nếu có
if [ -d "videos" ]; then
    echo "🧹 Removing old videos directory..."
    rm -rf videos
fi

# Load ALLURE_PATH / APP_URL từ .env
read_env() {
    grep -m 1 "^$1=" .env 2>/dev/null | sed -E "s/^[[:space:]]*$1=[[:space:]]*\"?([^\"]*)\"?/\1/"
}

ALLURE_PATH=""
APP_URL=""
if [ -f .env ]; then
    ALLURE_PATH=$(read_env ALLURE_PATH)
    APP_URL=$(read_env APP_URL)
    if [ -n "$ALLURE_PATH" ]; then
        echo "🧩 Loaded ALLURE_PATH from .env: $ALLURE_PATH"
    fi
fi
[ -z "$APP_URL" ] && APP_URL="(not set)"

if [ -z "$ALLURE_PATH" ]; then
    if command -v allure >/dev/null 2>&1; then
        ALLURE_PATH="$(command -v allure)"
        echo "🧩 Using allure from PATH: $ALLURE_PATH"
    else
        echo "❌ Không tìm thấy allure. Cài bằng: brew install allure"
        exit 1
    fi
fi

# Show tests folder structure cho dễ copy/paste
echo "📁 Available tests under ./tests:"
python3 - <<'PY'
import os

root = "tests"
if not os.path.isdir(root):
    print("  (tests directory not found)")
    raise SystemExit(0)

for current, dirs, files in os.walk(root):
    dirs[:] = sorted(d for d in dirs if d != "__pycache__")
    py_files = sorted(f for f in files if f.endswith(".py") and f != "__init__.py")
    level = current.count(os.sep) - root.count(os.sep)
    indent = "  " * level
    name = current if level == 0 else os.path.basename(current)
    print(f"{indent}{name}/")
    for f in py_files:
        print(f"{indent}  {f}")
PY
echo ""

# Hỏi test file / keyword
read -r -p "🔎 Enter test file or keyword: " keyword
keyword=$(printf '%s' "$keyword" | sed 's@\\\\@/@g')

echo "🔎 Resolving by @allure.title contains: $keyword"

matched_nodeids=()
while IFS= read -r line; do
    [ -n "$line" ] && matched_nodeids+=("$line")
done < <(
python3 - "$keyword" <<'PY'
import glob
import re
import sys

keyword_arg = sys.argv[1]
if not keyword_arg.strip():
    sys.exit(0)

# Tách theo dấu phẩy, bỏ khoảng trắng thừa
keywords = [k.strip() for k in keyword_arg.split(',') if k.strip()]

title_pattern = re.compile(r"^\s*@allure\.title\((['\"])(.*?)\1\)\s*$")
def_pattern = re.compile(r'^\s*def\s+(\w+)\s*\(')

for path in sorted(glob.glob("tests/**/*.py", recursive=True)):
    class_name = None
    pending_title = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            m_class = re.match(r'^\s*class\s+(\S+?)\s*[\(:]', line)
            if m_class:
                class_name = m_class.group(1)
                continue

            m_title = title_pattern.match(line)
            if m_title:
                pending_title = m_title.group(2)
                continue

            m_def = def_pattern.match(line)
            if m_def:
                func_name = m_def.group(1)
                if pending_title and any(k in pending_title for k in keywords):
                    nodeid = path
                    if class_name:
                        nodeid += f"::{class_name}"
                    nodeid += f"::{func_name}"
                    print(nodeid)
                pending_title = None
PY
)

if [ "${#matched_nodeids[@]}" -gt 0 ]; then
    echo "✅ Found ${#matched_nodeids[@]} testcase(s) by @allure.title:"
    printf '  - %s\n' "${matched_nodeids[@]}"
    echo "🚀 Running matched testcase(s) ..."
    python3 -m pytest "${matched_nodeids[@]}" --alluredir=allure-results --clean-alluredir -v -s || true
else
    pytest_k=$(echo "$keyword" | sed 's/,[[:space:]]*/ or /g')
    echo "ℹ️  No @allure.title match. Fallback to pytest -k \"$pytest_k\""
    echo "🚀 Running by keyword ..."
    python3 -m pytest -k "$pytest_k" --alluredir=allure-results --clean-alluredir -v -s || true
fi

# Tester name từ git
GIT_USER=$(git config user.name)
if [ -z "$GIT_USER" ]; then
    GIT_USER="${USER:-${USERNAME:-Unknown}}"
fi

# Write environment.properties
mkdir -p allure-results
{
    echo "Browser=Chromium"
    echo "Base_URL=$APP_URL"
    echo "Tester=$GIT_USER"
} >> allure-results/environment.properties

cat <<'EOF' > allure-results/categories.json
[
  {"name": "Timeout Errors", "matchedStatuses": ["failed"], "messageRegex": ".*TimeoutError.*"},
  {"name": "Assertion Failures", "matchedStatuses": ["failed"], "messageRegex": ".*AssertionError.*"},
  {"name": "Playwright Errors", "matchedStatuses": ["failed"], "messageRegex": ".*playwright.*"}
]
EOF

# ============================================================
# Generate Allure report
# ============================================================
echo "📊 Generating single-file Allure report..."
"$ALLURE_PATH" generate allure-results -o allure-report --clean --single-file || {
    echo "❌ Allure generate failed! Cài Java nếu thấy lỗi Java: brew install openjdk"
    exit 1
}

echo "🌐 Opening report..."
open allure-report/index.html
