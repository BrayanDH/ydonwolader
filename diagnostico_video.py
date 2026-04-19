#!/usr/bin/env python3
"""
Herramienta para diagnosticar problemas con descargas de YouTube
Muestra formatos disponibles y ayuda a resolver errores
"""

import sys
import yt_dlp
from pathlib import Path

def diagnose_video(url):
    """Diagnostica un video de YouTube"""
    print(f"\n{'='*70}")
    print(f"🔍 DIAGNÓSTICO DE VIDEO DE YOUTUBE")
    print(f"{'='*70}\n")
    
    print(f"📎 URL: {url}\n")
    
    try:
        # Obtener información del video
        with yt_dlp.YoutubeDL({'quiet': False}) as ydl:
            print("⏳ Extrayendo información del video...\n")
            info = ydl.extract_info(url, download=False)
            
            # Información básica
            print(f"{'='*70}")
            print("📺 INFORMACIÓN DEL VIDEO")
            print(f"{'='*70}")
            print(f"Título: {info.get('title', 'N/A')}")
            print(f"Canal: {info.get('uploader', 'N/A')}")
            print(f"Duración: {info.get('duration', 0)} segundos")
            print(f"ID: {info.get('id', 'N/A')}")
            print(f"Disponible: {info.get('is_live', False) and 'EN VIVO' or 'PRE-GRABADO'}\n")
            
            # Formatos disponibles
            formatos = info.get('formats', [])
            if formatos:
                print(f"{'='*70}")
                print(f"📊 FORMATOS DISPONIBLES ({len(formatos)})")
                print(f"{'='*70}\n")
                
                # Agrupar por tipo
                print("🎥 FORMATOS DE VIDEO + AUDIO:")
                count = 0
                for fmt in formatos:
                    if fmt.get('height') and fmt.get('acodec') != 'none':
                        height = fmt.get('height', 'N/A')
                        fps = fmt.get('fps', 'N/A')
                        codec = fmt.get('vcodec', 'N/A').split('.')[0]
                        format_id = fmt.get('format_id', 'N/A')
                        
                        if count < 10:  # Mostrar los primeros 10
                            print(f"  {format_id:6} - {height}p@{fps}fps - {codec}")
                            count += 1
                
                if len([f for f in formatos if f.get('height') and f.get('acodec') != 'none']) > 10:
                    print(f"  ... y {len([f for f in formatos if f.get('height') and f.get('acodec') != 'none']) - 10} más")
                
                # Formatos solo de audio
                print("\n🎵 FORMATOS SOLO AUDIO:")
                audio_count = 0
                for fmt in formatos:
                    if fmt.get('acodec') != 'none' and not fmt.get('height'):
                        codec = fmt.get('acodec', 'N/A').split('.')[0]
                        abr = fmt.get('abr', 'N/A')
                        format_id = fmt.get('format_id', 'N/A')
                        
                        if audio_count < 5:
                            print(f"  {format_id:6} - {codec} @ {abr}kbps")
                            audio_count += 1
                
                if len([f for f in formatos if f.get('acodec') != 'none' and not f.get('height')]) > 5:
                    print(f"  ... y {len([f for f in formatos if f.get('acodec') != 'none' and not f.get('height')]) - 5} más")
                
                # Recomendación
                print(f"\n{'='*70}")
                print("✅ RECOMENDACIÓN DE FORMATO")
                print(f"{'='*70}")
                print("Para la mejor experiencia, usa:")
                print("  'bestvideo[height<=720]/best[height<=720]/bestvideo/best'")
                
            else:
                print(f"{'='*70}")
                print("❌ NO HAY FORMATOS DE VIDEO DISPONIBLES")
                print(f"{'='*70}")
                print("⚠️  Este video probablemente está protegido o restringido.")
                print("   Solo hay imágenes disponibles para descarga.")
                
    except Exception as e:
        print(f"{'='*70}")
        print("❌ ERROR AL OBTENER INFORMACIÓN")
        print(f"{'='*70}")
        print(f"Error: {str(e)}\n")
        
        # Sugerencias
        if "Only images are available" in str(e):
            print("💡 El video está completamente protegido.")
            print("   Prueba con otro video.")
        elif "nsig extraction failed" in str(e):
            print("💡 Intenta actualizar yt-dlp:")
            print("   pip install --upgrade yt-dlp")
        elif "HTTP Error 404" in str(e):
            print("💡 Video no encontrado o URL inválida.")
        elif "HTTP Error 403" in str(e):
            print("💡 Video restringido por región.")
    
    print(f"\n{'='*70}\n")

def main():
    if len(sys.argv) < 2:
        print("📌 USO:")
        print("   python diagnostico.py <URL_DE_VIDEO>\n")
        print("📝 EJEMPLO:")
        print('   python diagnostico.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"\n')
        return
    
    url = sys.argv[1]
    diagnose_video(url)

if __name__ == "__main__":
    main()
