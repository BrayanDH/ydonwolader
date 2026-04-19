#!/usr/bin/env python3
"""
Script para verificar y actualizar yt-dlp
"""

import subprocess
import sys

def check_ytdlp():
    """Verifica la versión de yt-dlp"""
    try:
        result = subprocess.run(['yt-dlp', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✅ yt-dlp instalado: {version}")
        return True
    except:
        print("❌ yt-dlp no instalado")
        return False

def update_ytdlp():
    """Actualiza yt-dlp"""
    print("\n📦 Actualizando yt-dlp...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'], check=True)
        print("✅ yt-dlp actualizado correctamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al actualizar yt-dlp")
        return False

def check_ffmpeg():
    """Verifica si ffmpeg está instalado"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        version_line = result.stdout.split('\n')[0]
        print(f"✅ ffmpeg instalado: {version_line}")
        return True
    except:
        print("❌ ffmpeg no instalado")
        return False

def main():
    print("🔍 VERIFICADOR DE DEPENDENCIAS\n")
    print("="*50)
    
    # Verificar herramientas
    ytdlp_ok = check_ytdlp()
    ffmpeg_ok = check_ffmpeg()
    
    print("="*50)
    
    # Sugerencias
    if not ytdlp_ok:
        print("\n💡 Para instalar yt-dlp, ejecuta:")
        print("   pip install yt-dlp")
    
    if not ffmpeg_ok:
        print("\n💡 Para instalar ffmpeg:")
        print("   Windows: descargar de https://ffmpeg.org")
        print("   O usar: choco install ffmpeg")
    
    # Preguntar si actualizar
    if ytdlp_ok:
        print("\n¿Deseas actualizar yt-dlp a la última versión? (s/n)")
        respuesta = input("> ").strip().lower()
        if respuesta == 's':
            update_ytdlp()

if __name__ == "__main__":
    main()
