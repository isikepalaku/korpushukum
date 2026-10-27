#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV="${TIKTOK_WATCH_VENV:-$HOME/venvs/tiktok-watch}"
uv venv "$VENV"
uv pip install --python "$VENV/bin/python" -r "$ROOT/requirements.txt"
"$VENV/bin/python" -m playwright install chromium
