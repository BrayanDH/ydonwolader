#!/usr/bin/env python3
"""
Script avanzado para descargar videos de YouTube con opciones adicionales
"""

import os
import sys
import json
import yt_dlp
from pathlib import Path
from datetime import datetime


class YouTubeDownloader:
    """Clase para manejar descargas de YouTube"""
    
    def __init__(self, directorio_base='downloads'):
        self.directorio_base = directorio_base
        Path(directorio_base).mkdir(exist_ok=True)
    
    def obtener_info_video(self, url):
        """Obtiene información del video sin descargarlo"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'titulo': info.get('title', 'Sin título'),
                    'duracion': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Desconocido'),
                    'descripcion': info.get('description', '')[:200] + '...',
                    'formatos': len(info.get('formats', [])),
                    'fecha_subida': info.get('upload_date', 'Desconocida')
                }
        except Exception as e:
            print(f"❌ Error obteniendo información: {str(e)}")
            return None
    
    def descargar_video(self, url, opciones=None):
        """Descarga un video con opciones personalizadas"""
        
        if opciones is None:
            opciones = {}
        
        # Configuración por defecto
        ydl_opts = {
            'outtmpl': f'{self.directorio_base}/%(title)s.%(ext)s',
            'format': opciones.get('calidad', 'best'),
            'noplaylist': True,
        }
        
        # Opciones adicionales
        if opciones.get('solo_audio', False):
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': f'{self.directorio_base}/%(title)s.%(ext)s'
            })
        
        if opciones.get('subtitulos', False):
            ydl_opts.update({
                'writesubtitles': True,
                'writeautomaticsub': True,
                'subtitleslangs': ['es', 'en'],
            })
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"📥 Descargando: {url}")
                ydl.download([url])
                return True
                
        except Exception as e:
            print(f"❌ Error durante la descarga: {str(e)}")
            return False
    
    def descargar_playlist(self, url, max_videos=None):
        """Descarga una playlist completa"""
        
        ydl_opts = {
            'outtmpl': f'{self.directorio_base}/%(playlist_title)s/%(playlist_index)s - %(title)s.%(ext)s',
            'format': 'best',
        }
        
        if max_videos:
            ydl_opts['playlistend'] = max_videos
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"📋 Descargando playlist: {url}")
                ydl.download([url])
                return True
                
        except Exception as e:
            print(f"❌ Error descargando playlist: {str(e)}")
            return False


def mostrar_menu():
    """Muestra el menú principal"""
    print("\n🎬 YouTube Downloader Avanzado")
    print("=" * 40)
    print("1. Descargar video individual")
    print("2. Descargar solo audio (MP3)")
    print("3. Descargar con subtítulos")
    print("4. Descargar playlist")
    print("5. Ver información del video")
    print("6. Salir")
    return input("\n👉 Selecciona una opción (1-6): ").strip()


def formatear_duracion(segundos):
    """Convierte segundos a formato HH:MM:SS"""
    if not segundos:
        return "Desconocida"
    
    horas = segundos // 3600
    minutos = (segundos % 3600) // 60
    segundos = segundos % 60
    
    if horas > 0:
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    else:
        return f"{minutos:02d}:{segundos:02d}"


def main():
    downloader = YouTubeDownloader()
    
    while True:
        opcion = mostrar_menu()
        
        if opcion == '6':
            print("👋 ¡Hasta luego!")
            break
        
        if opcion in ['1', '2', '3', '4', '5']:
            url = input("\n📎 Ingresa la URL de YouTube: ").strip()
            
            if not url:
                print("❌ URL no válida")
                continue
        
        if opcion == '1':
            # Descargar video individual
            calidad = input("🎯 Calidad (best/720p/480p/360p o Enter para 'best'): ").strip() or 'best'
            opciones = {'calidad': calidad}
            
            if downloader.descargar_video(url, opciones):
                print("✅ Descarga completada!")
            
        elif opcion == '2':
            # Descargar solo audio
            opciones = {'solo_audio': True}
            
            if downloader.descargar_video(url, opciones):
                print("✅ Audio extraído y guardado como MP3!")
            
        elif opcion == '3':
            # Descargar con subtítulos
            calidad = input("🎯 Calidad (Enter para 'best'): ").strip() or 'best'
            opciones = {'calidad': calidad, 'subtitulos': True}
            
            if downloader.descargar_video(url, opciones):
                print("✅ Video descargado con subtítulos!")
            
        elif opcion == '4':
            # Descargar playlist
            max_videos = input("🔢 Máximo de videos (Enter para todos): ").strip()
            max_videos = int(max_videos) if max_videos.isdigit() else None
            
            if downloader.descargar_playlist(url, max_videos):
                print("✅ Playlist descargada!")
            
        elif opcion == '5':
            # Ver información del video
            print("🔍 Obteniendo información...")
            info = downloader.obtener_info_video(url)
            
            if info:
                print(f"\n📺 Título: {info['titulo']}")
                print(f"👤 Canal: {info['uploader']}")
                print(f"⏱️  Duración: {formatear_duracion(info['duracion'])}")
                print(f"📅 Fecha de subida: {info['fecha_subida']}")
                print(f"🎞️  Formatos disponibles: {info['formatos']}")
                print(f"📝 Descripción: {info['descripcion']}")
        
        else:
            print("❌ Opción no válida")
        
        input("\n⏸️  Presiona Enter para continuar...")


if __name__ == "__main__":
    main()
