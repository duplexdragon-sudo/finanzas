#!/usr/bin/env bash
# Lanza el servidor MCP de Instagram (https://github.com/jlbadano/ig-mcp, licencia MIT).
# Descarga una versión fija del repo y sus dependencias en ~/.cache/ig-mcp la primera vez.
#
# Uso:
#   run.sh             -> instala si falta y arranca el servidor (lo usa .mcp.json)
#   run.sh --install   -> solo instala (lo usa el hook SessionStart)
#
# Variables de entorno necesarias (configúralas en el entorno, NUNCA en el repo):
#   INSTAGRAM_ACCESS_TOKEN, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET,
#   INSTAGRAM_BUSINESS_ACCOUNT_ID
set -euo pipefail

REPO_URL="https://github.com/jlbadano/ig-mcp.git"
PINNED_COMMIT="549fbeedc7f4409556a88d9d462e5f7ea454ca6a"
DIR="${IG_MCP_DIR:-$HOME/.cache/ig-mcp}"
PY="$DIR/.venv/bin/python"

install() {
  if [ ! -d "$DIR/.git" ]; then
    git clone --quiet "$REPO_URL" "$DIR"
  fi
  git -C "$DIR" checkout --quiet "$PINNED_COMMIT"
  if [ ! -x "$PY" ] || [ ! -f "$DIR/.venv/.ok" ]; then
    python3 -m venv "$DIR/.venv"
    # mcp<2: el servidor usa la API de mcp 1.x
    "$DIR/.venv/bin/pip" install --quiet \
      "mcp>=1.0,<2" httpx requests python-dotenv pydantic pydantic-settings \
      asyncio-throttle aiofiles nest-asyncio pillow structlog rich python-dateutil
    touch "$DIR/.venv/.ok"
  fi
  mkdir -p "$DIR/logs"
}

install >&2

if [ "${1:-}" = "--install" ]; then
  echo "ig-mcp instalado en $DIR" >&2
  exit 0
fi

for v in INSTAGRAM_ACCESS_TOKEN FACEBOOK_APP_ID FACEBOOK_APP_SECRET INSTAGRAM_BUSINESS_ACCOUNT_ID; do
  if [ -z "${!v:-}" ]; then
    echo "Falta la variable de entorno $v. Agrégala en la configuración del entorno." >&2
    exit 1
  fi
done

cd "$DIR"
export CACHE_ENABLED="${CACHE_ENABLED:-false}"   # sin Redis
exec "$PY" -m src.instagram_mcp_server
