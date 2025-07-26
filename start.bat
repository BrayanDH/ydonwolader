@echo off
title YouTube Downloader - Inicio Completo

echo 🎬 YouTube Downloader - Verificación completa
echo =============================================
echo.

REM Verificar Python
echo 🐍 Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado
    echo Instala Python desde https://python.org
    pause
    exit /b 1
)
echo ✅ Python está instalado

REM Verificar dependencias de Python
echo 📦 Verificando dependencias de Python...
python -c "import yt_dlp, PIL, requests" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Instalando dependencias faltantes...
    pip install -r requirements.txt
)
echo ✅ Dependencias de Python OK

REM Verificar FFmpeg
echo 🔧 Verificando FFmpeg...
ffmpeg -version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ FFmpeg no está disponible
    echo 💡 Para instalar FFmpeg: winget install --id=Gyan.FFmpeg -e
    echo 📖 O ejecuta: powershell -ExecutionPolicy Bypass -File install_ffmpeg.ps1
    echo.
    echo ✅ La aplicación funcionará, pero sin la función de clips
    set FFMPEG_STATUS=SIN_CLIPS
) else (
    echo ✅ FFmpeg está instalado - Todas las funciones disponibles
    set FFMPEG_STATUS=COMPLETO
)

echo.
echo 🎉 ESTADO DEL SISTEMA:
echo ✅ Python: Funcionando
echo ✅ Dependencias: Instaladas
if "%FFMPEG_STATUS%"=="COMPLETO" (
    echo ✅ FFmpeg: Funcionando - TODAS las funciones disponibles
) else (
    echo ⚠️ FFmpeg: No disponible - Solo falta función de clips
)
echo.

echo 🚀 Iniciando YouTube Downloader GUI...
echo.
python youtube_downloader_gui.py

if errorlevel 1 (
    echo ❌ Error ejecutando la aplicación
    pause
)
