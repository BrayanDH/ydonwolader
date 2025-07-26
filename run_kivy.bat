@echo off
REM ===================================
REM Launcher para YouTube Downloader Pro - Kivy Desktop
REM ===================================

title YouTube Downloader Pro - Desktop Edition

echo.
echo ================================================
echo    🎬 YouTube Downloader Pro - Desktop
echo ================================================
echo.

REM Verificar que existe el archivo principal
if not exist "kivy_app.py" (
    echo ❌ Error: kivy_app.py no encontrado
    echo Asegúrate de ejecutar este archivo desde el directorio correcto
    pause
    exit /b 1
)

REM Crear directorio de descargas si no existe
if not exist "downloads" mkdir downloads

echo 🚀 Iniciando aplicación...
echo.

REM Ejecutar la aplicación
python kivy_app.py

echo.
echo 👋 Aplicación cerrada
pause
