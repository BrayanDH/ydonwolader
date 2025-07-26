#!/usr/bin/env python3
"""
Script para verificar que FFmpeg esté instalado y funcionando correctamente
"""

import subprocess
import sys

def verificar_ffmpeg():
    """Verifica si FFmpeg está instalado y funcionando"""
    
    print("🔧 Verificando instalación de FFmpeg...")
    print("=" * 50)
    
    try:
        # Ejecutar comando ffmpeg para obtener versión
        resultado = subprocess.run(
            ["ffmpeg", "-version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if resultado.returncode == 0:
            # Extraer información de la versión
            lineas = resultado.stdout.split('\n')
            version_line = lineas[0] if lineas else "Versión no encontrada"
            
            print("✅ FFmpeg está instalado y funcionando correctamente!")
            print(f"📦 {version_line}")
            
            # Verificar codecs importantes
            print("\n🎥 Verificando codecs disponibles...")
            
            # Verificar H.264
            resultado_codecs = subprocess.run(
                ["ffmpeg", "-codecs"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            
            if "h264" in resultado_codecs.stdout.lower():
                print("✅ Codec H.264 disponible")
            else:
                print("⚠️ Codec H.264 no encontrado")
            
            if "aac" in resultado_codecs.stdout.lower():
                print("✅ Codec AAC disponible")
            else:
                print("⚠️ Codec AAC no encontrado")
            
            print("\n🎉 ¡Todo listo para crear clips!")
            return True
            
        else:
            print("❌ Error ejecutando FFmpeg")
            print(f"Código de error: {resultado.returncode}")
            print(f"Error: {resultado.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout ejecutando FFmpeg (más de 10 segundos)")
        return False
        
    except FileNotFoundError:
        print("❌ FFmpeg no está disponible en esta sesión de terminal")
        print("\n🤔 ¿Acabas de instalar FFmpeg?")
        print("Si acabas de ejecutar 'winget install --id=Gyan.FFmpeg -e':")
        print("\n🔄 SOLUCIÓN INMEDIATA:")
        print("1. 🚪 CIERRA completamente esta terminal/VS Code")
        print("2. 🔄 ABRE una nueva terminal")
        print("3. 🧪 EJECUTA de nuevo: python verify_ffmpeg.py")
        print("4. 🚀 LUEGO ejecuta: python youtube_downloader_gui.py")
        print("\n📋 Si aún no tienes FFmpeg:")
        print("1. winget install --id=Gyan.FFmpeg -e")
        print("2. choco install ffmpeg (si tienes Chocolatey)")
        print("3. Descarga manual desde https://www.gyan.dev/ffmpeg/builds/")
        print("4. Lee: FFMPEG_INSTALL_GUIDE.md para instrucciones detalladas")
        print("\n💡 IMPORTANTE:")
        print("- Variables de entorno requieren reiniciar la terminal")
        print("- Winget modifica el PATH automáticamente")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {str(e)}")
        return False

def main():
    """Función principal"""
    
    print("🎬 YouTube Downloader - Verificador de FFmpeg")
    print()
    
    if verificar_ffmpeg():
        print("\n🚀 Puedes usar todas las funciones de la aplicación, incluyendo la creación de clips.")
    else:
        print("\n⚠️ Instala FFmpeg para usar la función de creación de clips.")
        print("La descarga normal de videos funcionará sin problemas.")
    
    print("\nPresiona Enter para continuar...")
    input()

if __name__ == "__main__":
    main()
