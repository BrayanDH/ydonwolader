# Instalador de FFmpeg para YouTube Downloader
# PowerShell Script

Write-Host "🔧 Instalador de FFmpeg (PowerShell)" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Verificar si ffmpeg ya está instalado
try {
    $ffmpegVersion = & ffmpeg -version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ FFmpeg ya está instalado y funcionando" -ForegroundColor Green
        Write-Host ($ffmpegVersion[0]) -ForegroundColor Gray
        Write-Host ""
        Read-Host "Presiona Enter para continuar"
        exit
    }
} catch {
    Write-Host "📦 FFmpeg no está instalado, procediendo con la instalación..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🎯 Opciones de instalación:" -ForegroundColor White
Write-Host "1. winget (Windows 10/11 - Recomendado)" -ForegroundColor Green
Write-Host "2. Chocolatey" -ForegroundColor Yellow
Write-Host "3. Descarga manual" -ForegroundColor Orange
Write-Host "4. Salir" -ForegroundColor Red
Write-Host ""

$choice = Read-Host "Selecciona una opción (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "🚀 Instalando con winget..." -ForegroundColor Green
        
        try {
            $wingetVersion = & winget --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ winget encontrado: $wingetVersion" -ForegroundColor Green
                Write-Host "📥 Instalando FFmpeg..." -ForegroundColor Cyan
                
                & winget install --id=Gyan.FFmpeg -e --silent
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✅ FFmpeg instalado exitosamente con winget!" -ForegroundColor Green
                } else {
                    Write-Host "❌ Error con winget, intenta otra opción" -ForegroundColor Red
                }
            }
        } catch {
            Write-Host "❌ winget no está disponible" -ForegroundColor Red
            Write-Host "Actualiza Windows 10/11 para tener winget disponible" -ForegroundColor Yellow
        }
    }
    
    "2" {
        Write-Host ""
        Write-Host "🍫 Instalando con Chocolatey..." -ForegroundColor Yellow
        
        try {
            $chocoVersion = & choco --version 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Chocolatey encontrado: $chocoVersion" -ForegroundColor Green
                Write-Host "📥 Instalando FFmpeg..." -ForegroundColor Cyan
                
                & choco install ffmpeg -y
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "✅ FFmpeg instalado exitosamente con Chocolatey!" -ForegroundColor Green
                }
            }
        } catch {
            Write-Host "❌ Chocolatey no está instalado" -ForegroundColor Red
            Write-Host "Instala Chocolatey desde: https://chocolatey.org/install" -ForegroundColor Yellow
        }
    }
    
    "3" {
        Write-Host ""
        Write-Host "📋 Instrucciones para instalación manual:" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "🎯 DESCARGA DIRECTA:" -ForegroundColor White
        Write-Host "1. Ve a: https://www.gyan.dev/ffmpeg/builds/" -ForegroundColor Gray
        Write-Host "2. Descarga: 'release builds' > 'ffmpeg-release-essentials.zip'" -ForegroundColor Gray
        Write-Host "3. Extrae a: C:\ffmpeg" -ForegroundColor Gray
        Write-Host "4. Agrega al PATH: C:\ffmpeg\bin" -ForegroundColor Gray
        Write-Host ""
        Write-Host "🎯 AGREGAR AL PATH:" -ForegroundColor White
        Write-Host "1. Busca 'Variables de entorno' en Windows" -ForegroundColor Gray
        Write-Host "2. Edita 'Variables del sistema' > 'PATH'" -ForegroundColor Gray
        Write-Host "3. Agrega nueva entrada: C:\ffmpeg\bin" -ForegroundColor Gray
        Write-Host "4. Reinicia terminal/VS Code" -ForegroundColor Gray
        Write-Host ""
        
        $openBrowser = Read-Host "¿Abrir página de descarga en el navegador? (s/n)"
        if ($openBrowser -eq "s" -or $openBrowser -eq "S") {
            Start-Process "https://www.gyan.dev/ffmpeg/builds/"
        }
    }
    
    "4" {
        Write-Host "👋 Saliendo..." -ForegroundColor Gray
        exit
    }
    
    default {
        Write-Host "❌ Opción no válida" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "⚠️ IMPORTANTE:" -ForegroundColor Yellow
Write-Host "- Reinicia tu terminal o VS Code después de la instalación" -ForegroundColor Gray
Write-Host "- Ejecuta 'python verify_ffmpeg.py' para verificar" -ForegroundColor Gray
Write-Host ""

Read-Host "Presiona Enter para continuar"
