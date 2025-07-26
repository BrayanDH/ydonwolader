@echo off
echo 🔧 Instalador Rápido de FFmpeg (winget)
echo =====================================
echo.

REM Verificar si ffmpeg ya está instalado
ffmpeg -version >nul 2>&1
if not errorlevel 1 (
    echo ✅ FFmpeg ya está instalado y funcionando
    ffmpeg -version | findstr "ffmpeg version"
    echo.
    goto :end
)

echo 📦 Instalando FFmpeg usando winget...
echo.

REM Verificar si winget está disponible
winget --version >nul 2>&1
if errorlevel 1 (
    echo ❌ winget no está disponible
    echo.
    echo 📋 Alternativas:
    echo 1. Actualiza Windows 10/11 para tener winget
    echo 2. Usa chocolatey: choco install ffmpeg
    echo 3. Descarga manual desde https://ffmpeg.org/download.html
    echo.
    goto :end
)

echo ✅ winget encontrado, instalando FFmpeg...
winget install --id=Gyan.FFmpeg -e --silent

if errorlevel 1 (
    echo ❌ Error con winget, probando con chocolatey...
    
    REM Verificar si chocolatey está disponible
    choco --version >nul 2>&1
    if not errorlevel 1 (
        echo ✅ Chocolatey encontrado, instalando...
        choco install ffmpeg -y
    ) else (
        echo ❌ Chocolatey tampoco está disponible
        goto :manual_instructions
    )
)

echo.
echo ⚠️ IMPORTANTE: Reinicia tu terminal o VS Code
echo.
echo Para verificar la instalación:
echo python verify_ffmpeg.py
echo.
goto :end

:manual_instructions
echo.
echo 📋 Instalación Manual Requerida:
echo.
echo 🎯 OPCIÓN MÁS FÁCIL - Chocolatey:
echo 1. Instala Chocolatey desde https://chocolatey.org/install
echo 2. Abre PowerShell como administrador
echo 3. Ejecuta: choco install ffmpeg
echo.
echo 🎯 OPCIÓN MANUAL:
echo 1. Ve a https://www.gyan.dev/ffmpeg/builds/
echo 2. Descarga "release builds" ^> "ffmpeg-release-essentials.zip"
echo 3. Extrae a C:\ffmpeg
echo 4. Agrega C:\ffmpeg\bin al PATH de Windows
echo 5. Reinicia terminal/VS Code
echo.

:end
echo.
echo Presiona cualquier tecla para continuar...
pause >nul
