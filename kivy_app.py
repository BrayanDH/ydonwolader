#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 YouTube Downloader & Clip Creator - Kivy Desktop Version
Aplicación de escritorio completa con todas las funcionalidades de Streamlit
"""

import os
import sys
import threading
import subprocess
import json
import time
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

# Kivy imports
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.scrollview import ScrollView
from kivy.uix.accordion import Accordion, AccordionItem
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.switch import Switch
from kivy.uix.checkbox import CheckBox
from kivy.logger import Logger

# YouTube DLP and FFmpeg
import yt_dlp

# Configurar Kivy
kivy.require('2.0.0')

class VideoInfoWidget(BoxLayout):
    """Widget para mostrar información del video"""
    
    def __init__(self, video_info=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.spacing = 10
        self.padding = 15
        
        if video_info:
            self.display_info(video_info)
    
    def display_info(self, info):
        self.clear_widgets()
        
        # Título
        title_label = Label(
            text=f"📺 {info.get('title', 'Sin título')}",
            text_size=(None, None),
            halign='left',
            font_size='18sp',
            bold=True
        )
        self.add_widget(title_label)
        
        # Información básica
        details_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height='100dp')
        
        # Canal
        details_layout.add_widget(Label(
            text=f"👤 Canal: {info.get('uploader', 'Desconocido')}",
            text_size=(None, None),
            halign='left'
        ))
        
        # Duración
        duration = self.format_duration(info.get('duration', 0))
        details_layout.add_widget(Label(
            text=f"⏱️ Duración: {duration}",
            text_size=(None, None),
            halign='left'
        ))
        
        # Fecha de subida
        upload_date = info.get('upload_date', 'Desconocida')
        if len(upload_date) == 8:  # YYYYMMDD format
            formatted_date = f"{upload_date[6:8]}/{upload_date[4:6]}/{upload_date[0:4]}"
        else:
            formatted_date = upload_date
            
        details_layout.add_widget(Label(
            text=f"📅 Subido: {formatted_date}",
            text_size=(None, None),
            halign='left'
        ))
        
        # Visualizaciones
        view_count = info.get('view_count', 0)
        views_text = f"{view_count:,}" if view_count else "N/A"
        details_layout.add_widget(Label(
            text=f"👁️ Vistas: {views_text}",
            text_size=(None, None),
            halign='left'
        ))
        
        self.add_widget(details_layout)
    
    def format_duration(self, seconds):
        """Convierte segundos a formato HH:MM:SS"""
        if not seconds:
            return "Desconocida"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

class TimelineWidget(BoxLayout):
    """Widget personalizado para el timeline de clips"""
    
    def __init__(self, duration=300, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.duration = duration
        self.start_time = 0
        self.end_time = 60
        self.spacing = 15
        self.padding = 10
        
        self.create_timeline()
    
    def create_timeline(self):
        self.clear_widgets()
        
        # Título
        title = Label(
            text="🎬 Timeline Interactivo",
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height='40dp'
        )
        self.add_widget(title)
        
        # Información de duración
        duration_label = Label(
            text=f"Duración total: {self.format_time(self.duration)}",
            size_hint_y=None,
            height='30dp'
        )
        self.add_widget(duration_label)
        
        # Slider de inicio
        start_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp')
        start_layout.add_widget(Label(text="🕐 Inicio:", size_hint_x=None, width='100dp'))
        
        self.start_slider = Slider(
            min=0,
            max=max(0, self.duration-1),
            value=self.start_time,
            step=1
        )
        self.start_slider.bind(value=self.on_start_change)
        start_layout.add_widget(self.start_slider)
        
        self.start_time_label = Label(
            text=self.format_time(self.start_time),
            size_hint_x=None,
            width='100dp'
        )
        start_layout.add_widget(self.start_time_label)
        self.add_widget(start_layout)
        
        # Slider de fin
        end_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp')
        end_layout.add_widget(Label(text="🕐 Fin:", size_hint_x=None, width='100dp'))
        
        self.end_slider = Slider(
            min=self.start_time+1,
            max=self.duration,
            value=self.end_time,
            step=1
        )
        self.end_slider.bind(value=self.on_end_change)
        end_layout.add_widget(self.end_slider)
        
        self.end_time_label = Label(
            text=self.format_time(self.end_time),
            size_hint_x=None,
            width='100dp'
        )
        end_layout.add_widget(self.end_time_label)
        self.add_widget(end_layout)
        
        # Barra de progreso visual
        self.progress_bar = ProgressBar(
            max=100,
            value=self.get_progress_percentage(),
            size_hint_y=None,
            height='20dp'
        )
        self.add_widget(self.progress_bar)
        
        # Información del clip
        self.clip_info_label = Label(
            text=self.get_clip_info_text(),
            size_hint_y=None,
            height='40dp'
        )
        self.add_widget(self.clip_info_label)
        
        # Botones rápidos
        quick_layout = GridLayout(cols=4, spacing=10, size_hint_y=None, height='50dp')
        
        btn_30s = Button(text="📺 30s", on_press=lambda x: self.set_quick_time(0, 30))
        btn_1min = Button(text="🎵 1min", on_press=lambda x: self.set_quick_time(0, 60))
        btn_2min = Button(text="📹 2min", on_press=lambda x: self.set_quick_time(0, 120))
        btn_5min = Button(text="🎬 5min", on_press=lambda x: self.set_quick_time(0, 300))
        
        quick_layout.add_widget(btn_30s)
        quick_layout.add_widget(btn_1min)
        quick_layout.add_widget(btn_2min)
        quick_layout.add_widget(btn_5min)
        
        self.add_widget(quick_layout)
    
    def on_start_change(self, instance, value):
        self.start_time = int(value)
        self.start_time_label.text = self.format_time(self.start_time)
        
        # Ajustar el slider de fin si es necesario
        if self.end_time <= self.start_time:
            self.end_time = min(self.start_time + 1, self.duration)
            self.end_slider.value = self.end_time
        
        self.end_slider.min = self.start_time + 1
        self.update_progress()
        self.update_clip_info()
    
    def on_end_change(self, instance, value):
        self.end_time = int(value)
        self.end_time_label.text = self.format_time(self.end_time)
        self.update_progress()
        self.update_clip_info()
    
    def set_quick_time(self, start, end):
        """Configura tiempos rápidos"""
        self.start_time = start
        self.end_time = min(end, self.duration)
        
        self.start_slider.value = self.start_time
        self.end_slider.value = self.end_time
        
        self.update_progress()
        self.update_clip_info()
    
    def update_progress(self):
        progress = self.get_progress_percentage()
        self.progress_bar.value = progress
    
    def update_clip_info(self):
        self.clip_info_label.text = self.get_clip_info_text()
    
    def get_progress_percentage(self):
        if self.duration == 0:
            return 0
        clip_duration = self.end_time - self.start_time
        return min(100, (clip_duration / self.duration) * 100)
    
    def get_clip_info_text(self):
        clip_duration = self.end_time - self.start_time
        percentage = (clip_duration / self.duration) * 100 if self.duration > 0 else 0
        return f"📏 Duración: {self.format_time(clip_duration)} ({percentage:.1f}%)"
    
    def format_time(self, seconds):
        """Convierte segundos a formato HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def get_times(self):
        """Retorna los tiempos actuales"""
        return self.start_time, self.end_time

class YouTubeTab(TabbedPanelItem):
    """Pestaña para descargar y crear clips de YouTube"""
    
    def __init__(self, **kwargs):
        super().__init__(text="🎬 YouTube", **kwargs)
        self.video_info = None
        self.downloaded_video_path = None
        self.timeline_widget = None
        self.create_content()
    
    def create_content(self):
        main_layout = BoxLayout(orientation='vertical', spacing=15, padding=20)
        
        # Título
        title = Label(
            text="🎬 YouTube Downloader & Clip Creator",
            font_size='24sp',
            bold=True,
            size_hint_y=None,
            height='50dp'
        )
        main_layout.add_widget(title)
        
        # ScrollView para contenido
        scroll = ScrollView()
        content_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Input URL
        url_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp')
        url_layout.add_widget(Label(text="🔗 URL:", size_hint_x=None, width='80dp'))
        
        self.url_input = TextInput(
            hint_text="https://www.youtube.com/watch?v=...",
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        url_layout.add_widget(self.url_input)
        
        analyze_btn = Button(
            text="🔍 Analizar",
            size_hint_x=None,
            width='120dp',
            on_press=self.analyze_video
        )
        url_layout.add_widget(analyze_btn)
        content_layout.add_widget(url_layout)
        
        # Información del video
        self.video_info_widget = VideoInfoWidget(size_hint_y=None, height='200dp')
        content_layout.add_widget(self.video_info_widget)
        
        # Botón de descarga
        download_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp')
        
        self.download_btn = Button(
            text="📥 Descargar Video",
            disabled=True,
            on_press=self.download_video
        )
        download_layout.add_widget(self.download_btn)
        
        self.download_progress = ProgressBar(size_hint_x=None, width='200dp')
        download_layout.add_widget(self.download_progress)
        content_layout.add_widget(download_layout)
        
        # Timeline
        self.timeline_container = BoxLayout(orientation='vertical', size_hint_y=None, height='300dp')
        content_layout.add_widget(self.timeline_container)
        
        # Configuración de clip
        clip_config_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='120dp')
        
        # Nombre del clip
        name_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        name_layout.add_widget(Label(text="📝 Nombre:", size_hint_x=None, width='100dp'))
        self.clip_name_input = TextInput(
            text=f"clip_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            multiline=False,
            size_hint_y=None,
            height='30dp'
        )
        name_layout.add_widget(self.clip_name_input)
        clip_config_layout.add_widget(name_layout)
        
        # Formato
        format_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        format_layout.add_widget(Label(text="🎞️ Formato:", size_hint_x=None, width='100dp'))
        self.format_spinner = Spinner(
            text='mp4',
            values=['mp4', 'webm', 'mkv'],
            size_hint_y=None,
            height='30dp'
        )
        format_layout.add_widget(self.format_spinner)
        clip_config_layout.add_widget(format_layout)
        
        # Botones de creación de clip
        clip_buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        
        self.create_clip_btn = Button(
            text="✂️ Crear Clip",
            disabled=True,
            on_press=self.create_clip_from_downloaded
        )
        clip_buttons_layout.add_widget(self.create_clip_btn)
        
        clip_config_layout.add_widget(clip_buttons_layout)
        content_layout.add_widget(clip_config_layout)
        
        # Estado y progreso
        self.status_label = Label(
            text="💡 Ingresa una URL de YouTube para comenzar",
            size_hint_y=None,
            height='30dp'
        )
        content_layout.add_widget(self.status_label)
        
        self.progress_label = Label(
            text="",
            size_hint_y=None,
            height='30dp'
        )
        content_layout.add_widget(self.progress_label)
        
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)
    
    def analyze_video(self, instance):
        """Analiza el video de YouTube"""
        url = self.url_input.text.strip()
        if not url:
            self.show_error("Por favor ingresa una URL válida")
            return
        
        self.status_label.text = "🔍 Analizando video..."
        self.download_btn.disabled = True
        
        # Ejecutar análisis en hilo separado
        threading.Thread(target=self._analyze_video_thread, args=(url,), daemon=True).start()
    
    def _analyze_video_thread(self, url):
        """Análisis en hilo separado"""
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
            # Actualizar UI en el hilo principal
            Clock.schedule_once(lambda dt: self._on_video_analyzed(info), 0)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_analyze_error(str(e)), 0)
    
    def _on_video_analyzed(self, info):
        """Callback cuando el video se analiza correctamente"""
        self.video_info = info
        
        # Actualizar información del video
        self.video_info_widget.display_info(info)
        
        # Crear timeline
        duration = info.get('duration', 300)
        self.timeline_widget = TimelineWidget(duration=duration, size_hint_y=None, height='300dp')
        
        self.timeline_container.clear_widgets()
        self.timeline_container.add_widget(self.timeline_widget)
        
        # Habilitar botón de descarga
        self.download_btn.disabled = False
        self.status_label.text = "✅ Video analizado correctamente"
    
    def _on_analyze_error(self, error):
        """Callback cuando hay error en el análisis"""
        self.show_error(f"Error analizando video: {error}")
        self.status_label.text = "❌ Error en el análisis"
    
    def download_video(self, instance):
        """Descarga el video completo"""
        if not self.video_info:
            return
        
        self.download_btn.disabled = True
        self.status_label.text = "📥 Descargando video..."
        self.download_progress.value = 0
        
        url = self.url_input.text.strip()
        threading.Thread(target=self._download_video_thread, args=(url,), daemon=True).start()
    
    def _download_video_thread(self, url):
        """Descarga en hilo separado"""
        try:
            download_dir = Path("downloads")
            download_dir.mkdir(exist_ok=True)
            
            def progress_hook(d):
                if d['status'] == 'downloading':
                    if '_percent_str' in d:
                        try:
                            percent = float(d['_percent_str'].replace('%', ''))
                            Clock.schedule_once(lambda dt: self._update_progress(percent), 0)
                        except:
                            pass
                elif d['status'] == 'finished':
                    Clock.schedule_once(lambda dt: self._on_download_finished(d['filename']), 0)
            
            ydl_opts = {
                'format': 'best[height<=720]/best',
                'outtmpl': str(download_dir / '%(title)s.%(ext)s'),
                'noplaylist': True,
                'progress_hooks': [progress_hook],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_download_error(str(e)), 0)
    
    def _update_progress(self, percent):
        """Actualiza la barra de progreso"""
        self.download_progress.value = min(100, percent)
        self.progress_label.text = f"Descargando... {percent:.1f}%"
    
    def _on_download_finished(self, filename):
        """Callback cuando la descarga termina"""
        self.downloaded_video_path = filename
        self.download_progress.value = 100
        self.status_label.text = "✅ Video descargado exitosamente"
        self.progress_label.text = f"📁 {Path(filename).name}"
        self.create_clip_btn.disabled = False
        self.download_btn.disabled = False
    
    def _on_download_error(self, error):
        """Callback cuando hay error en descarga"""
        self.show_error(f"Error descargando: {error}")
        self.download_btn.disabled = False
        self.status_label.text = "❌ Error en la descarga"
    
    def create_clip_from_downloaded(self, instance):
        """Crea clip del video descargado"""
        if not self.downloaded_video_path or not self.timeline_widget:
            self.show_error("Primero debes descargar el video")
            return
        
        start_time, end_time = self.timeline_widget.get_times()
        clip_name = self.clip_name_input.text.strip() or f"clip_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        output_format = self.format_spinner.text
        
        self.create_clip_btn.disabled = True
        self.status_label.text = "✂️ Creando clip..."
        
        threading.Thread(
            target=self._create_clip_thread,
            args=(self.downloaded_video_path, start_time, end_time, clip_name, output_format),
            daemon=True
        ).start()
    
    def _create_clip_thread(self, video_path, start_time, end_time, clip_name, output_format):
        """Crea clip en hilo separado"""
        try:
            output_dir = Path("downloads")
            output_dir.mkdir(exist_ok=True)
            output_path = output_dir / f"{clip_name}.{output_format}"
            
            # Convertir tiempos a formato FFmpeg
            start_time_str = self.seconds_to_time(start_time)
            duration = end_time - start_time
            
            # Comando FFmpeg
            cmd = [
                "ffmpeg", "-y",
                "-i", video_path,
                "-ss", start_time_str,
                "-t", str(duration),
                "-c", "copy",
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                Clock.schedule_once(lambda dt: self._on_clip_created(str(output_path)), 0)
            else:
                Clock.schedule_once(lambda dt: self._on_clip_error(result.stderr), 0)
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_clip_error(str(e)), 0)
    
    def _on_clip_created(self, output_path):
        """Callback cuando el clip se crea exitosamente"""
        self.status_label.text = "✅ ¡Clip creado exitosamente!"
        self.progress_label.text = f"📁 {Path(output_path).name}"
        self.create_clip_btn.disabled = False
        
        # Mostrar popup de éxito
        self.show_success(f"Clip guardado en:\n{output_path}")
    
    def _on_clip_error(self, error):
        """Callback cuando hay error creando clip"""
        self.show_error(f"Error creando clip: {error}")
        self.create_clip_btn.disabled = False
        self.status_label.text = "❌ Error creando clip"
    
    def seconds_to_time(self, seconds):
        """Convierte segundos a formato HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def show_error(self, message):
        """Muestra popup de error"""
        popup = Popup(
            title='❌ Error',
            content=Label(text=message, text_size=(None, None)),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def show_success(self, message):
        """Muestra popup de éxito"""
        popup = Popup(
            title='✅ Éxito',
            content=Label(text=message, text_size=(None, None)),
            size_hint=(0.8, 0.4)
        )
        popup.open()

class LocalVideoTab(TabbedPanelItem):
    """Pestaña para procesar videos locales"""
    
    def __init__(self, **kwargs):
        super().__init__(text="📁 Videos Locales", **kwargs)
        self.video_path = None
        self.video_info = None
        self.timeline_widget = None
        self.create_content()
    
    def create_content(self):
        main_layout = BoxLayout(orientation='vertical', spacing=15, padding=20)
        
        # Título
        title = Label(
            text="📁 Procesador de Videos Locales",
            font_size='24sp',
            bold=True,
            size_hint_y=None,
            height='50dp'
        )
        main_layout.add_widget(title)
        
        # ScrollView para contenido
        scroll = ScrollView()
        content_layout = BoxLayout(orientation='vertical', spacing=15, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Selección de archivo
        file_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        
        select_btn = Button(
            text="📎 Seleccionar Video",
            size_hint_x=None,
            width='200dp',
            on_press=self.select_video_file
        )
        file_layout.add_widget(select_btn)
        
        self.file_label = Label(text="Ningún archivo seleccionado", halign='left')
        file_layout.add_widget(self.file_label)
        content_layout.add_widget(file_layout)
        
        # Análisis de archivo
        analyze_btn = Button(
            text="🔍 Analizar Archivo",
            size_hint_y=None,
            height='40dp',
            disabled=True,
            on_press=self.analyze_video_file
        )
        self.analyze_btn = analyze_btn
        content_layout.add_widget(analyze_btn)
        
        # Información del video
        self.video_info_widget = VideoInfoWidget(size_hint_y=None, height='200dp')
        content_layout.add_widget(self.video_info_widget)
        
        # Timeline
        self.timeline_container = BoxLayout(orientation='vertical', size_hint_y=None, height='300dp')
        content_layout.add_widget(self.timeline_container)
        
        # Configuración de clip
        clip_config_layout = BoxLayout(orientation='vertical', size_hint_y=None, height='160dp')
        
        # Nombre del clip
        name_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        name_layout.add_widget(Label(text="📝 Nombre:", size_hint_x=None, width='100dp'))
        self.clip_name_input = TextInput(
            text=f"clip_local_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            multiline=False,
            size_hint_y=None,
            height='30dp'
        )
        name_layout.add_widget(self.clip_name_input)
        clip_config_layout.add_widget(name_layout)
        
        # Método de procesamiento
        method_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        method_layout.add_widget(Label(text="⚙️ Método:", size_hint_x=None, width='100dp'))
        self.method_spinner = Spinner(
            text='✂️ Clip Directo (Rápido)',
            values=['✂️ Clip Directo (Rápido)', '🎞️ Convertir y Crear (Calidad)'],
            size_hint_y=None,
            height='30dp'
        )
        method_layout.add_widget(self.method_spinner)
        clip_config_layout.add_widget(method_layout)
        
        # Botones de creación
        clip_buttons_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        
        self.create_clip_btn = Button(
            text="🚀 Crear Clip",
            disabled=True,
            on_press=self.create_local_clip
        )
        clip_buttons_layout.add_widget(self.create_clip_btn)
        
        clear_btn = Button(
            text="🗑️ Limpiar",
            size_hint_x=None,
            width='100dp',
            on_press=self.clear_selection
        )
        clip_buttons_layout.add_widget(clear_btn)
        
        clip_config_layout.add_widget(clip_buttons_layout)
        content_layout.add_widget(clip_config_layout)
        
        # Estado
        self.status_label = Label(
            text="💡 Selecciona un archivo de video para comenzar",
            size_hint_y=None,
            height='30dp'
        )
        content_layout.add_widget(self.status_label)
        
        self.progress_label = Label(
            text="",
            size_hint_y=None,
            height='30dp'
        )
        content_layout.add_widget(self.progress_label)
        
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        self.add_widget(main_layout)
    
    def select_video_file(self, instance):
        """Abre selector de archivos"""
        content = BoxLayout(orientation='vertical')
        
        # FileChooser
        filechooser = FileChooserIconView(
            path=str(Path.home()),
            filters=['*.mp4', '*.avi', '*.mkv', '*.mov', '*.wmv', '*.flv', 
                    '*.webm', '*.m4v', '*.mpg', '*.mpeg', '*.3gp']
        )
        content.add_widget(filechooser)
        
        # Botones
        buttons_layout = BoxLayout(size_hint_y=None, height='50dp')
        
        def on_select():
            if filechooser.selection:
                self.video_path = filechooser.selection[0]
                self.file_label.text = f"📁 {Path(self.video_path).name}"
                self.analyze_btn.disabled = False
                self.status_label.text = f"Archivo seleccionado: {Path(self.video_path).name}"
            popup.dismiss()
        
        def on_cancel():
            popup.dismiss()
        
        select_btn = Button(text="Seleccionar", on_press=lambda x: on_select())
        cancel_btn = Button(text="Cancelar", on_press=lambda x: on_cancel())
        
        buttons_layout.add_widget(select_btn)
        buttons_layout.add_widget(cancel_btn)
        content.add_widget(buttons_layout)
        
        popup = Popup(
            title='Seleccionar Archivo de Video',
            content=content,
            size_hint=(0.9, 0.9)
        )
        popup.open()
    
    def analyze_video_file(self, instance):
        """Analiza el archivo de video local"""
        if not self.video_path:
            return
        
        self.status_label.text = "🔍 Analizando archivo..."
        self.analyze_btn.disabled = True
        
        threading.Thread(target=self._analyze_local_video_thread, daemon=True).start()
    
    def _analyze_local_video_thread(self):
        """Análisis en hilo separado"""
        try:
            # Usar ffprobe para obtener información
            cmd = [
                "ffprobe", "-v", "quiet", "-print_format", "json",
                "-show_format", "-show_streams", self.video_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                probe_data = json.loads(result.stdout)
                
                # Procesar información
                format_info = probe_data.get('format', {})
                video_stream = None
                
                for stream in probe_data.get('streams', []):
                    if stream.get('codec_type') == 'video':
                        video_stream = stream
                        break
                
                if video_stream:
                    info = {
                        'title': Path(self.video_path).stem,
                        'duration': float(format_info.get('duration', 0)),
                        'width': video_stream.get('width', 0),
                        'height': video_stream.get('height', 0),
                        'codec': video_stream.get('codec_name', 'desconocido'),
                        'filesize': int(format_info.get('size', 0)),
                        'format': format_info.get('format_name', 'desconocido'),
                        'uploader': 'Archivo Local',
                        'upload_date': datetime.fromtimestamp(
                            Path(self.video_path).stat().st_mtime
                        ).strftime('%Y%m%d'),
                        'view_count': None
                    }
                    
                    Clock.schedule_once(lambda dt: self._on_local_video_analyzed(info), 0)
                else:
                    Clock.schedule_once(lambda dt: self._on_local_analyze_error("No se encontró stream de video"), 0)
            else:
                Clock.schedule_once(lambda dt: self._on_local_analyze_error(result.stderr), 0)
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_local_analyze_error(str(e)), 0)
    
    def _on_local_video_analyzed(self, info):
        """Callback cuando el análisis local termina"""
        self.video_info = info
        
        # Mostrar información
        self.video_info_widget.display_info(info)
        
        # Crear timeline
        duration = int(info.get('duration', 300))
        self.timeline_widget = TimelineWidget(duration=duration, size_hint_y=None, height='300dp')
        
        self.timeline_container.clear_widgets()
        self.timeline_container.add_widget(self.timeline_widget)
        
        # Habilitar creación de clips
        self.create_clip_btn.disabled = False
        self.analyze_btn.disabled = False
        self.status_label.text = "✅ Archivo analizado correctamente"
    
    def _on_local_analyze_error(self, error):
        """Callback cuando hay error en análisis local"""
        self.show_error(f"Error analizando archivo: {error}")
        self.analyze_btn.disabled = False
        self.status_label.text = "❌ Error en el análisis"
    
    def create_local_clip(self, instance):
        """Crea clip del video local"""
        if not self.video_path or not self.timeline_widget:
            self.show_error("Primero selecciona y analiza un video")
            return
        
        start_time, end_time = self.timeline_widget.get_times()
        clip_name = self.clip_name_input.text.strip() or f"clip_local_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        method = self.method_spinner.text
        
        self.create_clip_btn.disabled = True
        self.status_label.text = "✂️ Creando clip..."
        
        threading.Thread(
            target=self._create_local_clip_thread,
            args=(start_time, end_time, clip_name, method),
            daemon=True
        ).start()
    
    def _create_local_clip_thread(self, start_time, end_time, clip_name, method):
        """Crea clip local en hilo separado"""
        try:
            output_dir = Path("downloads")
            output_dir.mkdir(exist_ok=True)
            
            # Determinar extensión y comando según método
            if "Directo" in method:
                # Mantener extensión original
                extension = Path(self.video_path).suffix
                output_path = output_dir / f"{clip_name}{extension}"
                
                # Comando para clip directo
                cmd = [
                    "ffmpeg", "-y",
                    "-i", self.video_path,
                    "-ss", self.seconds_to_time(start_time),
                    "-t", str(end_time - start_time),
                    "-c", "copy",  # Copiar sin re-codificar
                    str(output_path)
                ]
            else:
                # Convertir a MP4
                output_path = output_dir / f"{clip_name}.mp4"
                
                # Comando para conversión
                cmd = [
                    "ffmpeg", "-y",
                    "-i", self.video_path,
                    "-ss", self.seconds_to_time(start_time),
                    "-t", str(end_time - start_time),
                    "-c:v", "libx264",
                    "-c:a", "aac",
                    "-preset", "medium",
                    "-crf", "23",
                    str(output_path)
                ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                Clock.schedule_once(lambda dt: self._on_local_clip_created(str(output_path)), 0)
            else:
                Clock.schedule_once(lambda dt: self._on_local_clip_error(result.stderr), 0)
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_local_clip_error(str(e)), 0)
    
    def _on_local_clip_created(self, output_path):
        """Callback cuando el clip local se crea"""
        self.status_label.text = "✅ ¡Clip creado exitosamente!"
        self.progress_label.text = f"📁 {Path(output_path).name}"
        self.create_clip_btn.disabled = False
        self.show_success(f"Clip guardado en:\n{output_path}")
    
    def _on_local_clip_error(self, error):
        """Callback cuando hay error creando clip local"""
        self.show_error(f"Error creando clip: {error}")
        self.create_clip_btn.disabled = False
        self.status_label.text = "❌ Error creando clip"
    
    def clear_selection(self, instance):
        """Limpia la selección actual"""
        self.video_path = None
        self.video_info = None
        self.timeline_widget = None
        
        self.file_label.text = "Ningún archivo seleccionado"
        self.analyze_btn.disabled = True
        self.create_clip_btn.disabled = True
        self.video_info_widget.clear_widgets()
        self.timeline_container.clear_widgets()
        self.status_label.text = "💡 Selecciona un archivo de video para comenzar"
        self.progress_label.text = ""
    
    def seconds_to_time(self, seconds):
        """Convierte segundos a formato HH:MM:SS"""
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def show_error(self, message):
        """Muestra popup de error"""
        popup = Popup(
            title='❌ Error',
            content=Label(text=message, text_size=(None, None)),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def show_success(self, message):
        """Muestra popup de éxito"""
        popup = Popup(
            title='✅ Éxito',
            content=Label(text=message, text_size=(None, None)),
            size_hint=(0.8, 0.4)
        )
        popup.open()

class DownloadTab(TabbedPanelItem):
    """Pestaña para descargar videos sin crear clips"""
    
    def __init__(self, **kwargs):
        super().__init__(text="📥 Descargas", **kwargs)
        self.create_content()
    
    def create_content(self):
        main_layout = BoxLayout(orientation='vertical', spacing=15, padding=20)
        
        # Título
        title = Label(
            text="📥 Descargador de Videos",
            font_size='24sp',
            bold=True,
            size_hint_y=None,
            height='50dp'
        )
        main_layout.add_widget(title)
        
        # URL Input
        url_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='60dp')
        url_layout.add_widget(Label(text="🔗 URL:", size_hint_x=None, width='80dp'))
        
        self.url_input = TextInput(
            hint_text="https://www.youtube.com/watch?v=...",
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        url_layout.add_widget(self.url_input)
        main_layout.add_widget(url_layout)
        
        # Opciones de descarga
        options_layout = GridLayout(cols=2, spacing=15, size_hint_y=None, height='120dp')
        
        # Calidad
        options_layout.add_widget(Label(text="🎯 Calidad:", halign='left'))
        self.quality_spinner = Spinner(
            text='Mejor disponible',
            values=['Mejor disponible', '720p', '480p', '360p', 'Solo audio (MP3)'],
            size_hint_y=None,
            height='40dp'
        )
        options_layout.add_widget(self.quality_spinner)
        
        # Directorio
        options_layout.add_widget(Label(text="📁 Directorio:", halign='left'))
        dir_layout = BoxLayout(orientation='horizontal')
        self.dir_input = TextInput(
            text="downloads",
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        dir_layout.add_widget(self.dir_input)
        
        select_dir_btn = Button(
            text="📂",
            size_hint_x=None,
            width='50dp',
            on_press=self.select_directory
        )
        dir_layout.add_widget(select_dir_btn)
        options_layout.add_widget(dir_layout)
        
        main_layout.add_widget(options_layout)
        
        # Opciones adicionales
        extras_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        
        self.subtitles_checkbox = CheckBox(size_hint_x=None, width='30dp')
        extras_layout.add_widget(self.subtitles_checkbox)
        extras_layout.add_widget(Label(text="📝 Incluir subtítulos"))
        
        main_layout.add_widget(extras_layout)
        
        # Botón de descarga
        download_btn = Button(
            text="📥 Descargar Video",
            size_hint_y=None,
            height='60dp',
            on_press=self.download_video
        )
        main_layout.add_widget(download_btn)
        
        # Progreso
        self.progress_bar = ProgressBar(size_hint_y=None, height='20dp')
        main_layout.add_widget(self.progress_bar)
        
        # Estado
        self.status_label = Label(
            text="💡 Ingresa una URL para descargar",
            size_hint_y=None,
            height='40dp'
        )
        main_layout.add_widget(self.status_label)
        
        # Historial de descargas
        history_title = Label(
            text="📋 Historial de Descargas",
            font_size='18sp',
            bold=True,
            size_hint_y=None,
            height='40dp'
        )
        main_layout.add_widget(history_title)
        
        scroll = ScrollView()
        self.history_layout = BoxLayout(
            orientation='vertical', 
            size_hint_y=None,
            spacing=5
        )
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        scroll.add_widget(self.history_layout)
        main_layout.add_widget(scroll)
        
        self.add_widget(main_layout)
    
    def select_directory(self, instance):
        """Selecciona directorio de descarga"""
        # Por simplicidad, usar un popup con input de texto
        content = BoxLayout(orientation='vertical', spacing=10)
        
        content.add_widget(Label(text="Ingresa la ruta del directorio:"))
        
        path_input = TextInput(
            text=self.dir_input.text,
            multiline=False,
            size_hint_y=None,
            height='40dp'
        )
        content.add_widget(path_input)
        
        buttons_layout = BoxLayout(size_hint_y=None, height='50dp')
        
        def on_ok():
            self.dir_input.text = path_input.text
            popup.dismiss()
        
        ok_btn = Button(text="OK", on_press=lambda x: on_ok())
        cancel_btn = Button(text="Cancelar", on_press=lambda x: popup.dismiss())
        
        buttons_layout.add_widget(ok_btn)
        buttons_layout.add_widget(cancel_btn)
        content.add_widget(buttons_layout)
        
        popup = Popup(
            title='Seleccionar Directorio',
            content=content,
            size_hint=(0.6, 0.4)
        )
        popup.open()
    
    def download_video(self, instance):
        """Descarga el video"""
        url = self.url_input.text.strip()
        if not url:
            self.show_error("Por favor ingresa una URL válida")
            return
        
        self.status_label.text = "📥 Iniciando descarga..."
        self.progress_bar.value = 0
        
        # Configurar opciones
        download_dir = self.dir_input.text or "downloads"
        quality = self.quality_spinner.text
        include_subtitles = self.subtitles_checkbox.active
        
        threading.Thread(
            target=self._download_thread,
            args=(url, download_dir, quality, include_subtitles),
            daemon=True
        ).start()
    
    def _download_thread(self, url, download_dir, quality, include_subtitles):
        """Descarga en hilo separado"""
        try:
            Path(download_dir).mkdir(exist_ok=True)
            
            # Configurar yt-dlp
            ydl_opts = {
                'outtmpl': f"{download_dir}/%(title)s.%(ext)s",
                'noplaylist': True,
            }
            
            # Configurar calidad
            quality_map = {
                "Mejor disponible": "best",
                "720p": "best[height<=720]",
                "480p": "best[height<=480]",
                "360p": "best[height<=360]",
                "Solo audio (MP3)": "bestaudio/best"
            }
            
            ydl_opts['format'] = quality_map.get(quality, "best")
            
            # Audio only
            if quality == "Solo audio (MP3)":
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            
            # Subtítulos
            if include_subtitles:
                ydl_opts.update({
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'subtitleslangs': ['es', 'en'],
                })
            
            # Hook de progreso
            def progress_hook(d):
                if d['status'] == 'downloading':
                    if '_percent_str' in d:
                        try:
                            percent = float(d['_percent_str'].replace('%', ''))
                            Clock.schedule_once(lambda dt: self._update_download_progress(percent), 0)
                        except:
                            pass
                elif d['status'] == 'finished':
                    Clock.schedule_once(lambda dt: self._on_download_complete(d['filename']), 0)
            
            ydl_opts['progress_hooks'] = [progress_hook]
            
            # Descargar
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_download_error(str(e)), 0)
    
    def _update_download_progress(self, percent):
        """Actualiza progreso de descarga"""
        self.progress_bar.value = min(100, percent)
        self.status_label.text = f"📥 Descargando... {percent:.1f}%"
    
    def _on_download_complete(self, filename):
        """Callback cuando descarga completa"""
        self.progress_bar.value = 100
        self.status_label.text = "✅ ¡Descarga completada!"
        
        # Agregar al historial
        file_info = BoxLayout(orientation='horizontal', size_hint_y=None, height='30dp')
        file_info.add_widget(Label(
            text=f"✅ {Path(filename).name}",
            halign='left',
            text_size=(None, None)
        ))
        file_info.add_widget(Label(
            text=datetime.now().strftime('%H:%M:%S'),
            size_hint_x=None,
            width='80dp'
        ))
        
        self.history_layout.add_widget(file_info)
        
        self.show_success(f"Archivo descargado:\n{filename}")
    
    def _on_download_error(self, error):
        """Callback cuando hay error en descarga"""
        self.show_error(f"Error descargando: {error}")
        self.status_label.text = "❌ Error en la descarga"
    
    def show_error(self, message):
        """Muestra popup de error"""
        popup = Popup(
            title='❌ Error',
            content=Label(text=message, text_size=(None, None)),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def show_success(self, message):
        """Muestra popup de éxito"""
        popup = Popup(
            title='✅ Éxito',
            content=Label(text=message, text_size=(None, None)),
            size_hint=(0.8, 0.4)
        )
        popup.open()

class YouTubeDownloaderApp(App):
    """Aplicación principal"""
    
    def build(self):
        self.title = "🎬 YouTube Downloader Pro - Desktop Edition"
        
        # Panel con pestañas
        tabs = TabbedPanel(do_default_tab=False)
        
        # Pestaña de YouTube
        youtube_tab = YouTubeTab()
        tabs.add_widget(youtube_tab)
        
        # Pestaña de videos locales
        local_tab = LocalVideoTab()
        tabs.add_widget(local_tab)
        
        # Pestaña de descargas
        download_tab = DownloadTab()
        tabs.add_widget(download_tab)
        
        return tabs

if __name__ == '__main__':
    # Verificar dependencias
    try:
        import yt_dlp
    except ImportError:
        print("❌ Error: yt-dlp no está instalado")
        print("Instala con: pip install yt-dlp")
        sys.exit(1)
    
    # Verificar FFmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode != 0:
            raise FileNotFoundError
    except FileNotFoundError:
        print("❌ Error: FFmpeg no está instalado o no está en el PATH")
        print("Descarga FFmpeg desde: https://ffmpeg.org/download.html")
        sys.exit(1)
    
    print("🚀 Iniciando YouTube Downloader Pro - Desktop Edition")
    YouTubeDownloaderApp().run()
