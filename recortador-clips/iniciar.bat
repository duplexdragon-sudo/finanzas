@echo off
REM Recortador de clips - doble clic para abrir la app (Windows)
cd /d "%~dp0"
title Recortador de clips - no cierres esta ventana

REM buscar Python: primero el lanzador "py", luego "python"
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY (
  echo No encuentro Python. Instala con:  winget install Python.Python.3.12
  echo y reinicia la PC.
  pause
  exit /b
)

where ffmpeg >nul 2>nul || (
  echo No encuentro ffmpeg. Instala con:  winget install Gyan.FFmpeg
  echo Si ya lo instalaste, reinicia la PC y vuelve a abrir este archivo.
  pause
  exit /b
)

if not exist .venv\Scripts\python.exe (
  echo Instalando por primera vez, tarda unos minutos...
  %PY% -m venv .venv || (echo No se pudo crear el entorno de Python & pause & exit /b)
  .venv\Scripts\python -m pip install --upgrade pip
  .venv\Scripts\python -m pip install -r requirements.txt || (echo Fallo la instalacion. Manda una foto de esta ventana. & pause & exit /b)
)

echo.
echo Abriendo la app en http://localhost:5000 ...
echo (deja esta ventana abierta mientras uses la app)
echo.
.venv\Scripts\python app.py
pause
