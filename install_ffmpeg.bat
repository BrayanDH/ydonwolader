@echo off
echo 🔧 Instalador de FFmpeg para YouTube Downloader
echo ================================================
echo.

REM Verificar si ffmpeg ya está instalado
ffmpeg -version >nul 2>&1
if not errorlevel 1 (
    echo ✅ FFmpeg ya está instalado y funcionando
    ffmpeg -version | findstr "ffmpeg version"
    echo.
    goto :end
)

echo 📦 FFmpeg no está instalado o no está en el PATH
echo.
echo Opciones de instalación:
echo.
echo 1. Descargar FFmpeg automáticamente (recomendado)
echo 2. Instrucciones para instalación manual
echo 3. Salir
echo.
set /p choice="Selecciona una opción (1-3): "

if "%choice%"=="1" goto :auto_install
if "%choice%"=="2" goto :manual_instructions
if "%choice%"=="3" goto :end

:auto_install
echo.
echo 🚀 Descargando e instalando FFmpeg...
echo.

REM Crear directorio para ffmpeg
if not exist "C:\ffmpeg" mkdir "C:\ffmpeg"
cd "C:\ffmpeg"

echo 📥 Descargando FFmpeg desde GitHub...
echo (Esto puede tomar unos minutos)

REM Descargar ffmpeg usando PowerShell
powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip' -OutFile 'ffmpeg.zip'}"

if not exist "ffmpeg.zip" (
    echo ❌ Error descargando FFmpeg
    echo Por favor, intenta la instalación manual
    goto :manual_instructions
)

echo 📂 Extrayendo archivos...
powershell -Command "Add-Type -AssemblyName System.IO.Compression.FileSystem; [System.IO.Compression.ZipFile]::ExtractToDirectory('ffmpeg.zip', '.')"

REM Encontrar la carpeta extraída
for /d %%i in (ffmpeg-*) do set FFMPEG_DIR=%%i

if not defined FFMPEG_DIR (
    echo ❌ Error extrayendo FFmpeg
    goto :manual_instructions
)

REM Copiar binarios a ubicación final
copy "%FFMPEG_DIR%\bin\*" "C:\ffmpeg\" >nul
if errorlevel 1 (
    echo ❌ Error copiando archivos
    echo Puede que necesites ejecutar como administrador
    pause
    exit /b 1
)

REM Limpiar archivos temporales
del "ffmpeg.zip" >nul 2>&1
rmdir /s /q "%FFMPEG_DIR%" >nul 2>&1

echo ⚙️ Agregando FFmpeg al PATH del sistema...

REM Agregar al PATH del sistema (requiere permisos de administrador)
setx PATH "%PATH%;C:\ffmpeg" /M >nul 2>&1
if errorlevel 1 (
    echo ⚠️ No se pudo agregar al PATH del sistema
    echo Agregando al PATH del usuario...
    setx PATH "%PATH%;C:\ffmpeg" >nul 2>&1
)

echo.
echo ✅ FFmpeg instalado exitosamente en C:\ffmpeg
echo.
echo ⚠️ IMPORTANTE: Reinicia tu terminal o VS Code para que los cambios surtan efecto
echo.
echo Para verificar la instalación, abre una nueva terminal y ejecuta:
echo ffmpeg -version
echo.
goto :end

:manual_instructions
echo.
echo 📋 Instrucciones para instalación manual de FFmpeg:
echo.
echo 1. Ve a https://ffmpeg.org/download.html
echo 2. Descarga la versión para Windows
echo 3. Extrae los archivos a una carpeta (ej: C:\ffmpeg)
echo 4. Agrega la carpeta bin al PATH del sistema:
echo    - Abre "Variables de entorno" en Windows
echo    - Edita la variable PATH
echo    - Agrega la ruta: C:\ffmpeg\bin
echo 5. Reinicia tu terminal
echo.
echo Alternativamente, puedes usar chocolatey:
echo choco install ffmpeg
echo.
echo O usar winget:
echo winget install FFmpeg
echo.

:end
echo.
echo Presiona cualquier tecla para continuar...
pause >nul
