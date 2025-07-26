#!/usr/bin/env python3
"""
Script simple para descargar videos de YouTube usando yt-dlp
"""

import os
import sys
import yt_dlp
from pathlib import Path


def descargar_video(url, directorio_destino='downloads', calidad='best'):
    """
    Descarga un video de YouTube
    
    Args:
        url (str): URL del video de YouTube
        directorio_destino (str): Directorio donde guardar el video
        calidad (str): Calidad del video ('best', 'worst', '720p', etc.)
    """
    
    # Crear directorio de descarga si no existe
    Path(directorio_destino).mkdir(exist_ok=True)
    
    # Configuración de yt-dlp
    ydl_opts = {
        'outtmpl': f'{directorio_destino}/%(title)s.%(ext)s',
        'format': calidad,
        'noplaylist': True,  # Solo descargar el video individual, no playlist
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"📥 Descargando: {url}")
            ydl.download([url])
            print("✅ Descarga completada exitosamente!")
            
    except Exception as e:
        print(f"❌ Error durante la descarga: {str(e)}")
        return False
    
    return True


def main():
    """Función principal del script"""
    
    print("🎬 Descargador de Videos de YouTube")
    print("=" * 40)
    
    # Verificar si se proporcionó URL como argumento
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        # Solicitar URL interactivamente
        url = input("📎 Ingresa la URL del video de YouTube: ").strip()
    
    # Validar que la URL no esté vacía
    if not url:
        print("❌ Error: Debes proporcionar una URL válida")
        sys.exit(1)
    
    # Opción para seleccionar directorio de descarga
    directorio = input("📁 Directorio de descarga (presiona Enter para 'downloads'): ").strip()
    if not directorio:
        directorio = 'downloads'
    
    # Opción para seleccionar calidad
    print("\n📊 Opciones de calidad disponibles:")
    print("1. best (mejor calidad disponible)")
    print("2. worst (menor calidad)")
    print("3. 720p")
    print("4. 480p")
    print("5. 360p")
    
    opcion_calidad = input("\n🎯 Selecciona la calidad (1-5, o presiona Enter para 'best'): ").strip()
    
    calidades = {
        '1': 'best',
        '2': 'worst',
        '3': 'best[height<=720]',
        '4': 'best[height<=480]',
        '5': 'best[height<=360]'
    }
    
    calidad = calidades.get(opcion_calidad, 'best')
    
    # Realizar la descarga
    print(f"\n🚀 Iniciando descarga en '{directorio}' con calidad '{calidad}'...")
    exito = descargar_video(url, directorio, calidad)
    
    if exito:
        print(f"\n🎉 ¡Video descargado exitosamente en '{directorio}'!")
    else:
        print("\n😞 La descarga no pudo completarse")
        sys.exit(1)


if __name__ == "__main__":
    main()
