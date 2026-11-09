@echo off
chcp 65001 >nul
title Subir Shorts DuplexDragon
if not exist "%USERPROFILE%\subir-shorts" mkdir "%USERPROFILE%\subir-shorts"
cd /d "%USERPROFILE%\subir-shorts"
echo Preparando...
curl -sL -o subir_shorts.py https://raw.githubusercontent.com/duplexdragon-sudo/finanzas/claude/lucid-fermi-mzw50z/redes/subir-shorts/subir_shorts.py
curl -sL -o shorts.json https://raw.githubusercontent.com/duplexdragon-sudo/finanzas/claude/lucid-fermi-mzw50z/redes/subir-shorts/shorts.json
py -m pip install -q playwright yt-dlp
py subir_shorts.py --cuantos 1 --ver
echo.
pause
