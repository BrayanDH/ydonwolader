#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 Launcher para YouTube Downloader Pro
Permite ejecutar tanto la versión Streamlit (moderna) como la Tkinter (legacy)
"""

import sys
import subprocess
import os
from pathlib import Path

def show_menu():
    """Muestra el menú de selección"""
    print("🎬 YouTube Downloader Pro - Launcher")
    print("=" * 50)
    print("1. 🌟 Streamlit App (Recomendado - Interfaz Moderna)")
    print("2. 🖥️  Tkinter App (Legacy - Interfaz Clásica)")
    print("3. ❌ Salir")
    print("=" * 50)

def run_streamlit():
    """Ejecuta la versión Streamlit"""
    print("\n🚀 Iniciando aplicación Streamlit...")
    print("💡 Se abrirá automáticamente en tu navegador")
    print("🌐 URL: http://localhost:8501")
    print("\n⏹️  Para detener: Ctrl+C en esta terminal\n")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Aplicación Streamlit cerrada por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando Streamlit: {e}")
        print("💡 Asegúrate de tener Streamlit instalado: pip install streamlit")
    except FileNotFoundError:
        print("❌ Streamlit no encontrado")
        print("💡 Instala con: pip install streamlit")

def run_tkinter():
    """Ejecuta la versión Tkinter"""
    print("\n🖥️  Iniciando aplicación Tkinter...")
    
    if not Path("youtube_downloader_gui.py").exists():
        print("❌ Archivo youtube_downloader_gui.py no encontrado")
        return
    
    try:
        subprocess.run([sys.executable, "youtube_downloader_gui.py"], check=True)
    except KeyboardInterrupt:
        print("\n👋 Aplicación Tkinter cerrada por el usuario")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando Tkinter: {e}")
    except FileNotFoundError:
        print("❌ Python no encontrado en PATH")

def check_dependencies():
    """Verifica las dependencias básicas"""
    missing_deps = []
    
    try:
        import yt_dlp
    except ImportError:
        missing_deps.append("yt-dlp")
    
    try:
        import streamlit
    except ImportError:
        missing_deps.append("streamlit")
    
    # Verificar FFmpeg
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, encoding='utf-8', errors='replace')
        if result.returncode != 0:
            missing_deps.append("ffmpeg")
    except FileNotFoundError:
        missing_deps.append("ffmpeg")
    
    if missing_deps:
        print("⚠️  Dependencias faltantes:")
        for dep in missing_deps:
            print(f"   • {dep}")
        print("\n💡 Instala con:")
        print("   pip install -r requirements.txt")
        print("   # Para FFmpeg, descarga desde: https://ffmpeg.org/download.html")
        return False
    
    return True

def main():
    """Función principal"""
    print("🔍 Verificando dependencias...")
    
    if not check_dependencies():
        print("\n❌ Por favor instala las dependencias faltantes antes de continuar.")
        input("Presiona Enter para continuar...")
        return
    
    print("✅ Todas las dependencias están disponibles\n")
    
    while True:
        show_menu()
        choice = input("\n👉 Selecciona una opción (1-3): ").strip()
        
        if choice == "1":
            run_streamlit()
        elif choice == "2":
            run_tkinter()
        elif choice == "3":
            print("\n👋 ¡Gracias por usar YouTube Downloader Pro!")
            break
        else:
            print("❌ Opción inválida. Por favor selecciona 1, 2 o 3.")
        
        print("\n" + "="*50)
        input("Presiona Enter para volver al menú...")

if __name__ == "__main__":
    main()
