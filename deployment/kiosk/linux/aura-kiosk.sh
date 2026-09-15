#!/usr/bin/env bash
# Lightweight kiosk launcher. Configure the agent URL below before use.
set -euo pipefail
# AURA_AGENT_URL is current; JARVIS_AGENT_URL kept as fallback.
AGENT_URL="${AURA_AGENT_URL:-${JARVIS_AGENT_URL:-http://127.0.0.1:8080}}"
# AURA_KIOSK_BROWSER is current; fall back to legacy names (avoids clash with AURA_BROWSER STT setting).
BROWSER="${AURA_KIOSK_BROWSER:-${JARVIS_BROWSER:-chromium}}"
if ! command -v "$BROWSER" >/dev/null 2>&1; then
  echo "Browser not found: $BROWSER" >&2
  echo "Install Chromium or set AURA_KIOSK_BROWSER to your supported browser binary." >&2
  exit 1
fi
exec "$BROWSER" \
  --kiosk "$AGENT_URL" \
  --no-first-run \
  --no-default-browser-check \
  --disable-session-crashed-bubble \
  --disable-features=TranslateUI \
  --start-maximized
