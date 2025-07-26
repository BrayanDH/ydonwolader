@echo off
echo 🚀 Instalando dependencias para YouTube Downloader...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.

REM Instalar dependencias
echo 📦 Instalando yt-dlp...
pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Error durante la instalación
    pause
    exit /b 1
)

echo.
echo ✅ ¡Instalación completada exitosamente!
echo.
echo Para usar la aplicación, puedes ejecutar:
echo • python youtube_downloader.py (versión consola)
echo • python youtube_downloader_gui.py (versión gráfica)
echo • run_gui.bat (acceso directo a la GUI)
echo.
pause
