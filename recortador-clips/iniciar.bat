@echo off
REM Recortador de clips - doble clic para abrir la app (Windows)
cd /d "%~dp0"
if not exist .venv (
  echo Instalando por primera vez...
  python -m venv .venv
  .venv\Scripts\python -m pip install --upgrade pip
  .venv\Scripts\pip install -r requirements.txt
)
where ffmpeg >nul 2>nul || (echo Falta ffmpeg: instala con  winget install Gyan.FFmpeg  y vuelve a abrir & pause & exit /b)
.venv\Scripts\python app.py
pause
