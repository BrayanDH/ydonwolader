#!/usr/bin/env python3
"""
Diagnóstico completo del sistema para YouTube Downloader
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python():
    """Verificar Python"""
    print("🐍 PYTHON")
    print("-" * 20)
    print(f"✅ Versión: {sys.version}")
    print(f"✅ Ejecutable: {sys.executable}")
    print()

def check_modules():
    """Verificar módulos de Python"""
    print("📦 MÓDULOS PYTHON")
    print("-" * 20)
    
    modules = {
        'tkinter': 'GUI',
        'yt_dlp': 'Descarga de videos',
        'PIL': 'Imágenes (Pillow)',
        'requests': 'HTTP requests',
        'subprocess': 'Ejecutar comandos',
        'threading': 'Hilos',
        'pathlib': 'Rutas de archivos',
        'json': 'JSON',
        'webbrowser': 'Abrir navegador'
    }
    
    for module, desc in modules.items():
        try:
            __import__(module)
            print(f"✅ {module:12} - {desc}")
        except ImportError:
            print(f"❌ {module:12} - {desc} (FALTANTE)")
    print()

def check_ffmpeg():
    """Verificar FFmpeg"""
    print("🔧 FFMPEG")
    print("-" * 20)
    
    try:
        resultado = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=5)
        if resultado.returncode == 0:
            version_line = resultado.stdout.split('\n')[0]
            print(f"✅ {version_line}")
            
            # Verificar codecs
            resultado_codecs = subprocess.run(["ffmpeg", "-codecs"], capture_output=True, text=True, timeout=5)
            if "h264" in resultado_codecs.stdout.lower():
                print("✅ Codec H.264 disponible")
            if "aac" in resultado_codecs.stdout.lower():
                print("✅ Codec AAC disponible")
                
        else:
            print("❌ FFmpeg no funciona correctamente")
            
    except FileNotFoundError:
        print("❌ FFmpeg no está instalado o no está en el PATH")
    except Exception as e:
        print(f"❌ Error verificando FFmpeg: {e}")
    print()

def check_directories():
    """Verificar directorios"""
    print("📁 DIRECTORIOS")
    print("-" * 20)
    
    dirs = [
        ("downloads", "Descargas principales"),
        ("temp_clips", "Videos temporales para clips")
    ]
    
    for dir_name, desc in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            files = list(dir_path.glob("*"))
            print(f"✅ {dir_name:12} - {desc} ({len(files)} archivos)")
        else:
            print(f"⚠️ {dir_name:12} - {desc} (no existe)")
    print()

def check_gui_files():
    """Verificar archivos de la aplicación"""
    print("📄 ARCHIVOS DE LA APLICACIÓN")
    print("-" * 30)
    
    files = [
        ("youtube_downloader_gui.py", "Interfaz gráfica principal"),
        ("youtube_downloader.py", "Script básico"),
        ("requirements.txt", "Dependencias"),
        ("verify_ffmpeg.py", "Verificador FFmpeg"),
        ("test_clips.py", "Test de clips")
    ]
    
    for file_name, desc in files:
        file_path = Path(file_name)
        if file_path.exists():
            size = file_path.stat().st_size
            print(f"✅ {file_name:25} - {desc} ({size:,} bytes)")
        else:
            print(f"❌ {file_name:25} - {desc} (FALTANTE)")
    print()

def run_gui_test():
    """Test básico de la GUI"""
    print("🎨 TEST DE GUI")
    print("-" * 20)
    
    try:
        import tkinter as tk
        from tkinter import ttk
        
        # Test básico de tkinter
        root = tk.Tk()
        root.title("Test")
        root.geometry("200x100")
        label = tk.Label(root, text="Test OK")
        label.pack()
        
        # Cerrar inmediatamente
        root.after(100, root.destroy)
        root.mainloop()
        
        print("✅ Tkinter funciona correctamente")
        
    except Exception as e:
        print(f"❌ Error con tkinter: {e}")
    print()

def main():
    """Función principal"""
    print("🔍 DIAGNÓSTICO COMPLETO - YouTube Downloader")
    print("=" * 60)
    print()
    
    check_python()
    check_modules()
    check_ffmpeg()
    check_directories()
    check_gui_files()
    run_gui_test()
    
    print("🏁 DIAGNÓSTICO COMPLETADO")
    print("=" * 60)
    print()
    print("💡 PRÓXIMOS PASOS:")
    print("1. Si todo está ✅, ejecuta: python youtube_downloader_gui.py")
    print("2. Si hay ❌, instala lo que falta")
    print("3. Para test de clips: python test_clips.py")
    print()
    
    input("Presiona Enter para continuar...")

if __name__ == "__main__":
    main()
