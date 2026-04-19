#!/usr/bin/env python3
"""
Script para listar todos los formatos disponibles del video
"""

import yt_dlp

PROBLEMATIC_URL = "https://www.youtube.com/watch?v=uik8XAXwqBQ"

def list_formats(url):
    """Lista todos los formatos disponibles"""
    print(f"🎬 Listando formatos disponibles para:")
    print(f"🔗 {url}\n")
    
    try:
        ydl_opts = {
            'listformats': True,
            'quiet': False,
            'no_warnings': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            print(f"\n📊 Información del video:")
            print(f"   - Título: {info.get('title', 'N/A')}")
            print(f"   - Duración: {info.get('duration', 'N/A')} segundos")
            print(f"   - Disponible: {info.get('ext', 'N/A')}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    list_formats(PROBLEMATIC_URL)
