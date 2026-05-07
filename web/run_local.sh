#!/usr/bin/env bash
# Aura — local stage demo runner.
#
# One command for the venue stage if the iPhone fails:
#   bash web/run_local.sh
#
# Starts:
#   - FastAPI on :8000 (the agent stack)
#   - Static frontend on :8080 (the React UI)
# Then opens http://localhost:8080/index.html in the default browser.
#
# Works offline. No CDN, no internet egress.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/.." && pwd)"

API_PORT="${AURA_API_PORT:-8000}"
WEB_PORT="${AURA_WEB_PORT:-8080}"

echo "==> Aura local demo"
echo "    repo root: $REPO_ROOT"
echo "    API  :$API_PORT"
echo "    web  :$WEB_PORT"

# Pick a Python — prefer venv if present, else system python3.
PY="python3"
if [[ -x "$REPO_ROOT/.venv/bin/python" ]]; then
  PY="$REPO_ROOT/.venv/bin/python"
fi
echo "    python: $PY"

# Best-effort dependency check.
if ! "$PY" -c "import fastapi, uvicorn" 2>/dev/null; then
  echo "==> installing FastAPI deps from web/api/requirements.txt"
  "$PY" -m pip install -r "$HERE/api/requirements.txt"
fi

# Boot FastAPI in the background.
echo "==> launching uvicorn on :$API_PORT"
PYTHONPATH="$REPO_ROOT" "$PY" -m uvicorn web.api.main:app \
  --host 127.0.0.1 --port "$API_PORT" \
  --log-level warning &
API_PID=$!

# Boot static server in the background.
echo "==> launching static server on :$WEB_PORT"
"$PY" -m http.server "$WEB_PORT" --directory "$HERE/web" --bind 127.0.0.1 &
WEB_PID=$!

# Open the browser (best-effort across macOS / Linux).
URL="http://localhost:$WEB_PORT/index.html"
sleep 1
if command -v open >/dev/null 2>&1; then
  open "$URL" || true
elif command -v xdg-open >/dev/null 2>&1; then
  xdg-open "$URL" || true
fi

echo ""
echo "==> Aura local demo is live."
echo "    Frontend : $URL"
echo "    API      : http://localhost:$API_PORT/api/health"
echo "    Stop     : Ctrl-C"

# Trap so both children die on exit.
trap 'echo "==> shutting down"; kill -TERM "$API_PID" "$WEB_PID" 2>/dev/null || true' EXIT INT TERM

# Block until either child exits.
wait -n
