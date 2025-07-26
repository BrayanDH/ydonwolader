@echo off
REM ===================================
REM Instalador para YouTube Downloader Pro - Kivy Desktop
REM ===================================

echo.
echo ================================================
echo    YouTube Downloader Pro - Kivy Desktop
echo         Instalador para Windows
echo ================================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python no está instalado
    echo Por favor instala Python 3.8 o superior desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python detectado

REM Crear directorio de descargas
if not exist "downloads" mkdir downloads
echo ✅ Directorio de descargas creado

REM Instalar dependencias de Kivy
echo.
echo 📦 Instalando Kivy y dependencias...
echo.

python -m pip install --upgrade pip
python -m pip install wheel setuptools

REM Instalar Kivy desde requirements
python -m pip install -r requirements_kivy.txt

if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias de Kivy
    echo Intentando instalación alternativa...
    python -m pip install kivy[base] kivymd
)

REM Instalar yt-dlp
echo.
echo 📦 Instalando yt-dlp...
python -m pip install yt-dlp

echo.
echo ⚙️ Verificando FFmpeg...

REM Verificar FFmpeg
ffmpeg -version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ FFmpeg no detectado
    echo.
    echo 📋 Para instalar FFmpeg:
    echo 1. Descarga desde: https://ffmpeg.org/download.html#build-windows
    echo 2. Extrae en C:\ffmpeg
    echo 3. Agrega C:\ffmpeg\bin al PATH
    echo.
    echo O usa chocolatey: choco install ffmpeg
    echo O usa winget: winget install Gyan.FFmpeg
    echo.
    pause
) else (
    echo ✅ FFmpeg detectado
)

echo.
echo ================================================
echo      ✅ Instalación completada
echo ================================================
echo.
echo Para ejecutar la aplicación:
echo python kivy_app.py
echo.
pause
