#!/usr/bin/env python3
"""
Interfaz gráfica para descargar videos de YouTube usando yt-dlp
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
import subprocess
import yt_dlp
from pathlib import Path
import json
from datetime import datetime
import webbrowser


class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 YouTube Downloader")
        self.root.geometry("800x900")
        self.root.minsize(700, 600)
        
        # Variables
        self.directorio_descarga = tk.StringVar(value="downloads")
        self.url_var = tk.StringVar()
        self.calidad_var = tk.StringVar(value="best")
        self.solo_audio_var = tk.BooleanVar()
        self.subtitulos_var = tk.BooleanVar()
        self.progreso_var = tk.StringVar(value="Listo para descargar...")
        
        # Variables para clips
        self.url_clip_var = tk.StringVar()
        self.inicio_clip_var = tk.StringVar(value="00:00:00")
        self.fin_clip_var = tk.StringVar(value="00:01:00")
        self.nombre_clip_var = tk.StringVar(value="clip_1")
        self.video_temp_path = None
        self.video_info_clip = None
        self.progreso_clip_var = tk.StringVar(value="Listo para crear clips...")
        
        # Variables para procesamiento de archivos locales
        self.archivo_local_var = tk.StringVar()
        self.inicio_archivo_var = tk.StringVar(value="00:00:00")
        self.fin_archivo_var = tk.StringVar(value="00:01:00")
        self.nombre_archivo_clip_var = tk.StringVar(value="clip_archivo_1")
        self.archivo_local_path = None
        self.video_info_archivo = None
        self.progreso_archivo_var = tk.StringVar(value="Listo para procesar archivos...")
        
        # Variable para controlar la descarga
        self.descarga_activa = False
        
        self.crear_interfaz()
        self.centrar_ventana()
        
    def centrar_ventana(self):
        """Centra la ventana en la pantalla"""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.root.winfo_width() // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.root.winfo_height() // 2)
        self.root.geometry(f"+{x}+{y}")
    
    def crear_interfaz(self):
        """Crea la interfaz gráfica"""
        
        # Crear notebook para pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Pestaña de descarga
        self.crear_pestaña_descarga(notebook)
        
        # Pestaña de clips
        self.crear_pestaña_clips(notebook)
        
        # Pestaña de procesamiento de archivos locales
        self.crear_pestaña_archivos(notebook)
        
        # Pestaña de información
        self.crear_pestaña_info(notebook)
        
        # Pestaña de configuración
        self.crear_pestaña_config(notebook)
        
    def crear_pestaña_descarga(self, notebook):
        """Crea la pestaña principal de descarga"""
        
        frame_descarga = ttk.Frame(notebook)
        notebook.add(frame_descarga, text="📥 Descargar")
        
        # Título
        titulo = tk.Label(frame_descarga, text="🎬 YouTube Video Downloader", 
                         font=("Arial", 16, "bold"), fg="#1f4e79")
        titulo.pack(pady=(10, 20))
        
        # URL Input
        url_frame = ttk.LabelFrame(frame_descarga, text="📎 URL del Video", padding=10)
        url_frame.pack(fill=tk.X, padx=20, pady=5)
        
        url_entry = tk.Entry(url_frame, textvariable=self.url_var, font=("Arial", 10))
        url_entry.pack(fill=tk.X, pady=5)
        url_entry.bind('<Return>', lambda e: self.obtener_info_video())
        
        # Botón para obtener información
        btn_info = ttk.Button(url_frame, text="🔍 Obtener Información", 
                             command=self.obtener_info_video)
        btn_info.pack(pady=5)
        
        # Frame de opciones
        opciones_frame = ttk.LabelFrame(frame_descarga, text="⚙️ Opciones de Descarga", padding=10)
        opciones_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Calidad
        calidad_frame = tk.Frame(opciones_frame)
        calidad_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(calidad_frame, text="🎯 Calidad:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        
        calidades = [
            ("Mejor disponible", "best"),
            ("720p", "best[height<=720]"),
            ("480p", "best[height<=480]"),
            ("360p", "best[height<=360]"),
            ("Peor calidad", "worst")
        ]
        
        calidad_combo = ttk.Combobox(calidad_frame, textvariable=self.calidad_var, 
                                   values=[c[0] for c in calidades], state="readonly")
        calidad_combo.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        calidad_combo.set("Mejor disponible")
        
        # Mapear valores para uso interno
        self.calidad_map = {c[0]: c[1] for c in calidades}
        
        # Checkboxes
        checks_frame = tk.Frame(opciones_frame)
        checks_frame.pack(fill=tk.X, pady=10)
        
        solo_audio_check = tk.Checkbutton(checks_frame, text="🎵 Solo Audio (MP3)", 
                                        variable=self.solo_audio_var, font=("Arial", 9))
        solo_audio_check.pack(side=tk.LEFT, padx=(0, 20))
        
        subtitulos_check = tk.Checkbutton(checks_frame, text="📝 Incluir Subtítulos", 
                                        variable=self.subtitulos_var, font=("Arial", 9))
        subtitulos_check.pack(side=tk.LEFT)
        
        # Directorio de descarga
        directorio_frame = ttk.LabelFrame(frame_descarga, text="📁 Directorio de Descarga", padding=10)
        directorio_frame.pack(fill=tk.X, padx=20, pady=5)
        
        dir_input_frame = tk.Frame(directorio_frame)
        dir_input_frame.pack(fill=tk.X)
        
        dir_entry = tk.Entry(dir_input_frame, textvariable=self.directorio_descarga, 
                           font=("Arial", 10))
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        btn_explorar = ttk.Button(dir_input_frame, text="📁 Explorar", 
                                command=self.seleccionar_directorio)
        btn_explorar.pack(side=tk.RIGHT)
        
        # Información del video
        self.info_frame = ttk.LabelFrame(frame_descarga, text="📺 Información del Video", padding=10)
        self.info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.info_text = scrolledtext.ScrolledText(self.info_frame, height=4, 
                                                  font=("Arial", 9), state=tk.DISABLED)
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Progreso
        progreso_frame = ttk.LabelFrame(frame_descarga, text="📊 Progreso", padding=10)
        progreso_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.progreso_label = tk.Label(progreso_frame, textvariable=self.progreso_var, 
                                      font=("Arial", 9), wraplength=700)
        self.progreso_label.pack(fill=tk.X, pady=5)
        
        self.progress_bar = ttk.Progressbar(progreso_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Botones principales
        botones_frame = tk.Frame(frame_descarga)
        botones_frame.pack(fill=tk.X, padx=20, pady=20)
        
        self.btn_descargar = tk.Button(botones_frame, text="📥 Descargar Video", 
                                      command=self.iniciar_descarga, font=("Arial", 12, "bold"),
                                      bg="#4CAF50", fg="white", relief="raised", bd=2)
        self.btn_descargar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.btn_cancelar = tk.Button(botones_frame, text="❌ Cancelar", 
                                     command=self.cancelar_descarga, font=("Arial", 12, "bold"),
                                     bg="#f44336", fg="white", relief="raised", bd=2, state=tk.DISABLED)
        self.btn_cancelar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
    
    def crear_pestaña_clips(self, notebook):
        """Crea la pestaña para crear clips de video"""
        
        frame_clips = ttk.Frame(notebook)
        notebook.add(frame_clips, text="✂️ Crear Clips")
        
        # Título
        titulo_clips = tk.Label(frame_clips, text="✂️ Crear Clips de YouTube", 
                               font=("Arial", 16, "bold"), fg="#1f4e79")
        titulo_clips.pack(pady=(10, 20))
        
        # URL Input para clips
        url_clip_frame = ttk.LabelFrame(frame_clips, text="📎 URL del Video para Clip", padding=10)
        url_clip_frame.pack(fill=tk.X, padx=20, pady=5)
        
        url_clip_entry = tk.Entry(url_clip_frame, textvariable=self.url_clip_var, font=("Arial", 10))
        url_clip_entry.pack(fill=tk.X, pady=5)
        url_clip_entry.bind('<Return>', lambda e: self.obtener_info_video_clip())
        
        # Botones para obtener información y descargar video completo
        botones_clip_frame = tk.Frame(url_clip_frame)
        botones_clip_frame.pack(fill=tk.X, pady=5)
        
        btn_info_clip = ttk.Button(botones_clip_frame, text="🔍 Obtener Info", 
                                  command=self.obtener_info_video_clip)
        btn_info_clip.pack(side=tk.LEFT, padx=(0, 5))
        
        self.btn_descargar_temp = ttk.Button(botones_clip_frame, text="📥 Descargar Video Completo", 
                                            command=self.descargar_video_temporal, state=tk.DISABLED)
        self.btn_descargar_temp.pack(side=tk.LEFT)
        
        # Información del video para clip
        self.info_clip_frame = ttk.LabelFrame(frame_clips, text="📺 Información del Video", padding=10)
        self.info_clip_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.info_clip_text = scrolledtext.ScrolledText(self.info_clip_frame, height=3, 
                                                       font=("Arial", 9), state=tk.DISABLED)
        self.info_clip_text.pack(fill=tk.BOTH, expand=True)
        
        # Configuración del clip
        clip_config_frame = ttk.LabelFrame(frame_clips, text="✂️ Configuración del Clip", padding=10)
        clip_config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Tiempo de inicio y fin
        tiempo_frame = tk.Frame(clip_config_frame)
        tiempo_frame.pack(fill=tk.X, pady=5)
        
        # Tiempo de inicio
        tk.Label(tiempo_frame, text="🕐 Inicio:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        inicio_entry = tk.Entry(tiempo_frame, textvariable=self.inicio_clip_var, 
                               font=("Arial", 10), width=15)
        inicio_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        # Tiempo de fin
        tk.Label(tiempo_frame, text="🕐 Fin:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        fin_entry = tk.Entry(tiempo_frame, textvariable=self.fin_clip_var, 
                            font=("Arial", 10), width=15)
        fin_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        # Ayuda de formato
        tk.Label(tiempo_frame, text="(Formato: HH:MM:SS)", 
                font=("Arial", 8), fg="#666").pack(side=tk.LEFT, padx=(10, 0))
        
        # Nombre del archivo de salida
        nombre_frame = tk.Frame(clip_config_frame)
        nombre_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(nombre_frame, text="📝 Nombre del clip:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        nombre_entry = tk.Entry(nombre_frame, textvariable=self.nombre_clip_var, 
                               font=("Arial", 10))
        nombre_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Botones de tiempo rápido
        botones_rapidos_frame = ttk.LabelFrame(frame_clips, text="⚡ Accesos Rápidos", padding=10)
        botones_rapidos_frame.pack(fill=tk.X, padx=20, pady=5)
        
        rapidos_frame = tk.Frame(botones_rapidos_frame)
        rapidos_frame.pack(fill=tk.X)
        
        tk.Button(rapidos_frame, text="📺 Primeros 30s", 
                 command=lambda: self.set_tiempo_rapido("00:00:00", "00:00:30"),
                 font=("Arial", 9), bg="#e3f2fd").pack(side=tk.LEFT, padx=2)
        
        tk.Button(rapidos_frame, text="🎵 1 minuto", 
                 command=lambda: self.set_tiempo_rapido("00:00:00", "00:01:00"),
                 font=("Arial", 9), bg="#e8f5e8").pack(side=tk.LEFT, padx=2)
        
        tk.Button(rapidos_frame, text="📹 2 minutos", 
                 command=lambda: self.set_tiempo_rapido("00:00:00", "00:02:00"),
                 font=("Arial", 9), bg="#fff3e0").pack(side=tk.LEFT, padx=2)
        
        tk.Button(rapidos_frame, text="🎬 5 minutos", 
                 command=lambda: self.set_tiempo_rapido("00:00:00", "00:05:00"),
                 font=("Arial", 9), bg="#fce4ec").pack(side=tk.LEFT, padx=2)
        
        # Progreso para clips
        progreso_clip_frame = ttk.LabelFrame(frame_clips, text="📊 Progreso del Clip", padding=10)
        progreso_clip_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.progreso_clip_label = tk.Label(progreso_clip_frame, textvariable=self.progreso_clip_var, 
                                           font=("Arial", 9), wraplength=700)
        self.progreso_clip_label.pack(fill=tk.X, pady=5)
        
        self.progress_bar_clip = ttk.Progressbar(progreso_clip_frame, mode='indeterminate')
        self.progress_bar_clip.pack(fill=tk.X, pady=5)
        
        # Información sobre los métodos de creación
        info_metodos_frame = ttk.LabelFrame(frame_clips, text="ℹ️ Métodos de Creación", padding=10)
        info_metodos_frame.pack(fill=tk.X, padx=20, pady=5)
        
        info_text = ("• ✂️ Crear Clip: Usa un video ya descargado (método rápido)\n"
                    "• 🎬 Descargar y Crear Clip: Descarga automáticamente y crea el clip (todo en uno)")
        info_label = tk.Label(info_metodos_frame, text=info_text, font=("Arial", 9), 
                            justify=tk.LEFT, wraplength=700, bg="#f0f0f0")
        info_label.pack(fill=tk.X, pady=5)
        
        # Botones principales para clips
        botones_clip_principales = tk.Frame(frame_clips)
        botones_clip_principales.pack(fill=tk.X, padx=20, pady=20)
        
        # Primer botón: Crear clip (método original - requiere descarga previa)
        self.btn_crear_clip_original = tk.Button(botones_clip_principales, text="✂️ Crear Clip", 
                                                command=self.crear_clip_original, font=("Arial", 10, "bold"),
                                                bg="#4CAF50", fg="white", relief="raised", bd=2, state=tk.DISABLED)
        self.btn_crear_clip_original.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))
        
        # Segundo botón: Descargar y crear clip automáticamente
        self.btn_crear_clip_auto = tk.Button(botones_clip_principales, text="🎬 Descargar y Crear Clip", 
                                           command=self.crear_clip_automatico, font=("Arial", 10, "bold"),
                                           bg="#FF9800", fg="white", relief="raised", bd=2, state=tk.DISABLED)
        self.btn_crear_clip_auto.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(3, 3))
        
        # Botón de limpiar temporales
        self.btn_limpiar_temp = tk.Button(botones_clip_principales, text="🗑️ Limpiar", 
                                         command=self.limpiar_archivos_temporales, font=("Arial", 10, "bold"),
                                         bg="#9E9E9E", fg="white", relief="raised", bd=2)
        self.btn_limpiar_temp.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(3, 0))
    
    def crear_pestaña_archivos(self, notebook):
        """Crea la pestaña para procesar archivos de video locales"""
        
        frame_archivos = ttk.Frame(notebook)
        notebook.add(frame_archivos, text="📁 Procesar Archivos")
        
        # Título
        titulo_archivos = tk.Label(frame_archivos, text="📁 Procesar Videos Locales", 
                                 font=("Arial", 16, "bold"), fg="#1f4e79")
        titulo_archivos.pack(pady=(10, 20))
        
        # Selección de archivo
        archivo_frame = ttk.LabelFrame(frame_archivos, text="📎 Seleccionar Video Local", padding=10)
        archivo_frame.pack(fill=tk.X, padx=20, pady=5)
        
        # Frame para entrada de archivo
        archivo_input_frame = tk.Frame(archivo_frame)
        archivo_input_frame.pack(fill=tk.X, pady=5)
        
        archivo_entry = tk.Entry(archivo_input_frame, textvariable=self.archivo_local_var, 
                               font=("Arial", 10), state="readonly")
        archivo_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        btn_seleccionar = ttk.Button(archivo_input_frame, text="📁 Seleccionar Archivo", 
                                   command=self.seleccionar_archivo_local)
        btn_seleccionar.pack(side=tk.RIGHT)
        
        # Botón para obtener información del archivo
        btn_info_archivo = ttk.Button(archivo_frame, text="🔍 Obtener Info del Archivo", 
                                    command=self.obtener_info_archivo_local, state=tk.DISABLED)
        btn_info_archivo.pack(pady=5)
        self.btn_info_archivo = btn_info_archivo
        
        # Información del archivo
        self.info_archivo_frame = ttk.LabelFrame(frame_archivos, text="📺 Información del Video", padding=10)
        self.info_archivo_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.info_archivo_text = scrolledtext.ScrolledText(self.info_archivo_frame, height=3, 
                                                         font=("Arial", 9), state=tk.DISABLED)
        self.info_archivo_text.pack(fill=tk.BOTH, expand=True)
        
        # Configuración del clip
        clip_archivo_config_frame = ttk.LabelFrame(frame_archivos, text="✂️ Configuración del Clip", padding=10)
        clip_archivo_config_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Tiempo de inicio y fin
        tiempo_archivo_frame = tk.Frame(clip_archivo_config_frame)
        tiempo_archivo_frame.pack(fill=tk.X, pady=5)
        
        # Tiempo de inicio
        tk.Label(tiempo_archivo_frame, text="🕐 Inicio:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        inicio_archivo_entry = tk.Entry(tiempo_archivo_frame, textvariable=self.inicio_archivo_var, 
                                       font=("Arial", 10), width=15)
        inicio_archivo_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        # Tiempo de fin
        tk.Label(tiempo_archivo_frame, text="🕐 Fin:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        fin_archivo_entry = tk.Entry(tiempo_archivo_frame, textvariable=self.fin_archivo_var, 
                                   font=("Arial", 10), width=15)
        fin_archivo_entry.pack(side=tk.LEFT, padx=(5, 15))
        
        # Ayuda de formato
        tk.Label(tiempo_archivo_frame, text="(Formato: HH:MM:SS)", 
                font=("Arial", 8), fg="#666").pack(side=tk.LEFT, padx=(10, 0))
        
        # Nombre del archivo de salida
        nombre_archivo_frame = tk.Frame(clip_archivo_config_frame)
        nombre_archivo_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(nombre_archivo_frame, text="📝 Nombre del clip:", font=("Arial", 9, "bold")).pack(side=tk.LEFT)
        nombre_archivo_entry = tk.Entry(nombre_archivo_frame, textvariable=self.nombre_archivo_clip_var, 
                                       font=("Arial", 10))
        nombre_archivo_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
        
        # Botones de tiempo rápido
        botones_archivo_rapidos_frame = ttk.LabelFrame(frame_archivos, text="⚡ Accesos Rápidos", padding=10)
        botones_archivo_rapidos_frame.pack(fill=tk.X, padx=20, pady=5)
        
        rapidos_archivo_frame = tk.Frame(botones_archivo_rapidos_frame)
        rapidos_archivo_frame.pack(fill=tk.X)
        
        tk.Button(rapidos_archivo_frame, text="📺 Primeros 30s", 
                 command=lambda: self.set_tiempo_rapido_archivo("00:00:00", "00:00:30"),
                 font=("Arial", 9), bg="#e3f2fd").pack(side=tk.LEFT, padx=2)
        
        tk.Button(rapidos_archivo_frame, text="🎵 1 minuto", 
                 command=lambda: self.set_tiempo_rapido_archivo("00:00:00", "00:01:00"),
                 font=("Arial", 9), bg="#e8f5e8").pack(side=tk.LEFT, padx=2)
        
        tk.Button(rapidos_archivo_frame, text="📹 2 minutos", 
                 command=lambda: self.set_tiempo_rapido_archivo("00:00:00", "00:02:00"),
                 font=("Arial", 9), bg="#fff3e0").pack(side=tk.LEFT, padx=2)
        
        tk.Button(rapidos_archivo_frame, text="🎬 5 minutos", 
                 command=lambda: self.set_tiempo_rapido_archivo("00:00:00", "00:05:00"),
                 font=("Arial", 9), bg="#fce4ec").pack(side=tk.LEFT, padx=2)
        
        # Progreso para archivos
        progreso_archivo_frame = ttk.LabelFrame(frame_archivos, text="📊 Progreso del Procesamiento", padding=10)
        progreso_archivo_frame.pack(fill=tk.X, padx=20, pady=5)
        
        self.progreso_archivo_label = tk.Label(progreso_archivo_frame, textvariable=self.progreso_archivo_var, 
                                             font=("Arial", 9), wraplength=700)
        self.progreso_archivo_label.pack(fill=tk.X, pady=5)
        
        self.progress_bar_archivo = ttk.Progressbar(progreso_archivo_frame, mode='indeterminate')
        self.progress_bar_archivo.pack(fill=tk.X, pady=5)
        
        # Información sobre los métodos de procesamiento
        info_metodos_archivo_frame = ttk.LabelFrame(frame_archivos, text="ℹ️ Métodos de Procesamiento", padding=10)
        info_metodos_archivo_frame.pack(fill=tk.X, padx=20, pady=5)
        
        info_archivo_text = ("• ✂️ Crear Clip: Procesa el archivo directamente (rápido)\n"
                           "• 🎞️ Convertir y Crear Clip: Convierte formato si es necesario y crea el clip")
        info_archivo_label = tk.Label(info_metodos_archivo_frame, text=info_archivo_text, font=("Arial", 9), 
                                    justify=tk.LEFT, wraplength=700, bg="#f0f0f0")
        info_archivo_label.pack(fill=tk.X, pady=5)
        
        # Botones principales para archivos
        botones_archivo_principales = tk.Frame(frame_archivos)
        botones_archivo_principales.pack(fill=tk.X, padx=20, pady=20)
        
        # Primer botón: Crear clip directo
        self.btn_crear_clip_archivo = tk.Button(botones_archivo_principales, text="✂️ Crear Clip", 
                                              command=self.crear_clip_archivo, font=("Arial", 10, "bold"),
                                              bg="#4CAF50", fg="white", relief="raised", bd=2, state=tk.DISABLED)
        self.btn_crear_clip_archivo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 3))
        
        # Segundo botón: Convertir y crear clip
        self.btn_convertir_clip_archivo = tk.Button(botones_archivo_principales, text="🎞️ Convertir y Crear Clip", 
                                                  command=self.convertir_y_crear_clip_archivo, font=("Arial", 9, "bold"),
                                                  bg="#FF9800", fg="white", relief="raised", bd=2, state=tk.DISABLED)
        self.btn_convertir_clip_archivo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(3, 3))
        
        # Botón de limpiar
        self.btn_limpiar_archivo = tk.Button(botones_archivo_principales, text="🗑️ Limpiar", 
                                           command=self.limpiar_seleccion_archivo, font=("Arial", 10, "bold"),
                                           bg="#9E9E9E", fg="white", relief="raised", bd=2)
        self.btn_limpiar_archivo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(3, 0))
    
    def crear_pestaña_info(self, notebook):
        """Crea la pestaña de información detallada"""
        
        frame_info = ttk.Frame(notebook)
        notebook.add(frame_info, text="ℹ️ Información")
        
        # Área de texto para información detallada
        self.info_detallada = scrolledtext.ScrolledText(frame_info, font=("Consolas", 9))
        self.info_detallada.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Botones
        botones_info_frame = tk.Frame(frame_info)
        botones_info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        btn_limpiar_info = ttk.Button(botones_info_frame, text="🗑️ Limpiar", 
                                    command=self.limpiar_info)
        btn_limpiar_info.pack(side=tk.LEFT, padx=5)
        
        btn_guardar_info = ttk.Button(botones_info_frame, text="💾 Guardar Info", 
                                    command=self.guardar_info)
        btn_guardar_info.pack(side=tk.LEFT, padx=5)
        
    def crear_pestaña_config(self, notebook):
        """Crea la pestaña de configuración"""
        
        frame_config = ttk.Frame(notebook)
        notebook.add(frame_config, text="⚙️ Configuración")
        
        # Información de la aplicación
        info_app = ttk.LabelFrame(frame_config, text="📱 Información de la Aplicación", padding=10)
        info_app.pack(fill=tk.X, padx=20, pady=10)
        
        info_texto = """
🎬 YouTube Downloader GUI v1.0
📅 Creado en julio 2025
⚡ Basado en yt-dlp
🐍 Python + tkinter

Características:
• Descarga videos en múltiples calidades
• Extracción de audio a MP3
• Descarga de subtítulos
• Interfaz amigable e intuitiva
        """
        
        tk.Label(info_app, text=info_texto.strip(), font=("Arial", 9), justify=tk.LEFT).pack(anchor=tk.W)
        
        # Enlaces útiles
        enlaces_frame = ttk.LabelFrame(frame_config, text="🔗 Enlaces Útiles", padding=10)
        enlaces_frame.pack(fill=tk.X, padx=20, pady=10)
        
        btn_youtube = tk.Button(enlaces_frame, text="📺 Ir a YouTube", 
                               command=lambda: webbrowser.open("https://youtube.com"),
                               bg="#FF0000", fg="white", font=("Arial", 9, "bold"))
        btn_youtube.pack(fill=tk.X, pady=2)
        
        btn_yt_dlp = tk.Button(enlaces_frame, text="📖 Documentación yt-dlp", 
                              command=lambda: webbrowser.open("https://github.com/yt-dlp/yt-dlp"),
                              bg="#333333", fg="white", font=("Arial", 9, "bold"))
        btn_yt_dlp.pack(fill=tk.X, pady=2)
        
        # Directorio de descargas
        dir_frame = ttk.LabelFrame(frame_config, text="📁 Gestión de Archivos", padding=10)
        dir_frame.pack(fill=tk.X, padx=20, pady=10)
        
        btn_abrir_dir = ttk.Button(dir_frame, text="📂 Abrir Directorio de Descargas", 
                                 command=self.abrir_directorio_descargas)
        btn_abrir_dir.pack(fill=tk.X, pady=2)
        
        btn_limpiar_dir = ttk.Button(dir_frame, text="🗑️ Limpiar Directorio", 
                                   command=self.limpiar_directorio)
        btn_limpiar_dir.pack(fill=tk.X, pady=2)
    
    def seleccionar_directorio(self):
        """Permite seleccionar un directorio para las descargas"""
        directorio = filedialog.askdirectory(initialdir=self.directorio_descarga.get())
        if directorio:
            self.directorio_descarga.set(directorio)
    
    def obtener_info_video(self):
        """Obtiene información del video en un hilo separado"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("⚠️ Advertencia", "Por favor ingresa una URL válida")
            return
        
        # Ejecutar en hilo separado para no bloquear la UI
        threading.Thread(target=self._obtener_info_video_thread, args=(url,), daemon=True).start()
    
    def _obtener_info_video_thread(self, url):
        """Hilo para obtener información del video"""
        self.progreso_var.set("🔍 Obteniendo información del video...")
        self.progress_bar.start()
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                # Actualizar UI en el hilo principal
                self.root.after(0, self._mostrar_info_video, info)
                
        except Exception as e:
            error_msg = f"❌ Error obteniendo información: {str(e)}"
            self.root.after(0, lambda: self.progreso_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            self.root.after(0, self.progress_bar.stop)
    
    def _mostrar_info_video(self, info):
        """Muestra la información del video en la interfaz"""
        titulo = info.get('title', 'Sin título')
        duracion = self._formatear_duracion(info.get('duration', 0))
        uploader = info.get('uploader', 'Desconocido')
        descripcion = info.get('description', '')[:300] + '...' if info.get('description') else 'Sin descripción'
        fecha_subida = info.get('upload_date', 'Desconocida')
        formatos = len(info.get('formats', []))
        
        # Actualizar texto en el frame de información básica
        info_basica = f"""
📺 Título: {titulo}
👤 Canal: {uploader}
⏱️ Duración: {duracion}
📅 Fecha de subida: {fecha_subida}
🎞️ Formatos disponibles: {formatos}
📝 Descripción: {descripcion}
        """.strip()
        
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info_basica)
        self.info_text.config(state=tk.DISABLED)
        
        # Información detallada en la otra pestaña
        info_completa = json.dumps(info, indent=2, ensure_ascii=False)
        self.info_detallada.delete(1.0, tk.END)
        self.info_detallada.insert(1.0, f"Información completa del video:\n\n{info_completa}")
        
        self.progreso_var.set("✅ Información obtenida correctamente")
    
    def _formatear_duracion(self, segundos):
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
    
    def iniciar_descarga(self):
        """Inicia el proceso de descarga"""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("⚠️ Advertencia", "Por favor ingresa una URL válida")
            return
        
        if self.descarga_activa:
            messagebox.showinfo("ℹ️ Información", "Ya hay una descarga en progreso")
            return
        
        # Cambiar estado de botones
        self.btn_descargar.config(state=tk.DISABLED)
        self.btn_cancelar.config(state=tk.NORMAL)
        self.descarga_activa = True
        
        # Iniciar descarga en hilo separado
        opciones = {
            'calidad': self.calidad_map.get(self.calidad_var.get(), 'best'),
            'solo_audio': self.solo_audio_var.get(),
            'subtitulos': self.subtitulos_var.get(),
            'directorio': self.directorio_descarga.get()
        }
        
        threading.Thread(target=self._descargar_video_thread, args=(url, opciones), daemon=True).start()
    
    def _descargar_video_thread(self, url, opciones):
        """Hilo para descargar el video"""
        try:
            # Crear directorio si no existe
            Path(opciones['directorio']).mkdir(exist_ok=True)
            
            # Configuración de yt-dlp
            ydl_opts = {
                'outtmpl': f"{opciones['directorio']}/%(title)s.%(ext)s",
                'format': opciones['calidad'],
                'noplaylist': True,
            }
            
            # Opciones adicionales
            if opciones['solo_audio']:
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                })
            
            if opciones['subtitulos']:
                ydl_opts.update({
                    'writesubtitles': True,
                    'writeautomaticsub': True,
                    'subtitleslangs': ['es', 'en'],
                })
            
            # Hook para progreso
            def progreso_hook(d):
                if d['status'] == 'downloading':
                    progreso = f"📥 Descargando... {d.get('_percent_str', 'N/A')}"
                    self.root.after(0, lambda: self.progreso_var.set(progreso))
                elif d['status'] == 'finished':
                    self.root.after(0, lambda: self.progreso_var.set(f"✅ Descarga completada: {d['filename']}"))
            
            ydl_opts['progress_hooks'] = [progreso_hook]
            
            # Iniciar descarga
            self.root.after(0, lambda: self.progreso_var.set("🚀 Iniciando descarga..."))
            self.root.after(0, self.progress_bar.start)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Éxito
            self.root.after(0, lambda: messagebox.showinfo("✅ Éxito", "¡Video descargado exitosamente!"))
            
        except Exception as e:
            error_msg = f"❌ Error durante la descarga: {str(e)}"
            self.root.after(0, lambda: self.progreso_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            # Restaurar estado de botones
            self.root.after(0, self._finalizar_descarga)
    
    def _finalizar_descarga(self):
        """Finaliza el proceso de descarga y restaura la UI"""
        self.btn_descargar.config(state=tk.NORMAL)
        self.btn_cancelar.config(state=tk.DISABLED)
        self.descarga_activa = False
        self.progress_bar.stop()
    
    def cancelar_descarga(self):
        """Cancela la descarga actual"""
        if messagebox.askyesno("⚠️ Confirmar", "¿Deseas cancelar la descarga actual?"):
            # Nota: yt-dlp no tiene una forma fácil de cancelar, pero podemos simular
            self.progreso_var.set("❌ Descarga cancelada por el usuario")
            self._finalizar_descarga()
    
    def limpiar_info(self):
        """Limpia la información detallada"""
        self.info_detallada.delete(1.0, tk.END)
    
    def guardar_info(self):
        """Guarda la información del video en un archivo"""
        contenido = self.info_detallada.get(1.0, tk.END).strip()
        if not contenido:
            messagebox.showwarning("⚠️ Advertencia", "No hay información para guardar")
            return
        
        archivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            try:
                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write(contenido)
                messagebox.showinfo("✅ Éxito", f"Información guardada en: {archivo}")
            except Exception as e:
                messagebox.showerror("Error", f"Error guardando archivo: {str(e)}")
    
    def abrir_directorio_descargas(self):
        """Abre el directorio de descargas en el explorador"""
        directorio = self.directorio_descarga.get()
        Path(directorio).mkdir(exist_ok=True)
        
        try:
            os.startfile(directorio)  # Windows
        except:
            try:
                os.system(f'explorer "{directorio}"')  # Windows alternativo
            except:
                messagebox.showinfo("ℹ️ Información", f"Directorio: {directorio}")
    
    def limpiar_directorio(self):
        """Limpia el directorio de descargas"""
        if messagebox.askyesno("⚠️ Confirmar", "¿Deseas eliminar todos los archivos del directorio de descargas?"):
            try:
                directorio = Path(self.directorio_descarga.get())
                if directorio.exists():
                    archivos_eliminados = 0
                    for archivo in directorio.glob("*"):
                        if archivo.is_file():
                            archivo.unlink()
                            archivos_eliminados += 1
                    
                    messagebox.showinfo("✅ Éxito", f"Se eliminaron {archivos_eliminados} archivos")
                else:
                    messagebox.showinfo("ℹ️ Información", "El directorio no existe")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error limpiando directorio: {str(e)}")
    
    # ==================== FUNCIONES PARA CLIPS ====================
    
    def obtener_info_video_clip(self):
        """Obtiene información del video para clips"""
        url = self.url_clip_var.get().strip()
        if not url:
            messagebox.showwarning("⚠️ Advertencia", "Por favor ingresa una URL válida")
            return
        
        threading.Thread(target=self._obtener_info_video_clip_thread, args=(url,), daemon=True).start()
    
    def _obtener_info_video_clip_thread(self, url):
        """Hilo para obtener información del video para clips"""
        self.progreso_clip_var.set("🔍 Obteniendo información del video...")
        self.progress_bar_clip.start()
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                self.video_info_clip = info
                
                # Actualizar UI en el hilo principal
                self.root.after(0, self._mostrar_info_video_clip, info)
                
        except Exception as e:
            error_str = str(e)
            
            # Detectar tipos específicos de errores
            if "Only images are available" in error_str or "format is not available" in error_str.lower():
                error_msg = ("❌ Video protegido o restringido\n\n"
                           "Este video no puede ser procesado porque:\n"
                           "• YouTube lo tiene protegido o restringido\n"
                           "• Solo hay imágenes disponibles\n"
                           "• El contenido es de acceso limitado")
            elif "nsig extraction failed" in error_str.lower():
                error_msg = ("❌ Error de extracción de firma\n\n"
                           "Intenta actualizar yt-dlp:\n"
                           "pip install --upgrade yt-dlp")
            elif "HTTP Error 404" in error_str or "Video not found" in error_str:
                error_msg = "❌ Video no encontrado. Verifica que la URL sea correcta."
            else:
                error_msg = f"❌ Error obteniendo información: {error_str}"
            
            self.root.after(0, lambda: self.progreso_clip_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            self.root.after(0, self.progress_bar_clip.stop)
    
    def _mostrar_info_video_clip(self, info):
        """Muestra la información del video para clips"""
        titulo = info.get('title', 'Sin título')
        duracion = self._formatear_duracion(info.get('duration', 0))
        uploader = info.get('uploader', 'Desconocido')
        
        # Actualizar texto en el frame de información de clips
        info_basica = f"📺 {titulo}\n👤 Canal: {uploader} | ⏱️ Duración: {duracion}"
        
        self.info_clip_text.config(state=tk.NORMAL)
        self.info_clip_text.delete(1.0, tk.END)
        self.info_clip_text.insert(1.0, info_basica)
        self.info_clip_text.config(state=tk.DISABLED)
        
        # Habilitar botón de descarga temporal (por compatibilidad)
        self.btn_descargar_temp.config(state=tk.NORMAL)
        
        # ✨ Habilitar ambos botones de crear clip
        self.btn_crear_clip_auto.config(state=tk.NORMAL)  # Botón automático
        # El botón original se habilitará solo después de descargar el video temporal
        
        # Establecer tiempo de fin por defecto basado en la duración
        if info.get('duration'):
            duracion_formateada = self._segundos_a_tiempo(min(300, info.get('duration')))  # Max 5 minutos
            self.fin_clip_var.set(duracion_formateada)
        
        # Establecer nombre por defecto basado en el título
        nombre_limpio = "".join(c for c in titulo if c.isalnum() or c in (' ', '-', '_')).rstrip()[:30]
        self.nombre_clip_var.set(f"clip_{nombre_limpio}")
        
        self.progreso_clip_var.set("✅ Información obtenida. Elige tu método de creación de clips:")
    
    def _segundos_a_tiempo(self, segundos):
        """Convierte segundos a formato HH:MM:SS"""
        horas = segundos // 3600
        minutos = (segundos % 3600) // 60
        segundos = segundos % 60
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    
    def descargar_video_temporal(self):
        """Descarga el video completo temporalmente para crear clips"""
        if not self.video_info_clip:
            messagebox.showwarning("⚠️ Advertencia", "Primero obtén la información del video")
            return
        
        url = self.url_clip_var.get().strip()
        threading.Thread(target=self._descargar_video_temporal_thread, args=(url,), daemon=True).start()
    
    def _descargar_video_temporal_thread(self, url):
        """Hilo para descargar video temporal"""
        try:
            # Crear directorio temporal
            temp_dir = Path("temp_clips")
            temp_dir.mkdir(exist_ok=True)
            
            # Configuración para descarga temporal
            ydl_opts = {
                'outtmpl': f'{temp_dir}/%(title)s.%(ext)s',
                'format': 'bestvideo[height<=720]/best[height<=720]/bestvideo/best',
                'noplaylist': True,
                'quiet': False,
                'no_warnings': False
            }
            
            self.root.after(0, lambda: self.progreso_clip_var.set("📥 Descargando video completo..."))
            self.root.after(0, self.progress_bar_clip.start)
            self.root.after(0, lambda: self.btn_descargar_temp.config(state=tk.DISABLED))
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Encontrar el archivo descargado
            archivos = list(temp_dir.glob("*"))
            if archivos:
                self.video_temp_path = str(archivos[0])
                # Habilitar el botón del método original ahora que tenemos el video descargado
                self.root.after(0, lambda: self.btn_crear_clip_original.config(state=tk.NORMAL))
                self.root.after(0, lambda: self.progreso_clip_var.set("✅ Video descargado. Puedes usar ambos métodos de creación."))
            else:
                raise Exception("No se encontró el archivo descargado")
                
        except Exception as e:
            error_str = str(e)
            
            # Detectar tipos específicos de errores
            if "Only images are available" in error_str or "format is not available" in error_str.lower():
                error_msg = ("❌ Video protegido o restringido\n\n"
                           "Este video no puede ser descargado porque:\n"
                           "• YouTube lo tiene protegido o restringido\n"
                           "• Solo hay imágenes disponibles para descarga\n"
                           "• El contenido puede ser de acceso limitado\n\n"
                           "Intenta con otro video de YouTube.")
            elif "nsig extraction failed" in error_str.lower():
                error_msg = ("❌ Error de extracción de firma\n\n"
                           "Intenta actualizar yt-dlp:\n"
                           "pip install --upgrade yt-dlp")
            else:
                error_msg = f"❌ Error descargando video: {error_str}"
            
            self.root.after(0, lambda: self.progreso_clip_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            self.root.after(0, self.progress_bar_clip.stop)
            self.root.after(0, lambda: self.btn_descargar_temp.config(state=tk.NORMAL))
    
    def set_tiempo_rapido(self, inicio, fin):
        """Establece tiempos rápidos predefinidos"""
        self.inicio_clip_var.set(inicio)
        self.fin_clip_var.set(fin)
    
    def _tiempo_a_segundos(self, tiempo_str):
        """Convierte tiempo HH:MM:SS a segundos"""
        try:
            partes = tiempo_str.split(':')
            if len(partes) == 3:
                h, m, s = map(int, partes)
                return h * 3600 + m * 60 + s
            elif len(partes) == 2:
                m, s = map(int, partes)
                return m * 60 + s
            else:
                return int(partes[0])
        except:
            return 0
    
    def crear_clip_automatico(self):
        """Crea el clip descargando el video automáticamente si es necesario"""
        print("🎬 DEBUG: Iniciando crear_clip_automatico()")
        
        # Validar que tenemos la información del video
        if not self.video_info_clip:
            print("❌ DEBUG: No hay información del video")
            messagebox.showwarning("⚠️ Advertencia", "Primero obtén la información del video")
            return
        
        # Validar campos de tiempo y nombre
        inicio = self.inicio_clip_var.get().strip()
        fin = self.fin_clip_var.get().strip()
        nombre = self.nombre_clip_var.get().strip()
        
        print(f"📋 DEBUG: Datos - Inicio: {inicio}, Fin: {fin}, Nombre: {nombre}")
        
        if not all([inicio, fin, nombre]):
            print("❌ DEBUG: Campos incompletos")
            messagebox.showwarning("⚠️ Advertencia", "Completa todos los campos")
            return
        
        # Convertir tiempos a segundos para validación
        inicio_seg = self._tiempo_a_segundos(inicio)
        fin_seg = self._tiempo_a_segundos(fin)
        
        print(f"⏱️ DEBUG: Tiempos convertidos - Inicio: {inicio_seg}s, Fin: {fin_seg}s")
        
        if inicio_seg >= fin_seg:
            print("❌ DEBUG: Tiempo de inicio >= tiempo de fin")
            messagebox.showwarning("⚠️ Advertencia", "El tiempo de inicio debe ser menor al tiempo de fin")
            return
        
        print("✅ DEBUG: Validaciones pasadas, iniciando proceso automático...")
        threading.Thread(target=self._crear_clip_automatico_thread, args=(inicio, fin, nombre), daemon=True).start()
    
    def crear_clip_original(self):
        """Crea el clip usando ffmpeg (método original - requiere descarga previa)"""
        print("✂️ DEBUG: Iniciando crear_clip_original()")
        
        if not self.video_temp_path or not os.path.exists(self.video_temp_path):
            print("❌ DEBUG: Video temporal no encontrado")
            messagebox.showwarning("⚠️ Advertencia", "Primero descarga el video completo usando el botón 'Descargar Video Temporal'")
            return
        
        # Validar tiempos
        inicio = self.inicio_clip_var.get().strip()
        fin = self.fin_clip_var.get().strip()
        nombre = self.nombre_clip_var.get().strip()
        
        print(f"📋 DEBUG: Datos - Inicio: {inicio}, Fin: {fin}, Nombre: {nombre}")
        
        if not all([inicio, fin, nombre]):
            print("❌ DEBUG: Campos incompletos")
            messagebox.showwarning("⚠️ Advertencia", "Completa todos los campos")
            return
        
        # Convertir tiempos a segundos para validación
        inicio_seg = self._tiempo_a_segundos(inicio)
        fin_seg = self._tiempo_a_segundos(fin)
        
        print(f"⏱️ DEBUG: Tiempos convertidos - Inicio: {inicio_seg}s, Fin: {fin_seg}s")
        
        if inicio_seg >= fin_seg:
            print("❌ DEBUG: Tiempo de inicio >= tiempo de fin")
            messagebox.showwarning("⚠️ Advertencia", "El tiempo de inicio debe ser menor al tiempo de fin")
            return
        
        print("✅ DEBUG: Validaciones pasadas, iniciando hilo...")
        threading.Thread(target=self._crear_clip_original_thread, args=(inicio, fin, nombre), daemon=True).start()
    
    def _crear_clip_original_thread(self, inicio, fin, nombre):
        """Hilo para crear el clip usando video ya descargado (método original)"""
        try:
            print("✂️ DEBUG: Iniciando hilo de creación de clip original")
            self.root.after(0, lambda: self.progreso_clip_var.set("✂️ Creando clip desde video descargado..."))
            self.root.after(0, self.progress_bar_clip.start)
            self.root.after(0, lambda: self.btn_crear_clip_original.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.btn_crear_clip_auto.config(state=tk.DISABLED))
            
            # Preparar directorio de salida
            output_dir = Path(self.directorio_descarga.get())
            output_dir.mkdir(exist_ok=True)
            print(f"📁 DEBUG: Directorio de salida: {output_dir}")
            
            # Obtener extensión del archivo original
            extension = Path(self.video_temp_path).suffix
            output_path = output_dir / f"{nombre}{extension}"
            print(f"📄 DEBUG: Archivo de salida: {output_path}")
            
            # Calcular duración del clip
            inicio_seg = self._tiempo_a_segundos(inicio)
            fin_seg = self._tiempo_a_segundos(fin)
            duracion = fin_seg - inicio_seg
            print(f"⏱️ DEBUG: Duración del clip: {duracion}s")
            
            # Comando ffmpeg para crear el clip
            cmd = [
                "ffmpeg", "-y",  # -y para sobrescribir sin preguntar
                "-i", self.video_temp_path,
                "-ss", inicio,  # Tiempo de inicio
                "-t", str(duracion),  # Duración del clip
                "-c", "copy",  # Copiar streams sin re-encodificar (más rápido)
                str(output_path)
            ]
            
            print(f"🔧 DEBUG: Comando ffmpeg: {' '.join(cmd)}")
            
            # Ejecutar comando
            resultado = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            
            print(f"📊 DEBUG: Código de retorno: {resultado.returncode}")
            if resultado.stderr:
                print(f"⚠️ DEBUG: stderr: {resultado.stderr}")
            if resultado.stdout:
                print(f"ℹ️ DEBUG: stdout: {resultado.stdout}")
            
            if resultado.returncode == 0:
                print("✅ DEBUG: Clip creado exitosamente")
                self.root.after(0, lambda: self.progreso_clip_var.set(f"✅ Clip creado: {output_path.name}"))
                self.root.after(0, lambda: messagebox.showinfo("✅ Éxito", f"Clip creado exitosamente:\n{output_path}"))
            else:
                error_msg = f"Error de ffmpeg: {resultado.stderr}"
                print(f"❌ DEBUG: Error ffmpeg: {error_msg}")
                self.root.after(0, lambda: self.progreso_clip_var.set("❌ Error creando clip"))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                
        except FileNotFoundError:
            error_msg = "❌ ffmpeg no encontrado. Asegúrate de que esté instalado y en el PATH."
            print(f"❌ DEBUG: {error_msg}")
            self.root.after(0, lambda: self.progreso_clip_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        except Exception as e:
            error_msg = f"❌ Error creando clip: {str(e)}"
            print(f"💥 DEBUG: Excepción: {error_msg}")
            self.root.after(0, lambda: self.progreso_clip_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            print("🏁 DEBUG: Finalizando hilo de creación original")
            self.root.after(0, self.progress_bar_clip.stop)
            self.root.after(0, lambda: self.btn_crear_clip_original.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_crear_clip_auto.config(state=tk.NORMAL))
    
    def _crear_clip_automatico_thread(self, inicio, fin, nombre):
        """Hilo para crear clip con descarga automática y limpieza"""
        video_temp_path = None
        try:
            print("🚀 DEBUG: Iniciando proceso automático de clip")
            self.root.after(0, lambda: self.progreso_clip_var.set("📥 Descargando video completo..."))
            self.root.after(0, self.progress_bar_clip.start)
            self.root.after(0, lambda: self.btn_crear_clip_auto.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.btn_crear_clip_original.config(state=tk.DISABLED))
            
            # Paso 1: Descargar el video completo temporalmente
            url = self.url_clip_var.get()
            temp_dir = Path("temp_clips")
            temp_dir.mkdir(exist_ok=True)
            
            print(f"📥 DEBUG: Descargando video de {url}")
            
            # Configurar yt-dlp para descarga temporal
            # Usar formato flexible que intenta mejor opción pero fallback a alternativas
            ydl_opts = {
                'format': 'bestvideo[height<=720]/best[height<=720]/bestvideo/best',
                'outtmpl': str(temp_dir / '%(title)s.%(ext)s'),
                'noplaylist': True,
                'quiet': False,
                'no_warnings': False
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_filename = ydl.prepare_filename(info)
                video_temp_path = Path(video_filename)
                
                # Si el archivo no existe con ese nombre exacto, buscar en el directorio
                if not video_temp_path.exists():
                    video_files = list(temp_dir.glob("*"))
                    video_files = [f for f in video_files if f.is_file() and f.suffix in ['.mp4', '.webm', '.mkv']]
                    if video_files:
                        video_temp_path = video_files[0]
                    else:
                        raise FileNotFoundError("No se pudo encontrar el video descargado")
            
            print(f"✅ DEBUG: Video descargado: {video_temp_path}")
            
            # Paso 2: Crear el clip
            self.root.after(0, lambda: self.progreso_clip_var.set("✂️ Creando clip..."))
            
            # Preparar directorio de salida (directorio final, no temporal)
            output_dir = Path(self.directorio_descarga.get())
            output_dir.mkdir(exist_ok=True)
            print(f"📁 DEBUG: Directorio de salida: {output_dir}")
            
            # Crear archivo de salida
            extension = video_temp_path.suffix
            output_path = output_dir / f"{nombre}{extension}"
            print(f"📄 DEBUG: Archivo de salida: {output_path}")
            
            # Calcular duración del clip
            inicio_seg = self._tiempo_a_segundos(inicio)
            fin_seg = self._tiempo_a_segundos(fin)
            duracion = fin_seg - inicio_seg
            print(f"⏱️ DEBUG: Duración del clip: {duracion}s")
            
            # Comando ffmpeg para crear el clip
            cmd = [
                "ffmpeg", "-y",  # -y para sobrescribir sin preguntar
                "-i", str(video_temp_path),
                "-ss", inicio,  # Tiempo de inicio
                "-t", str(duracion),  # Duración del clip
                "-c", "copy",  # Copiar streams sin re-encodificar (más rápido)
                str(output_path)
            ]
            
            print(f"🔧 DEBUG: Comando ffmpeg: {' '.join(cmd)}")
            
            # Ejecutar comando
            resultado = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            
            print(f"📊 DEBUG: Código de retorno: {resultado.returncode}")
            if resultado.stderr:
                print(f"⚠️ DEBUG: stderr: {resultado.stderr}")
            if resultado.stdout:
                print(f"ℹ️ DEBUG: stdout: {resultado.stdout}")
            
            if resultado.returncode == 0:
                print("✅ DEBUG: Clip creado exitosamente")
                
                # Paso 3: Borrar el video temporal
                self.root.after(0, lambda: self.progreso_clip_var.set("🗑️ Limpiando archivos temporales..."))
                try:
                    if video_temp_path and video_temp_path.exists():
                        video_temp_path.unlink()
                        print(f"🗑️ DEBUG: Video temporal eliminado: {video_temp_path}")
                    
                    # Limpiar directorio temporal si está vacío
                    if temp_dir.exists() and not list(temp_dir.iterdir()):
                        temp_dir.rmdir()
                        print("🗑️ DEBUG: Directorio temporal eliminado")
                        
                except Exception as e:
                    print(f"⚠️ DEBUG: Error limpiando archivos temporales: {e}")
                
                # Actualizar UI con éxito
                self.root.after(0, lambda: self.progreso_clip_var.set(f"✅ Clip creado y guardado"))
                self.root.after(0, lambda: messagebox.showinfo("✅ Éxito", 
                    f"¡Clip creado exitosamente!\n\n📁 Guardado en: {output_path}\n🗑️ Video temporal eliminado"))
            else:
                error_msg = f"Error de ffmpeg: {resultado.stderr}"
                print(f"❌ DEBUG: Error ffmpeg: {error_msg}")
                self.root.after(0, lambda: self.progreso_clip_var.set("❌ Error creando clip"))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                
        except FileNotFoundError as e:
            if "ffmpeg" in str(e).lower():
                error_msg = "❌ ffmpeg no encontrado. Asegúrate de que esté instalado y en el PATH."
            else:
                error_msg = f"❌ Archivo no encontrado: {str(e)}"
            print(f"❌ DEBUG: {error_msg}")
            self.root.after(0, lambda: self.progreso_clip_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        except Exception as e:
            error_str = str(e)
            
            # Detectar tipos específicos de errores
            if "Only images are available" in error_str or "format is not available" in error_str.lower():
                error_msg = ("❌ Video protegido o restringido\n\n"
                           "Este video no puede ser descargado porque:\n"
                           "• YouTube lo tiene protegido o restringido\n"
                           "• Solo hay imágenes disponibles para descarga\n"
                           "• El contenido puede ser de acceso limitado\n\n"
                           "Intenta con otro video de YouTube.")
            elif "nsig extraction failed" in error_str.lower():
                error_msg = ("❌ Error de extracción de firma\n\n"
                           "Intenta actualizar yt-dlp:\n"
                           "pip install --upgrade yt-dlp")
            elif "HTTP Error 403" in error_str or "HTTP Error 404" in error_str:
                error_msg = ("❌ Error de acceso al video\n\n"
                           "El video puede estar:\n"
                           "• Privado o eliminado\n"
                           "• Restringido por región\n"
                           "• No disponible en tu país")
            else:
                error_msg = f"❌ Error en proceso automático: {error_str}"
            
            print(f"💥 DEBUG: Excepción: {error_msg}")
            self.root.after(0, lambda: self.progreso_clip_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            # Limpiar archivo temporal en caso de error
            if video_temp_path and video_temp_path.exists():
                try:
                    video_temp_path.unlink()
                    print(f"🗑️ DEBUG: Video temporal limpiado en finally: {video_temp_path}")
                except:
                    pass
                    
            print("🏁 DEBUG: Finalizando proceso automático")
            self.root.after(0, self.progress_bar_clip.stop)
            self.root.after(0, lambda: self.btn_crear_clip_auto.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_crear_clip_original.config(state=tk.NORMAL))
    
    
    def limpiar_archivos_temporales(self):
        """Limpia los archivos temporales"""
        if messagebox.askyesno("⚠️ Confirmar", "¿Deseas eliminar los archivos temporales?"):
            try:
                temp_dir = Path("temp_clips")
                if temp_dir.exists():
                    archivos_eliminados = 0
                    for archivo in temp_dir.glob("*"):
                        if archivo.is_file():
                            archivo.unlink()
                            archivos_eliminados += 1
                    
                    # Limpiar variables
                    self.video_temp_path = None
                    self.video_info_clip = None
                    self.btn_crear_clip_original.config(state=tk.DISABLED)
                    self.btn_crear_clip_auto.config(state=tk.DISABLED)
                    self.btn_descargar_temp.config(state=tk.DISABLED)
                    
                    # Limpiar campos
                    self.url_clip_var.set("")
                    self.info_clip_text.config(state=tk.NORMAL)
                    self.info_clip_text.delete(1.0, tk.END)
                    self.info_clip_text.config(state=tk.DISABLED)
                    self.progreso_clip_var.set("🗑️ Archivos temporales eliminados")
                    
                    messagebox.showinfo("✅ Éxito", f"Se eliminaron {archivos_eliminados} archivos temporales")
                else:
                    messagebox.showinfo("ℹ️ Información", "No hay archivos temporales")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error limpiando archivos temporales: {str(e)}")

    # ==================== FUNCIONES PARA ARCHIVOS LOCALES ====================
    
    def seleccionar_archivo_local(self):
        """Permite seleccionar un archivo de video local"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de video",
            filetypes=[
                ("Videos", "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.m4v"),
                ("MP4", "*.mp4"),
                ("AVI", "*.avi"),
                ("MKV", "*.mkv"),
                ("MOV", "*.mov"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if archivo:
            self.archivo_local_var.set(archivo)
            self.archivo_local_path = archivo
            self.btn_info_archivo.config(state=tk.NORMAL)
            self.progreso_archivo_var.set("📁 Archivo seleccionado. Obtén la información para continuar.")
    
    def obtener_info_archivo_local(self):
        """Obtiene información del archivo de video local usando ffprobe"""
        archivo_path = self.archivo_local_var.get().strip()
        if not archivo_path:
            messagebox.showwarning("⚠️ Advertencia", "Por favor selecciona un archivo de video")
            return
        
        threading.Thread(target=self._obtener_info_archivo_thread, args=(archivo_path,), daemon=True).start()
    
    def _obtener_info_archivo_thread(self, archivo_path):
        """Hilo para obtener información del archivo usando ffprobe"""
        self.root.after(0, lambda: self.progreso_archivo_var.set("🔍 Obteniendo información del archivo..."))
        self.root.after(0, self.progress_bar_archivo.start)
        
        try:
            # Usar ffprobe para obtener información del archivo
            cmd = [
                "ffprobe", "-v", "quiet", "-print_format", "json", 
                "-show_format", "-show_streams", archivo_path
            ]
            
            resultado = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
            
            if resultado.returncode == 0:
                import json
                info = json.loads(resultado.stdout)
                
                # Procesar información
                format_info = info.get('format', {})
                video_stream = None
                
                # Encontrar el stream de video
                for stream in info.get('streams', []):
                    if stream.get('codec_type') == 'video':
                        video_stream = stream
                        break
                
                if video_stream:
                    # Crear objeto de información similar al de yt-dlp
                    video_info = {
                        'title': Path(archivo_path).stem,
                        'duration': float(format_info.get('duration', 0)),
                        'width': video_stream.get('width', 0),
                        'height': video_stream.get('height', 0),
                        'fps': eval(video_stream.get('avg_frame_rate', '0/1')),
                        'codec': video_stream.get('codec_name', 'desconocido'),
                        'filesize': int(format_info.get('size', 0)),
                        'format': format_info.get('format_name', 'desconocido'),
                        'bitrate': int(format_info.get('bit_rate', 0)) if format_info.get('bit_rate') else 0
                    }
                    
                    self.video_info_archivo = video_info
                    self.root.after(0, self._mostrar_info_archivo, video_info)
                else:
                    raise Exception("No se encontró stream de video en el archivo")
            else:
                raise Exception(f"Error ejecutando ffprobe: {resultado.stderr}")
                
        except FileNotFoundError:
            error_msg = "❌ ffprobe no encontrado. Instala FFmpeg para usar esta función."
            self.root.after(0, lambda: self.progreso_archivo_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        except subprocess.TimeoutExpired:
            error_msg = "❌ Tiempo agotado obteniendo información del archivo."
            self.root.after(0, lambda: self.progreso_archivo_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        except Exception as e:
            error_msg = f"❌ Error obteniendo información: {str(e)}"
            self.root.after(0, lambda: self.progreso_archivo_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            self.root.after(0, self.progress_bar_archivo.stop)
    
    def _mostrar_info_archivo(self, info):
        """Muestra la información del archivo local"""
        titulo = info.get('title', 'Sin título')
        duracion = self._formatear_duracion(int(info.get('duration', 0)))
        resolucion = f"{info.get('width', 0)}x{info.get('height', 0)}"
        fps = info.get('fps', 0)
        codec = info.get('codec', 'desconocido')
        formato = info.get('format', 'desconocido')
        tamaño = self._formatear_tamaño(info.get('filesize', 0))
        
        # Actualizar texto en el frame de información de archivo
        info_basica = f"📁 {titulo}\n🎞️ {resolucion} | ⚡ {fps:.1f} fps | 🎬 {codec} | 📊 {tamaño}\n⏱️ Duración: {duracion} | 📋 Formato: {formato}"
        
        self.info_archivo_text.config(state=tk.NORMAL)
        self.info_archivo_text.delete(1.0, tk.END)
        self.info_archivo_text.insert(1.0, info_basica)
        self.info_archivo_text.config(state=tk.DISABLED)
        
        # Habilitar botones de procesamiento
        self.btn_crear_clip_archivo.config(state=tk.NORMAL)
        self.btn_convertir_clip_archivo.config(state=tk.NORMAL)
        
        # Establecer tiempo de fin por defecto basado en la duración
        if info.get('duration'):
            duracion_formateada = self._segundos_a_tiempo(min(300, int(info.get('duration'))))  # Max 5 minutos
            self.fin_archivo_var.set(duracion_formateada)
        
        # Establecer nombre por defecto basado en el título del archivo
        nombre_limpio = "".join(c for c in titulo if c.isalnum() or c in (' ', '-', '_')).rstrip()[:30]
        self.nombre_archivo_clip_var.set(f"clip_{nombre_limpio}")
        
        self.progreso_archivo_var.set("✅ Información obtenida. Elige tu método de procesamiento:")
    
    def _formatear_tamaño(self, bytes_size):
        """Convierte bytes a formato legible"""
        if bytes_size == 0:
            return "Desconocido"
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
        return f"{bytes_size:.1f} TB"
    
    def set_tiempo_rapido_archivo(self, inicio, fin):
        """Establece tiempos rápidos predefinidos para archivos"""
        self.inicio_archivo_var.set(inicio)
        self.fin_archivo_var.set(fin)
    
    def crear_clip_archivo(self):
        """Crea un clip directamente del archivo local"""
        print("✂️ DEBUG: Iniciando crear_clip_archivo()")
        
        if not self.archivo_local_path or not os.path.exists(self.archivo_local_path):
            print("❌ DEBUG: Archivo local no encontrado")
            messagebox.showwarning("⚠️ Advertencia", "Por favor selecciona un archivo de video válido")
            return
        
        # Validar campos
        inicio = self.inicio_archivo_var.get().strip()
        fin = self.fin_archivo_var.get().strip()
        nombre = self.nombre_archivo_clip_var.get().strip()
        
        print(f"📋 DEBUG: Datos - Archivo: {self.archivo_local_path}")
        print(f"📋 DEBUG: Datos - Inicio: {inicio}, Fin: {fin}, Nombre: {nombre}")
        
        if not all([inicio, fin, nombre]):
            print("❌ DEBUG: Campos incompletos")
            messagebox.showwarning("⚠️ Advertencia", "Completa todos los campos")
            return
        
        # Convertir tiempos a segundos para validación
        inicio_seg = self._tiempo_a_segundos(inicio)
        fin_seg = self._tiempo_a_segundos(fin)
        
        print(f"⏱️ DEBUG: Tiempos convertidos - Inicio: {inicio_seg}s, Fin: {fin_seg}s")
        
        if inicio_seg >= fin_seg:
            print("❌ DEBUG: Tiempo de inicio >= tiempo de fin")
            messagebox.showwarning("⚠️ Advertencia", "El tiempo de inicio debe ser menor al tiempo de fin")
            return
        
        print("✅ DEBUG: Validaciones pasadas, iniciando procesamiento...")
        threading.Thread(target=self._crear_clip_archivo_thread, args=(inicio, fin, nombre), daemon=True).start()
    
    def _crear_clip_archivo_thread(self, inicio, fin, nombre):
        """Hilo para crear clip del archivo local"""
        try:
            print("✂️ DEBUG: Iniciando hilo de creación de clip de archivo")
            self.root.after(0, lambda: self.progreso_archivo_var.set("✂️ Creando clip desde archivo local..."))
            self.root.after(0, self.progress_bar_archivo.start)
            self.root.after(0, lambda: self.btn_crear_clip_archivo.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.btn_convertir_clip_archivo.config(state=tk.DISABLED))
            
            # Preparar directorio de salida
            output_dir = Path(self.directorio_descarga.get())
            output_dir.mkdir(exist_ok=True)
            print(f"📁 DEBUG: Directorio de salida: {output_dir}")
            
            # Obtener extensión del archivo original
            extension = Path(self.archivo_local_path).suffix
            output_path = output_dir / f"{nombre}{extension}"
            print(f"📄 DEBUG: Archivo de salida: {output_path}")
            
            # Calcular duración del clip
            inicio_seg = self._tiempo_a_segundos(inicio)
            fin_seg = self._tiempo_a_segundos(fin)
            duracion = fin_seg - inicio_seg
            print(f"⏱️ DEBUG: Duración del clip: {duracion}s")
            
            # Comando ffmpeg para crear el clip
            cmd = [
                "ffmpeg", "-y",  # -y para sobrescribir sin preguntar
                "-i", self.archivo_local_path,
                "-ss", inicio,  # Tiempo de inicio
                "-t", str(duracion),  # Duración del clip
                "-c", "copy",  # Copiar streams sin re-encodificar (más rápido)
                str(output_path)
            ]
            
            print(f"🔧 DEBUG: Comando ffmpeg: {' '.join(cmd)}")
            
            # Ejecutar comando
            resultado = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            
            print(f"📊 DEBUG: Código de retorno: {resultado.returncode}")
            if resultado.stderr:
                print(f"⚠️ DEBUG: stderr: {resultado.stderr}")
            if resultado.stdout:
                print(f"ℹ️ DEBUG: stdout: {resultado.stdout}")
            
            if resultado.returncode == 0:
                print("✅ DEBUG: Clip creado exitosamente")
                self.root.after(0, lambda: self.progreso_archivo_var.set(f"✅ Clip creado: {output_path.name}"))
                self.root.after(0, lambda: messagebox.showinfo("✅ Éxito", f"Clip creado exitosamente:\n{output_path}"))
            else:
                error_msg = f"Error de ffmpeg: {resultado.stderr}"
                print(f"❌ DEBUG: Error ffmpeg: {error_msg}")
                self.root.after(0, lambda: self.progreso_archivo_var.set("❌ Error creando clip"))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                
        except FileNotFoundError:
            error_msg = "❌ ffmpeg no encontrado. Asegúrate de que esté instalado y en el PATH."
            print(f"❌ DEBUG: {error_msg}")
            self.root.after(0, lambda: self.progreso_archivo_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        except Exception as e:
            error_msg = f"❌ Error creando clip: {str(e)}"
            print(f"💥 DEBUG: Excepción: {error_msg}")
            self.root.after(0, lambda: self.progreso_archivo_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            print("🏁 DEBUG: Finalizando hilo de creación de archivo")
            self.root.after(0, self.progress_bar_archivo.stop)
            self.root.after(0, lambda: self.btn_crear_clip_archivo.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_convertir_clip_archivo.config(state=tk.NORMAL))
    
    def convertir_y_crear_clip_archivo(self):
        """Convierte el archivo y crea un clip (útil para formatos incompatibles)"""
        print("🎞️ DEBUG: Iniciando convertir_y_crear_clip_archivo()")
        
        if not self.archivo_local_path or not os.path.exists(self.archivo_local_path):
            print("❌ DEBUG: Archivo local no encontrado")
            messagebox.showwarning("⚠️ Advertencia", "Por favor selecciona un archivo de video válido")
            return
        
        # Validar campos
        inicio = self.inicio_archivo_var.get().strip()
        fin = self.fin_archivo_var.get().strip()
        nombre = self.nombre_archivo_clip_var.get().strip()
        
        print(f"📋 DEBUG: Datos - Archivo: {self.archivo_local_path}")
        print(f"📋 DEBUG: Datos - Inicio: {inicio}, Fin: {fin}, Nombre: {nombre}")
        
        if not all([inicio, fin, nombre]):
            print("❌ DEBUG: Campos incompletos")
            messagebox.showwarning("⚠️ Advertencia", "Completa todos los campos")
            return
        
        # Convertir tiempos a segundos para validación
        inicio_seg = self._tiempo_a_segundos(inicio)
        fin_seg = self._tiempo_a_segundos(fin)
        
        print(f"⏱️ DEBUG: Tiempos convertidos - Inicio: {inicio_seg}s, Fin: {fin_seg}s")
        
        if inicio_seg >= fin_seg:
            print("❌ DEBUG: Tiempo de inicio >= tiempo de fin")
            messagebox.showwarning("⚠️ Advertencia", "El tiempo de inicio debe ser menor al tiempo de fin")
            return
        
        print("✅ DEBUG: Validaciones pasadas, iniciando conversión...")
        threading.Thread(target=self._convertir_y_crear_clip_archivo_thread, args=(inicio, fin, nombre), daemon=True).start()
    
    def _convertir_y_crear_clip_archivo_thread(self, inicio, fin, nombre):
        """Hilo para convertir y crear clip del archivo local"""
        try:
            print("🎞️ DEBUG: Iniciando hilo de conversión y creación de clip")
            self.root.after(0, lambda: self.progreso_archivo_var.set("🎞️ Convirtiendo y creando clip..."))
            self.root.after(0, self.progress_bar_archivo.start)
            self.root.after(0, lambda: self.btn_crear_clip_archivo.config(state=tk.DISABLED))
            self.root.after(0, lambda: self.btn_convertir_clip_archivo.config(state=tk.DISABLED))
            
            # Preparar directorio de salida
            output_dir = Path(self.directorio_descarga.get())
            output_dir.mkdir(exist_ok=True)
            print(f"📁 DEBUG: Directorio de salida: {output_dir}")
            
            # Crear archivo de salida (siempre MP4 para compatibilidad)
            output_path = output_dir / f"{nombre}.mp4"
            print(f"📄 DEBUG: Archivo de salida: {output_path}")
            
            # Calcular duración del clip
            inicio_seg = self._tiempo_a_segundos(inicio)
            fin_seg = self._tiempo_a_segundos(fin)
            duracion = fin_seg - inicio_seg
            print(f"⏱️ DEBUG: Duración del clip: {duracion}s")
            
            # Comando ffmpeg para convertir y crear el clip
            cmd = [
                "ffmpeg", "-y",  # -y para sobrescribir sin preguntar
                "-i", self.archivo_local_path,
                "-ss", inicio,  # Tiempo de inicio
                "-t", str(duracion),  # Duración del clip
                "-c:v", "libx264",  # Codec de video H.264
                "-c:a", "aac",  # Codec de audio AAC
                "-preset", "medium",  # Preset de velocidad/calidad
                "-crf", "23",  # Calidad constante (0-51, menor = mejor calidad)
                str(output_path)
            ]
            
            print(f"🔧 DEBUG: Comando ffmpeg: {' '.join(cmd)}")
            
            # Ejecutar comando
            resultado = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
            
            print(f"📊 DEBUG: Código de retorno: {resultado.returncode}")
            if resultado.stderr:
                print(f"⚠️ DEBUG: stderr: {resultado.stderr}")
            if resultado.stdout:
                print(f"ℹ️ DEBUG: stdout: {resultado.stdout}")
            
            if resultado.returncode == 0:
                print("✅ DEBUG: Clip convertido y creado exitosamente")
                self.root.after(0, lambda: self.progreso_archivo_var.set(f"✅ Clip convertido y creado: {output_path.name}"))
                self.root.after(0, lambda: messagebox.showinfo("✅ Éxito", f"Clip convertido y creado exitosamente:\n{output_path}"))
            else:
                error_msg = f"Error de ffmpeg: {resultado.stderr}"
                print(f"❌ DEBUG: Error ffmpeg: {error_msg}")
                self.root.after(0, lambda: self.progreso_archivo_var.set("❌ Error convirtiendo clip"))
                self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                
        except FileNotFoundError:
            error_msg = "❌ ffmpeg no encontrado. Asegúrate de que esté instalado y en el PATH."
            print(f"❌ DEBUG: {error_msg}")
            self.root.after(0, lambda: self.progreso_archivo_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        except Exception as e:
            error_msg = f"❌ Error convirtiendo clip: {str(e)}"
            print(f"💥 DEBUG: Excepción: {error_msg}")
            self.root.after(0, lambda: self.progreso_archivo_var.set(error_msg))
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
        
        finally:
            print("🏁 DEBUG: Finalizando hilo de conversión")
            self.root.after(0, self.progress_bar_archivo.stop)
            self.root.after(0, lambda: self.btn_crear_clip_archivo.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_convertir_clip_archivo.config(state=tk.NORMAL))
    
    def limpiar_seleccion_archivo(self):
        """Limpia la selección de archivo y resetea la interfaz"""
        if messagebox.askyesno("⚠️ Confirmar", "¿Deseas limpiar la selección actual?"):
            try:
                # Limpiar variables
                self.archivo_local_var.set("")
                self.archivo_local_path = None
                self.video_info_archivo = None
                
                # Deshabilitar botones
                self.btn_info_archivo.config(state=tk.DISABLED)
                self.btn_crear_clip_archivo.config(state=tk.DISABLED)
                self.btn_convertir_clip_archivo.config(state=tk.DISABLED)
                
                # Limpiar campos de tiempo y nombre
                self.inicio_archivo_var.set("00:00:00")
                self.fin_archivo_var.set("00:01:00")
                self.nombre_archivo_clip_var.set("clip_archivo_1")
                
                # Limpiar información
                self.info_archivo_text.config(state=tk.NORMAL)
                self.info_archivo_text.delete(1.0, tk.END)
                self.info_archivo_text.config(state=tk.DISABLED)
                
                self.progreso_archivo_var.set("🗑️ Selección limpiada. Selecciona un nuevo archivo.")
                
                messagebox.showinfo("✅ Éxito", "Selección limpiada correctamente")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error limpiando selección: {str(e)}")


def main():
    """Función principal"""
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
