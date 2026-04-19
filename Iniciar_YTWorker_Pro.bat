@echo off
title YTWorker Pro Launcher
mode con: cols=60 lines=10
color 0B

echo ============================================
echo           YTWORKER PRO LAUNCHER
echo ============================================

:: Navegar al directorio donde esta el batch
cd /d "%~dp0"

:: Ejecutar el launcher de python
python ytworker_launcher.py

echo.
echo [OK] Proceso completado.
timeout /t 3
exit
