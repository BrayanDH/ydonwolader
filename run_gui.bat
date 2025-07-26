@echo off
title YouTube Downloader GUI

echo 🚀 Iniciando YouTube Downloader GUI...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Verificar si las dependencias están instaladas
python -c "import yt_dlp" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando dependencias necesarias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Error instalando dependencias
        pause
        exit /b 1
    )
)

REM Verificar FFmpeg (opcional para clips)
echo 🔧 Verificando FFmpeg (necesario para crear clips)...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ FFmpeg no está instalado - La función de clips no funcionará
    echo 💡 Para instalar FFmpeg: powershell -ExecutionPolicy Bypass -File install_ffmpeg.ps1
    echo 📖 O lee: FFMPEG_INSTALL_GUIDE.md
    echo.
    echo ✅ La aplicación funcionará sin problemas para descargas normales
    echo.
) else (
    echo ✅ FFmpeg está instalado - Todas las funciones disponibles
)

REM Iniciar la aplicación GUI
echo ✅ Iniciando aplicación...
python youtube_downloader_gui.py

if errorlevel 1 (
    echo ❌ Error ejecutando la aplicación
    pause
)
