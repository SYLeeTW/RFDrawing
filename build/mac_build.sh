#!/usr/bin/env bash
# mac_build.sh
# 建立 Python 虛擬環境並打包 RFDrawing.app（macOS）

set -e  # 任一指令失敗就中止

# 專案根目錄：build/ 的上一層
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${PROJECT_ROOT}/venv"

echo "==> Project root: ${PROJECT_ROOT}"
echo "==> Using venv at: ${VENV_DIR}"

# 1. 建立 / 更新虛擬環境
if [ ! -d "${VENV_DIR}" ]; then
  echo "==> Creating virtual environment..."
  python3 -m venv "${VENV_DIR}"
else
  echo "==> Virtual environment already exists."
fi

# 2. 安裝套件
echo "==> Installing Python dependencies..."
"${VENV_DIR}/bin/python" -m pip install --upgrade pip
"${VENV_DIR}/bin/python" -m pip install -r "${PROJECT_ROOT}/requirements.txt"

# 3. 進入 src 並清乾淨舊的 build/dist/spec
cd "${PROJECT_ROOT}/src"
echo "==> Cleaning old build artifacts..."
rm -rf build dist RFDrawing.spec

# 4. 用 venv 裡的 pyinstaller 打包
echo "==> Running PyInstaller (macOS, windowed app)..."
"${VENV_DIR}/bin/pyinstaller" --windowed --name RFDrawing rf_drawing_gui.py

echo "==> Build finished."
echo "App is at: ${PROJECT_ROOT}/src/dist/RFDrawing.app"