#!/usr/bin/env bash
# Recortador de clips - Mac / Linux:  ./iniciar.sh
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  echo "Instalando por primera vez..."
  python3 -m venv .venv && .venv/bin/pip install --upgrade pip && .venv/bin/pip install -r requirements.txt
fi
command -v ffmpeg >/dev/null || { echo "Falta ffmpeg (Mac: brew install ffmpeg)"; exit 1; }
exec .venv/bin/python app.py "$@"
