#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 YouTube Downloader Pro - Kivy Desktop Edition (Mejorada)
Versión mejorada con KivyMD para mejor interfaz
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
from kivy.uix.switch import Switch
from kivy.uix.checkbox import CheckBox
from kivy.clock import Clock
from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.logger import Logger
from kivy.uix.image import AsyncImage
from kivy.core.window import Window

# KivyMD (si está disponible)
try:
    from kivymd.app import MDApp
    from kivymd.uix.button import MDRaisedButton, MDIconButton
    from kivymd.uix.card import MDCard
    from kivymd.uix.label import MDLabel
    from kivymd.uix.textfield import MDTextField
    from kivymd.uix.progressbar import MDProgressBar
    from kivymd.uix.tab import MDTabs, MDTabsBase
    from kivymd.uix.boxlayout import MDBoxLayout
    from kivymd.uix.gridlayout import MDGridLayout
    from kivymd.uix.screen import MDScreen
    from kivymd.uix.toolbar import MDTopAppBar
    KIVYMD_AVAILABLE = True
except ImportError:
    KIVYMD_AVAILABLE = False

# YouTube DLP
import yt_dlp

# Configurar Kivy
kivy.require('2.0.0')

class ModernTimelineWidget(BoxLayout):
    """Timeline moderno con mejor diseño"""
    
    def __init__(self, duration=300, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.duration = duration
        self.start_time = 0
        self.end_time = min(60, duration)
        self.spacing = 10
        self.padding = [15, 10]
        
        self.create_timeline()
    
    def create_timeline(self):
        self.clear_widgets()
        
        # Header con información
        header_card = self.create_card()
        header_layout = BoxLayout(orientation='vertical', spacing=5, padding=15)
        
        title_label = Label(
            text="🎬 Timeline de Edición",
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height='35dp',
            color=(1, 1, 1, 1)
        )
        header_layout.add_widget(title_label)
        
        duration_label = Label(
            text=f"⏱️ Duración total: {self.format_time(self.duration)}",
            font_size='16sp',
            size_hint_y=None,
            height='25dp',
            color=(0.8, 0.8, 0.8, 1)
        )
        header_layout.add_widget(duration_label)
        
        header_card.add_widget(header_layout)
        self.add_widget(header_card)
        
        # Timeline principal
        timeline_card = self.create_card()
        timeline_layout = BoxLayout(orientation='vertical', spacing=15, padding=15)
        
        # Slider de inicio
        start_container = BoxLayout(orientation='vertical', spacing=5)
        start_label = Label(
            text="🕐 Tiempo de Inicio",
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height='25dp',
            color=(0.3, 0.7, 1, 1)
        )
        start_container.add_widget(start_label)
        
        start_slider_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        self.start_slider = Slider(
            min=0,
            max=max(0, self.duration-1),
            value=self.start_time,
            step=1,
            size_hint_x=0.8
        )
        self.start_slider.bind(value=self.on_start_change)
        start_slider_layout.add_widget(self.start_slider)
        
        self.start_time_label = Label(
            text=self.format_time(self.start_time),
            size_hint_x=0.2,
            font_size='14sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        start_slider_layout.add_widget(self.start_time_label)
        start_container.add_widget(start_slider_layout)
        timeline_layout.add_widget(start_container)
        
        # Slider de fin
        end_container = BoxLayout(orientation='vertical', spacing=5)
        end_label = Label(
            text="🏁 Tiempo de Fin",
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height='25dp',
            color=(1, 0.5, 0.3, 1)
        )
        end_container.add_widget(end_label)
        
        end_slider_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp')
        self.end_slider = Slider(
            min=self.start_time+1,
            max=self.duration,
            value=self.end_time,
            step=1,
            size_hint_x=0.8
        )
        self.end_slider.bind(value=self.on_end_change)
        end_slider_layout.add_widget(self.end_slider)
        
        self.end_time_label = Label(
            text=self.format_time(self.end_time),
            size_hint_x=0.2,
            font_size='14sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        end_slider_layout.add_widget(self.end_time_label)
        end_container.add_widget(end_slider_layout)
        timeline_layout.add_widget(end_container)
        
        # Barra de progreso visual
        progress_container = BoxLayout(orientation='vertical', spacing=5)
        progress_label = Label(
            text="📊 Previsualización del Clip",
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height='25dp',
            color=(0.5, 1, 0.5, 1)
        )
        progress_container.add_widget(progress_label)
        
        self.progress_bar = ProgressBar(
            max=100,
            value=self.get_progress_percentage(),
            size_hint_y=None,
            height='25dp'
        )
        progress_container.add_widget(self.progress_bar)
        
        # Información del clip
        self.clip_info_label = Label(
            text=self.get_clip_info_text(),
            size_hint_y=None,
            height='30dp',
            font_size='14sp',
            color=(1, 1, 0.7, 1)
        )
        progress_container.add_widget(self.clip_info_label)
        timeline_layout.add_widget(progress_container)
        
        timeline_card.add_widget(timeline_layout)
        self.add_widget(timeline_card)
        
        # Botones rápidos
        quick_card = self.create_card()
        quick_layout = BoxLayout(orientation='vertical', spacing=10, padding=15)
        
        quick_title = Label(
            text="⚡ Configuraciones Rápidas",
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height='25dp',
            color=(1, 0.8, 0.3, 1)
        )
        quick_layout.add_widget(quick_title)
        
        buttons_grid = GridLayout(cols=4, spacing=10, size_hint_y=None, height='50dp')
        
        quick_buttons = [
            ("📺 30s", 0, 30, (0.3, 0.7, 1, 1)),
            ("🎵 1min", 0, 60, (0.7, 0.3, 1, 1)),
            ("📹 2min", 0, 120, (1, 0.5, 0.3, 1)),
            ("🎬 5min", 0, 300, (0.5, 1, 0.3, 1))
        ]
        
        for text, start, end, color in quick_buttons:
            btn = Button(
                text=text,
                background_color=color,
                on_press=lambda x, s=start, e=end: self.set_quick_time(s, e)
            )
            buttons_grid.add_widget(btn)
        
        quick_layout.add_widget(buttons_grid)
        quick_card.add_widget(quick_layout)
        self.add_widget(quick_card)
    
    def create_card(self):
        """Crea una tarjeta con estilo moderno"""
        if KIVYMD_AVAILABLE:
            card = MDCard(
                elevation=3,
                padding=0,
                size_hint_y=None,
                md_bg_color=(0.1, 0.1, 0.1, 0.9)
            )
        else:
            card = BoxLayout(
                size_hint_y=None,
                padding=2
            )
            # Simular card con color de fondo
            with card.canvas.before:
                from kivy.graphics import Color, Rectangle
                Color(0.1, 0.1, 0.1, 0.9)
                card.rect = Rectangle(size=card.size, pos=card.pos)
            
            def update_rect(instance, value):
                card.rect.pos = instance.pos
                card.rect.size = instance.size
            
            card.bind(size=update_rect, pos=update_rect)
        
        return card
    
    def on_start_change(self, instance, value):
        self.start_time = int(value)
        self.start_time_label.text = self.format_time(self.start_time)
        
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
        return f"📏 Duración del clip: {self.format_time(clip_duration)} ({percentage:.1f}% del video original)"
    
    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"
    
    def get_times(self):
        return self.start_time, self.end_time

class ModernVideoInfoWidget(BoxLayout):
    """Widget moderno para mostrar información del video"""
    
    def __init__(self, video_info=None, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.spacing = 10
        self.padding = 15
        
        if video_info:
            self.display_info(video_info)
    
    def display_info(self, info):
        self.clear_widgets()
        
        # Card principal
        main_card = self.create_card()
        card_layout = BoxLayout(orientation='vertical', spacing=15, padding=20)
        
        # Título del video
        title_label = Label(
            text=f"🎬 {info.get('title', 'Sin título')}",
            font_size='22sp',
            bold=True,
            text_size=(None, None),
            halign='center',
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height='60dp'
        )
        title_label.bind(texture_size=title_label.setter('text_size'))
        card_layout.add_widget(title_label)
        
        # Grid con información
        info_grid = GridLayout(cols=2, spacing=15, size_hint_y=None, height='120dp')
        
        # Canal
        info_grid.add_widget(self.create_info_item("👤 Canal", info.get('uploader', 'Desconocido')))
        
        # Duración
        duration = self.format_duration(info.get('duration', 0))
        info_grid.add_widget(self.create_info_item("⏱️ Duración", duration))
        
        # Fecha
        upload_date = info.get('upload_date', 'Desconocida')
        if len(upload_date) == 8:
            formatted_date = f"{upload_date[6:8]}/{upload_date[4:6]}/{upload_date[0:4]}"
        else:
            formatted_date = upload_date
        info_grid.add_widget(self.create_info_item("📅 Subido", formatted_date))
        
        # Vistas
        view_count = info.get('view_count', 0)
        views_text = f"{view_count:,}" if view_count else "N/A"
        info_grid.add_widget(self.create_info_item("👁️ Vistas", views_text))
        
        card_layout.add_widget(info_grid)
        
        # Información técnica adicional
        if 'width' in info and 'height' in info:
            resolution = f"{info['width']}x{info['height']}"
            tech_info = Label(
                text=f"🎯 Resolución: {resolution} | 📋 Formato: {info.get('ext', 'N/A')}",
                size_hint_y=None,
                height='30dp',
                font_size='14sp',
                color=(0.8, 0.8, 1, 1)
            )
            card_layout.add_widget(tech_info)
        
        main_card.add_widget(card_layout)
        self.add_widget(main_card)
    
    def create_card(self):
        """Crea una tarjeta moderna"""
        if KIVYMD_AVAILABLE:
            return MDCard(
                elevation=5,
                padding=0,
                size_hint_y=None,
                md_bg_color=(0.05, 0.05, 0.15, 0.95)
            )
        else:
            card = BoxLayout(size_hint_y=None, padding=3)
            with card.canvas.before:
                from kivy.graphics import Color, Rectangle
                Color(0.05, 0.05, 0.15, 0.95)
                card.rect = Rectangle(size=card.size, pos=card.pos)
            
            def update_rect(instance, value):
                card.rect.pos = instance.pos
                card.rect.size = instance.size
            
            card.bind(size=update_rect, pos=update_rect)
            return card
    
    def create_info_item(self, label_text, value_text):
        """Crea un item de información"""
        item_layout = BoxLayout(orientation='vertical', spacing=5)
        
        label = Label(
            text=label_text,
            font_size='16sp',
            bold=True,
            size_hint_y=None,
            height='25dp',
            color=(0.7, 0.9, 1, 1)
        )
        
        value = Label(
            text=str(value_text),
            font_size='14sp',
            size_hint_y=None,
            height='25dp',
            color=(1, 1, 1, 1)
        )
        
        item_layout.add_widget(label)
        item_layout.add_widget(value)
        return item_layout
    
    def format_duration(self, seconds):
        if not seconds:
            return "Desconocida"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes:02d}:{seconds:02d}"

class YouTubeDownloaderKivyApp(App):
    """Aplicación principal mejorada"""
    
    def build(self):
        self.title = "🎬 YouTube Downloader Pro - Desktop Edition"
        
        # Configurar ventana
        Window.size = (1200, 800)
        Window.minimum_width = 800
        Window.minimum_height = 600
        
        # Panel principal
        main_layout = BoxLayout(orientation='vertical')
        
        # Header
        header = self.create_header()
        main_layout.add_widget(header)
        
        # Tabs mejoradas
        tabs = TabbedPanel(do_default_tab=False, tab_height='50dp')
        
        # YouTube Tab
        youtube_tab = self.create_youtube_tab()
        tabs.add_widget(youtube_tab)
        
        # Local Videos Tab
        local_tab = self.create_local_tab()
        tabs.add_widget(local_tab)
        
        # Downloads Tab
        download_tab = self.create_download_tab()
        tabs.add_widget(download_tab)
        
        main_layout.add_widget(tabs)
        
        # Footer
        footer = self.create_footer()
        main_layout.add_widget(footer)
        
        return main_layout
    
    def create_header(self):
        """Crea el header de la aplicación"""
        header_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='80dp',
            padding=20,
            spacing=15
        )
        
        # Color de fondo
        with header_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.1, 0.1, 0.2, 1)
            header_layout.rect = Rectangle(size=header_layout.size, pos=header_layout.pos)
        
        def update_header_rect(instance, value):
            header_layout.rect.pos = instance.pos
            header_layout.rect.size = instance.size
        
        header_layout.bind(size=update_header_rect, pos=update_header_rect)
        
        # Título
        title_label = Label(
            text="🎬 YouTube Downloader Pro",
            font_size='28sp',
            bold=True,
            color=(1, 1, 1, 1)
        )
        header_layout.add_widget(title_label)
        
        # Información de versión
        version_layout = BoxLayout(orientation='vertical', size_hint_x=None, width='200dp')
        
        version_label = Label(
            text="Desktop Edition v2.0",
            font_size='16sp',
            color=(0.8, 0.8, 1, 1),
            size_hint_y=None,
            height='25dp'
        )
        
        status_label = Label(
            text="🟢 Sistema listo",
            font_size='14sp',
            color=(0.5, 1, 0.5, 1),
            size_hint_y=None,
            height='25dp'
        )
        
        version_layout.add_widget(version_label)
        version_layout.add_widget(status_label)
        header_layout.add_widget(version_layout)
        
        return header_layout
    
    def create_footer(self):
        """Crea el footer de la aplicación"""
        footer_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height='40dp',
            padding=[20, 10]
        )
        
        # Color de fondo
        with footer_layout.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(0.05, 0.05, 0.1, 1)
            footer_layout.rect = Rectangle(size=footer_layout.size, pos=footer_layout.pos)
        
        def update_footer_rect(instance, value):
            footer_layout.rect.pos = instance.pos
            footer_layout.rect.size = instance.size
        
        footer_layout.bind(size=update_footer_rect, pos=update_footer_rect)
        
        # Información
        info_label = Label(
            text="💡 Tip: Usa Ctrl+C para cancelar operaciones | FFmpeg requerido para procesamiento",
            font_size='12sp',
            color=(0.7, 0.7, 0.7, 1)
        )
        footer_layout.add_widget(info_label)
        
        return footer_layout
    
    def create_youtube_tab(self):
        """Crea la pestaña de YouTube mejorada"""
        tab = TabbedPanelItem(text="🎬 YouTube Clips")
        
        main_layout = BoxLayout(orientation='vertical', spacing=15, padding=20)
        
        # Scroll view para contenido
        scroll = ScrollView()
        content_layout = BoxLayout(orientation='vertical', spacing=20, size_hint_y=None)
        content_layout.bind(minimum_height=content_layout.setter('height'))
        
        # Sección de URL
        url_card = self.create_section_card("🔗 Análisis de Video de YouTube")
        url_layout = BoxLayout(orientation='vertical', spacing=10, padding=15)
        
        url_input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp')
        url_input = TextInput(
            hint_text="Pega aquí la URL de YouTube (ej: https://youtube.com/watch?v=...)",
            multiline=False,
            size_hint_y=None,
            height='40dp',
            font_size='14sp'
        )
        url_input_layout.add_widget(url_input)
        
        analyze_btn = Button(
            text="🔍 Analizar",
            size_hint_x=None,
            width='120dp',
            background_color=(0.2, 0.6, 1, 1)
        )
        url_input_layout.add_widget(analyze_btn)
        url_layout.add_widget(url_input_layout)
        
        url_card.add_widget(url_layout)
        content_layout.add_widget(url_card)
        
        # Placeholder para información del video
        info_placeholder = Label(
            text="📋 La información del video aparecerá aquí después del análisis",
            size_hint_y=None,
            height='200dp',
            color=(0.7, 0.7, 0.7, 1)
        )
        content_layout.add_widget(info_placeholder)
        
        scroll.add_widget(content_layout)
        main_layout.add_widget(scroll)
        
        tab.add_widget(main_layout)
        return tab
    
    def create_local_tab(self):
        """Crea la pestaña de videos locales"""
        tab = TabbedPanelItem(text="📁 Videos Locales")
        
        main_layout = BoxLayout(orientation='vertical', spacing=15, padding=20)
        
        # Placeholder content
        placeholder = Label(
            text="📁 Funcionalidad de videos locales\n\n🚧 En desarrollo...",
            font_size='20sp',
            halign='center'
        )
        main_layout.add_widget(placeholder)
        
        tab.add_widget(main_layout)
        return tab
    
    def create_download_tab(self):
        """Crea la pestaña de descargas"""
        tab = TabbedPanelItem(text="📥 Descargas")
        
        main_layout = BoxLayout(orientation='vertical', spacing=15, padding=20)
        
        # Placeholder content
        placeholder = Label(
            text="📥 Centro de descargas\n\n🚧 En desarrollo...",
            font_size='20sp',
            halign='center'
        )
        main_layout.add_widget(placeholder)
        
        tab.add_widget(main_layout)
        return tab
    
    def create_section_card(self, title):
        """Crea una tarjeta de sección"""
        if KIVYMD_AVAILABLE:
            card = MDCard(
                elevation=3,
                padding=0,
                size_hint_y=None,
                md_bg_color=(0.1, 0.1, 0.15, 0.9)
            )
        else:
            card = BoxLayout(
                orientation='vertical',
                size_hint_y=None,
                padding=2
            )
            
            with card.canvas.before:
                from kivy.graphics import Color, Rectangle, RoundedRectangle
                Color(0.1, 0.1, 0.15, 0.9)
                card.rect = RoundedRectangle(size=card.size, pos=card.pos, radius=[10])
            
            def update_card_rect(instance, value):
                card.rect.pos = instance.pos
                card.rect.size = instance.size
            
            card.bind(size=update_card_rect, pos=update_card_rect)
            
            # Título de la sección
            title_label = Label(
                text=title,
                font_size='18sp',
                bold=True,
                size_hint_y=None,
                height='40dp',
                color=(0.8, 0.9, 1, 1)
            )
            card.add_widget(title_label)
        
        return card

if __name__ == '__main__':
    # Verificar dependencias
    try:
        import yt_dlp
        print("✅ yt-dlp disponible")
    except ImportError:
        print("❌ Error: yt-dlp no está instalado")
        print("Instala con: pip install yt-dlp")
        sys.exit(1)
    
    # Verificar FFmpeg
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ FFmpeg disponible")
        else:
            raise FileNotFoundError
    except FileNotFoundError:
        print("⚠️ Advertencia: FFmpeg no detectado")
        print("Algunas funciones pueden no estar disponibles")
    
    # Crear directorio de descargas
    Path("downloads").mkdir(exist_ok=True)
    
    print("🚀 Iniciando YouTube Downloader Pro - Desktop Edition")
    YouTubeDownloaderKivyApp().run()
