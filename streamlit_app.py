#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 YouTube Downloader & Clip Creator - Streamlit Version
Aplicación moderna con timeline visual para gestionar clips de video
Migrada desde tkinter para mejor experiencia de usuario
"""

import streamlit as st
import yt_dlp
import subprocess
import json
import os
import threading
import time
from pathlib import Path
from datetime import datetime
import tempfile
import shutil

# Configuración de página
st.set_page_config(
    page_title="🎬 YouTube Downloader Pro",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 2rem;
    }
    
    .video-info-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #4ECDC4;
        margin: 1rem 0;
    }
    
    .timeline-container {
        background-color: #ffffff;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    
    .clip-preview {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1rem;
        font-weight: bold;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        background: linear-gradient(90deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Menu horizontal mejorado */
    .menu-button {
        text-align: center;
        margin: 0 0.5rem;
    }
    
    /* Mejorar inputs */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Mejorar sliders */
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #667eea, #764ba2);
    }
    
    /* Mejorar selectbox */
    .stSelectbox > div > div > select {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        padding: 0.5rem;
    }
    
    /* Contenedor principal */
    .block-container {
        padding-top: 2rem;
        max-width: 1200px;
    }
    
    /* Título de sección mejorado */
    .section-title {
        color: #2d3748;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #f7fafc, #edf2f7);
        border-radius: 10px;
        border-left: 5px solid #667eea;
    }
    
    .timeline-marker {
        background-color: #FF6B6B;
        height: 20px;
        border-radius: 10px;
        margin: 5px 0;
    }
    
    /* Video centrado responsive */
    .video-container {
        display: flex;
        justify-content: center;
        margin: 1.5rem 0;
        padding: 1rem;
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .video-container iframe {
        border-radius: 10px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    
    .video-container iframe:hover {
        transform: scale(1.02);
    }
    
    /* Responsive video en móviles */
    @media (max-width: 768px) {
        .video-container iframe {
            width: 100%;
            height: 225px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Funciones auxiliares
@st.cache_data(ttl=3600)  # Cache por 1 hora
def get_video_info(url):
    """Obtiene información del video con cache por URL"""
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'restrictfilenames': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except Exception as e:
        st.error(f"❌ Error obteniendo información: {str(e)}")
        return None

def format_duration(seconds):
    """Convierte segundos a formato HH:MM:SS"""
    if not seconds:
        return "Desconocida"
    
    # Convertir a entero para evitar errores con valores float
    seconds = int(float(seconds))
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes:02d}:{seconds:02d}"

def time_to_seconds(time_str):
    """Convierte tiempo HH:MM:SS a segundos"""
    try:
        parts = time_str.split(':')
        if len(parts) == 3:
            h, m, s = map(int, parts)
            return h * 3600 + m * 60 + s
        elif len(parts) == 2:
            m, s = map(int, parts)
            return m * 60 + s
        else:
            return int(parts[0])
    except:
        return 0

def seconds_to_time(seconds):
    """Convierte segundos a formato HH:MM:SS"""
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def get_basic_video_duration(video_path):
    """Obtiene solo la duración del video usando ffprobe (rápido)"""
    try:
        cmd = ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", 
               "-of", "csv=p=0", video_path]
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=10)
        if result.returncode == 0:
            return float(result.stdout.strip())
    except:
        pass
    return None

def create_clip_ffmpeg(video_path, start_time, end_time, output_path):
    """Crea un clip usando ffmpeg"""
    try:
        duration = time_to_seconds(end_time) - time_to_seconds(start_time)
        
        cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-ss", start_time,
            "-t", str(duration),
            "-c", "copy",
            output_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
        return result.returncode == 0, result.stderr
    except Exception as e:
        return False, str(e)

# Inicializar estado de la sesión
if 'video_info' not in st.session_state:
    st.session_state.video_info = None
if 'downloaded_video_path' not in st.session_state:
    st.session_state.downloaded_video_path = None
if 'clips_created' not in st.session_state:
    st.session_state.clips_created = []
if 'local_video_path' not in st.session_state:
    st.session_state.local_video_path = None
if 'local_video_info' not in st.session_state:
    st.session_state.local_video_info = None
if 'local_basic_duration' not in st.session_state:
    st.session_state.local_basic_duration = None
# Variables para controlar los valores de los sliders desde los botones rápidos
# Para videos locales
if 'local_quick_start' not in st.session_state:
    st.session_state.local_quick_start = 0
if 'local_quick_end' not in st.session_state:
    st.session_state.local_quick_end = 60
if 'local_quick_counter' not in st.session_state:
    st.session_state.local_quick_counter = 0
# Para clips de YouTube
if 'youtube_quick_start' not in st.session_state:
    st.session_state.youtube_quick_start = 0
if 'youtube_quick_end' not in st.session_state:
    st.session_state.youtube_quick_end = 60
if 'youtube_quick_counter' not in st.session_state:
    st.session_state.youtube_quick_counter = 0
# URL del video actual para clips
if 'current_clip_url' not in st.session_state:
    st.session_state.current_clip_url = None
# Video descargado de YouTube para clips
if 'downloaded_youtube_path' not in st.session_state:
    st.session_state.downloaded_youtube_path = None
if 'downloaded_youtube_info' not in st.session_state:
    st.session_state.downloaded_youtube_info = None

# Título principal con estilo moderno
st.markdown('<h1 class="main-header">🎬 YouTube Downloader & Clip Creator Pro</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #718096; font-size: 1.2rem; margin-bottom: 2rem;">Timeline visual • Reproducción de video • Clips precisos</p>', unsafe_allow_html=True)
st.markdown("---")

# Menú horizontal fijo
st.markdown("""
<style>
    .menu-container {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 0;
        border-radius: 15px;
        margin-bottom: 2rem;
    }
    
    .menu-item {
        display: inline-block;
        width: 24%;
        text-align: center;
        color: white;
        font-weight: bold;
        text-decoration: none;
        padding: 10px;
        border-radius: 10px;
        margin: 0 0.5%;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .menu-item:hover {
        background-color: rgba(255,255,255,0.2);
        transform: translateY(-2px);
    }
    
    .menu-item.active {
        background-color: rgba(255,255,255,0.3);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Menú horizontal con separadores visuales
st.markdown("---")
st.markdown('<div style="text-align: center; margin: 2rem 0;"><h3 style="color: #4a5568; margin-bottom: 1rem;">🎯 Selecciona una opción</h3></div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    download_btn = st.button("📥 Descargar Videos", use_container_width=True, help="Descarga videos de YouTube, TikTok, Instagram, Facebook y 1000+ sitios más")
with col2:
    clips_btn = st.button("✂️ Crear Clips YouTube", use_container_width=True, help="Crea clips de videos de YouTube con timeline visual") 
with col3:
    local_btn = st.button("📁 Procesar Videos Locales", use_container_width=True, help="Procesa videos desde tu computadora")
with col4:
    info_btn = st.button("ℹ️ Información", use_container_width=True, help="Información sobre la aplicación")

st.markdown("---")

# Determinar página activa
if 'active_page' not in st.session_state:
    st.session_state.active_page = "📥 Descargar Videos"

if download_btn:
    st.session_state.active_page = "📥 Descargar Videos"
elif clips_btn:
    st.session_state.active_page = "✂️ Crear Clips YouTube"
elif local_btn:
    st.session_state.active_page = "📁 Procesar Videos Locales"
elif info_btn:
    st.session_state.active_page = "ℹ️ Información"

page = st.session_state.active_page

# ==================== PÁGINA: DESCARGAR VIDEOS ====================
if page == "📥 Descargar Videos":
    st.markdown('<div class="section-title">📥 Descargador Universal de Videos</div>', unsafe_allow_html=True)
    
    # Información de plataformas soportadas
    st.markdown("### 🌐 Plataformas Populares Soportadas")
    
    col_platforms = st.columns(5)
    with col_platforms[0]:
        st.markdown("**🔴 YouTube**\n- Videos normales\n- Shorts\n- Livestreams")
    with col_platforms[1]:
        st.markdown("**📘 Facebook**\n- Videos públicos\n- Watch videos")
    with col_platforms[2]:
        st.markdown("**📸 Instagram**\n- Reels\n- IGTV\n- Posts con video")
    with col_platforms[3]:
        st.markdown("**🎵 TikTok**\n- Videos públicos\n- Sin marca de agua")
    with col_platforms[4]:
        st.markdown("**🐦 Twitter/X**\n- Videos embebidos\n- Clips compartidos")
    
    # Más plataformas en expandable
    with st.expander("🔍 Ver todas las plataformas soportadas (1000+)"):
        st.markdown("""
        **Redes Sociales:** LinkedIn, Snapchat, Reddit, Pinterest, VK, Odnoklassniki
        
        **Video Streaming:** Vimeo, Dailymotion, Twitch, Rumble, BitChute, Bilibili
        
        **Educación:** Khan Academy, Coursera, edX, Udemy, MIT OpenCourseWare
        
        **Noticias:** CNN, BBC, NBC, ABC News, Reuters, AP News, Sky News
        
        **Entretenimiento:** Comedy Central, Adult Swim, Crunchyroll, Funimation
        
        **Contenido para Adultos:** Pornhub, Xvideos, Xhamster y otros sitios 🔞
        
        **Deportes:** ESPN, NFL, NBA, FIFA, Olympics
        
        **Música:** SoundCloud, Bandcamp, Mixcloud
        
        **Y muchas más...** yt-dlp soporta más de 1000 sitios web diferentes.
        
        ⚠️ **Nota:** Siempre respeta los términos de servicio y las leyes locales.
        """)
    
    
    st.markdown("---")
    
    # Input URL con estilo mejorado
    st.markdown("### 🔗 Ingresa la URL del video")
    url = st.text_input("URL del Video (cualquier plataforma soportada):", 
                       placeholder="https://www.youtube.com/watch?v=... o https://www.tiktok.com/@user/video/... etc.",
                       help="Funciona con YouTube, TikTok, Instagram, Facebook, Twitter, Vimeo y 1000+ sitios más")
    
    # Detección automática de plataforma (mejorada)
    if url:
        platform = "Desconocida"
        platform_emoji = "🌐"
        
        # Plataformas principales
        if 'youtube.com' in url or 'youtu.be' in url:
            platform = "YouTube"
            platform_emoji = "🔴"
        elif 'tiktok.com' in url:
            platform = "TikTok"
            platform_emoji = "🎵"
        elif 'instagram.com' in url:
            platform = "Instagram"
            platform_emoji = "📸"
        elif 'facebook.com' in url or 'fb.watch' in url:
            platform = "Facebook"
            platform_emoji = "📘"
        elif 'twitter.com' in url or 'x.com' in url:
            platform = "Twitter/X"
            platform_emoji = "🐦"
        elif 'vimeo.com' in url:
            platform = "Vimeo"
            platform_emoji = "🎬"
        elif 'twitch.tv' in url:
            platform = "Twitch"
            platform_emoji = "🟣"
        
        # Plataformas de video adicionales
        elif 'dailymotion.com' in url:
            platform = "Dailymotion"
            platform_emoji = "🟠"
        elif 'vk.com' in url:
            platform = "VK"
            platform_emoji = "🔵"
        elif 'ok.ru' in url:
            platform = "Odnoklassniki"
            platform_emoji = "🟤"
        elif 'bilibili.com' in url:
            platform = "Bilibili"
            platform_emoji = "📺"
        
        # Plataformas de noticias
        elif any(news in url for news in ['cnn.com', 'bbc.com', 'reuters.com', 'nbcnews.com']):
            platform = "Noticias"
            platform_emoji = "📰"
        
        # Plataformas para adultos (también soportadas por yt-dlp)
        elif any(adult in url for adult in ['pornhub.com', 'xvideos.com', 'xhamster.com', 'redtube.com', 'tube8.com', 'youporn.com', 'spankbang.com']):
            platform = "Contenido para Adultos"
            platform_emoji = "🔞"
        
        # Otras plataformas
        elif 'reddit.com' in url:
            platform = "Reddit"
            platform_emoji = "🤖"
        elif 'linkedin.com' in url:
            platform = "LinkedIn"
            platform_emoji = "💼"
        elif 'rumble.com' in url:
            platform = "Rumble"
            platform_emoji = "📻"
        
        st.info(f"{platform_emoji} **Plataforma detectada:** {platform}")
        
        # Advertencia para contenido adulto
        if platform_emoji == "🔞":
            st.warning("⚠️ **Contenido para Adultos Detectado** - Asegúrate de cumplir con las leyes locales y términos de uso.")
    
    
    if st.button("🔍 Obtener Información del Video", use_container_width=True) and url:
        with st.spinner("🔍 Obteniendo información del video..."):
            video_info = get_video_info(url)
            if video_info:
                st.session_state.video_info = video_info
                
                # Mostrar información del video con estilo mejorado
                st.markdown('<div class="video-info-card">', unsafe_allow_html=True)
                st.markdown("### 📺 Información del Video")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**📺 Título:** {video_info.get('title', 'Sin título')}")
                    st.markdown(f"**👤 Canal:** {video_info.get('uploader', 'Desconocido')}")
                    st.markdown(f"**⏱️ Duración:** {format_duration(video_info.get('duration', 0))}")
                
                with col2:
                    st.markdown(f"**📅 Fecha:** {video_info.get('upload_date', 'Desconocida')}")
                    view_count = video_info.get('view_count', 'N/A')
                    if isinstance(view_count, (int, float)) and view_count is not None:
                        st.markdown(f"**👁️ Vistas:** {view_count:,}")
                    else:
                        st.markdown(f"**👁️ Vistas:** {view_count}")
                    like_count = video_info.get('like_count', 'N/A')
                    if isinstance(like_count, (int, float)) and like_count is not None:
                        st.markdown(f"**👍 Likes:** {like_count:,}")
                    else:
                        st.markdown(f"**👍 Likes:** {like_count}")
                
                # Thumbnail y vista previa mejorada para múltiples plataformas
                if video_info.get('thumbnail'):
                    st.markdown("### 🖼️ Vista Previa")
                    col_thumb, col_video = st.columns([1, 1])
                    
                    with col_thumb:
                        st.image(video_info['thumbnail'], width=300, caption="Miniatura del video")
                    
                    with col_video:
                        st.subheader("🎬 Vista del Video")
                        
                        # Vista previa específica por plataforma
                        if 'youtube.com' in url or 'youtu.be' in url:
                            try:
                                import re
                                youtube_regex = r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)'
                                match = re.search(youtube_regex, url)
                                if match:
                                    video_id = match.group(1)
                                    embed_url = f"https://www.youtube.com/embed/{video_id}"
                                    st.markdown(f"""
                                    <iframe width="100%" height="200" 
                                    src="{embed_url}" 
                                    frameborder="0" 
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                                    allowfullscreen>
                                    </iframe>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.info("💡 No se pudo cargar la vista previa de YouTube")
                            except Exception as e:
                                st.warning("⚠️ Error cargando vista previa de YouTube")
                        
                        elif 'vimeo.com' in url:
                            try:
                                import re
                                vimeo_regex = r'vimeo\.com/(\d+)'
                                match = re.search(vimeo_regex, url)
                                if match:
                                    video_id = match.group(1)
                                    embed_url = f"https://player.vimeo.com/video/{video_id}"
                                    st.markdown(f"""
                                    <iframe width="100%" height="200" 
                                    src="{embed_url}" 
                                    frameborder="0" 
                                    allow="autoplay; fullscreen; picture-in-picture" 
                                    allowfullscreen>
                                    </iframe>
                                    """, unsafe_allow_html=True)
                                else:
                                    st.info("💡 Vista previa no disponible para este video de Vimeo")
                            except Exception as e:
                                st.warning("⚠️ Error cargando vista previa de Vimeo")
                        
                        else:
                            # Para otras plataformas, mostrar información adicional
                            st.info(f"🌐 **Plataforma:** {platform}")
                            st.markdown("**💡 Vista previa no disponible**")
                            st.markdown("El video se descargará normalmente.")
                            
                            # Mostrar información adicional si está disponible
                            if video_info.get('formats'):
                                formats_count = len(video_info['formats'])
                                st.write(f"📊 **Formatos disponibles:** {formats_count}")
                            
                            if video_info.get('filesize'):
                                size_mb = video_info['filesize'] / (1024 * 1024)
                                st.write(f"💾 **Tamaño estimado:** {size_mb:.1f} MB")
                
                st.markdown('</div>', unsafe_allow_html=True)
    
    # Opciones de descarga mejoradas para múltiples plataformas
    if st.session_state.video_info:
        st.markdown("---")
        st.subheader("⚙️ Opciones de Descarga Universal")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**🎯 Calidad de Video**")
            quality = st.selectbox("Selecciona la calidad:", 
                                 ["Mejor disponible", "1080p", "720p", "480p", "360p", "Peor disponible"],
                                 help="La calidad disponible depende de la plataforma")
            
            quality_map = {
                "Mejor disponible": "best",
                "1080p": "best[height<=1080]",
                "720p": "best[height<=720]",
                "480p": "best[height<=480]",
                "360p": "best[height<=360]",
                "Peor disponible": "worst"
            }
        
        with col2:
            st.markdown("**🎵 Opciones de Audio**")
            audio_only = st.checkbox("🎵 Solo Audio (MP3)", help="Descargar únicamente el audio en formato MP3")
            if not audio_only:
                audio_quality = st.selectbox("Calidad de Audio:", ["192 kbps", "128 kbps", "96 kbps"])
            else:
                audio_quality = st.selectbox("Calidad MP3:", ["320 kbps", "192 kbps", "128 kbps"])
        
        with col3:
            st.markdown("**📝 Extras**")
            subtitles = st.checkbox("📝 Incluir Subtítulos", help="Descargar subtítulos si están disponibles")
            thumbnail = st.checkbox("🖼️ Descargar Miniatura", help="Guardar la imagen de miniatura")
            
            # Directorio de descarga
            st.markdown("**📁 Ubicación**")
            download_dir = st.text_input("Directorio:", value="downloads", help="Carpeta donde guardar los archivos")
        
        # Información adicional sobre el video
        if st.session_state.video_info:
            with st.expander("📊 Información Técnica del Video"):
                info = st.session_state.video_info
                
                col_tech1, col_tech2 = st.columns(2)
                with col_tech1:
                    st.write(f"**🎞️ Formato Original:** {info.get('ext', 'N/A')}")
                    st.write(f"**📐 Resolución:** {info.get('width', 'N/A')}x{info.get('height', 'N/A')}")
                    st.write(f"**🕐 FPS:** {info.get('fps', 'N/A')}")
                
                with col_tech2:
                    if info.get('filesize'):
                        size_mb = info['filesize'] / (1024 * 1024)
                        st.write(f"**💾 Tamaño:** {size_mb:.1f} MB")
                    st.write(f"**🎵 Audio Codec:** {info.get('acodec', 'N/A')}")
                    st.write(f"**🎬 Video Codec:** {info.get('vcodec', 'N/A')}")
        
        # Botón de descarga principal
        st.markdown("---")
        if st.button("📥 Descargar Video", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Crear directorio
                Path(download_dir).mkdir(exist_ok=True)
                status_text.text("📁 Preparando directorio de descarga...")
                progress_bar.progress(10)
                
                # Configurar yt-dlp con opciones universales
                ydl_opts = {
                    'outtmpl': f"{download_dir}/%(title)s.%(id)s.%(ext)s",
                    'format': quality_map[quality],
                    'noplaylist': True,
                    'extract_flat': False,
                    'writeinfojson': True,  # Guardar metadata
                    'restrictfilenames': True,
                }
                
                # Configurar audio
                if audio_only:
                    audio_bitrate = audio_quality.split()[0]  # Extraer número
                    ydl_opts.update({
                        'format': 'bestaudio/best',
                        'postprocessors': [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': 'mp3',
                            'preferredquality': audio_bitrate,
                        }],
                    })
                    status_text.text(f"🎵 Configurando descarga de audio {audio_bitrate}...")
                else:
                    status_text.text(f"🎬 Configurando descarga de video...")
                
                # Configurar subtítulos
                if subtitles:
                    ydl_opts.update({
                        'writesubtitles': True,
                        'writeautomaticsub': True,
                        'subtitleslangs': ['es', 'en', 'es-es', 'en-us'],
                        'skip_unavailable_fragments': False,
                    })
                    status_text.text("📝 Configurando descarga de subtítulos...")
                
                # Configurar miniatura
                if thumbnail:
                    ydl_opts.update({
                        'writethumbnail': True,
                        'postprocessors': ydl_opts.get('postprocessors', []) + [{
                            'key': 'FFmpegThumbnailsConvertor',
                            'format': 'jpg',
                        }],
                    })
                    status_text.text("🖼️ Configurando descarga de miniatura...")
                
                progress_bar.progress(20)
                
                # Hook para progreso mejorado
                def progress_hook(d):
                    if d['status'] == 'downloading':
                        percent_str = d.get('_percent_str', 'N/A')
                        speed = d.get('_speed_str', 'N/A')
                        eta = d.get('_eta_str', 'N/A')
                        status_text.text(f"📥 Descargando... {percent_str} - Velocidad: {speed} - ETA: {eta}")
                        
                        # Actualizar barra de progreso
                        if '_percent_str' in d:
                            try:
                                percent = float(d['_percent_str'].replace('%', ''))
                                progress_bar.progress(min(90, int(20 + percent * 0.7)))
                            except:
                                pass
                    
                    elif d['status'] == 'finished':
                        filename = Path(d['filename']).name
                        status_text.text(f"✅ Completado: {filename}")
                        progress_bar.progress(95)
                    
                    elif d['status'] == 'error':
                        status_text.text(f"❌ Error en descarga")
                
                ydl_opts['progress_hooks'] = [progress_hook]
                
                # Descargar con manejo de errores específicos por plataforma
                status_text.text(f"🚀 Iniciando descarga desde {platform}...")
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    # Intentar extraer información adicional
                    try:
                        info = ydl.extract_info(url, download=False)
                        if info.get('is_live'):
                            st.warning("⚠️ Este es un stream en vivo. La descarga puede fallar o ser incompleta.")
                        
                        if info.get('duration', 0) > 3600:  # Más de 1 hora
                            st.info(f"⏰ Video largo detectado ({format_duration(info['duration'])}). La descarga puede tomar tiempo.")
                        
                    except Exception as e:
                        st.warning(f"⚠️ No se pudo obtener información previa: {str(e)}")
                    
                    # Realizar descarga
                    ydl.download([url])
                
                progress_bar.progress(100)
                status_text.text("🎉 ¡Descarga completada exitosamente!")
                
                # Mostrar resumen
                st.success(f"✅ **Video descargado desde {platform}**")
                st.info(f"📁 **Ubicación:** `{download_dir}/`")
                
                if audio_only:
                    st.info(f"🎵 **Formato:** MP3 ({audio_quality})")
                else:
                    st.info(f"🎬 **Calidad:** {quality}")
                
                if subtitles:
                    st.info("📝 **Subtítulos:** Incluidos (si estaban disponibles)")
                
                if thumbnail:
                    st.info("🖼️ **Miniatura:** Descargada en formato JPG")
                
            except yt_dlp.utils.DownloadError as e:
                error_msg = str(e)
                if "not available" in error_msg.lower():
                    st.error(f"❌ **Video no disponible en {platform}**")
                    st.info("💡 Posibles causas: Video privado, eliminado, geobloqueado o URL incorrecta")
                elif "copyright" in error_msg.lower():
                    st.error("❌ **Error de derechos de autor**")
                    st.info("💡 Este video puede estar protegido por derechos de autor")
                else:
                    st.error(f"❌ **Error de descarga:** {error_msg}")
                    
            except Exception as e:
                st.error(f"❌ **Error inesperado:** {str(e)}")
                st.info("💡 Intenta con una URL diferente o verifica tu conexión a internet")

# ==================== PÁGINA: CREAR CLIPS YOUTUBE ====================
elif page == "✂️ Crear Clips YouTube":
    st.header("✂️ Crear Clips de YouTube")
    
    # Input URL para clips - mantener valor de session_state si existe
    default_url = st.session_state.get('current_clip_url', '')
    clip_url = st.text_input("🔗 URL del Video para Clip:", 
                            value=default_url,
                            placeholder="https://www.youtube.com/watch?v=...")
    
    # Guardar la URL en session_state para uso posterior
    if clip_url and clip_url.strip():
        # Si la URL cambió, limpiar información del video anterior
        if (st.session_state.get('current_clip_url') and 
            st.session_state.current_clip_url != clip_url.strip()):
            st.session_state.video_info = None
            st.session_state.downloaded_youtube_path = None
            st.session_state.downloaded_youtube_info = None
            # Resetear valores de timeline
            st.session_state.youtube_quick_start = 0
            st.session_state.youtube_quick_end = 60
            st.session_state.youtube_quick_counter += 1
        
        st.session_state.current_clip_url = clip_url.strip()
    
    # Mostrar información del video si ya está analizado
    if st.session_state.get('video_info') and st.session_state.get('current_clip_url'):
        col_status, col_reset = st.columns([3, 1])
        with col_status:
            st.success(f"✅ Video analizado: {st.session_state.video_info.get('title', 'Video de YouTube')}")
        with col_reset:
            if st.button("🔄 Nuevo Video", help="Limpiar para analizar un video diferente"):
                # Limpiar información del video anterior
                st.session_state.video_info = None
                st.session_state.current_clip_url = None
                st.session_state.downloaded_youtube_path = None
                st.session_state.downloaded_youtube_info = None
                # Resetear valores de timeline
                st.session_state.youtube_quick_start = 0
                st.session_state.youtube_quick_end = 60
                st.session_state.youtube_quick_counter += 1
                st.rerun()
    
    # Botón de análisis centrado
    if st.button("🔍 Analizar Video para Clips", use_container_width=True) and clip_url and clip_url.strip():
        with st.spinner("🔍 Obteniendo información del video..."):
            video_info = get_video_info(clip_url)
            if video_info:
                st.session_state.video_info = video_info
                st.rerun()  # Recargar para mostrar la información actualizada
    
    # Mensaje de ayuda cuando no hay video info
    if not st.session_state.get('video_info'):
        st.info("💡 Ingresa una URL y haz clic en 'Analizar' para comenzar")
    
    # Botón para descargar el video completo (centrado y simplificado)
    if st.session_state.video_info and st.session_state.current_clip_url:
        if st.button("🎬 Descargar Video Completo", type="primary", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                video_url = st.session_state.current_clip_url
                
                # Preparar directorio
                download_dir = Path("downloads")
                download_dir.mkdir(exist_ok=True)
                
                status_text.text("🔍 Preparando descarga...")
                progress_bar.progress(10)
                
                # Configurar yt-dlp para descarga completa
                ydl_opts = {
                    'format': 'best[height<=720]/best',
                    'outtmpl': str(download_dir / '%(title)s.%(ext)s'),
                    'noplaylist': True,
                    'restrictfilenames': True,
                }
                
                # Hook para progreso
                def progress_hook(d):
                    if d['status'] == 'downloading':
                        percent_str = d.get('_percent_str', 'N/A')
                        speed = d.get('_speed_str', 'N/A')
                        status_text.text(f"📥 Descargando... {percent_str} - {speed}")
                        
                        # Actualizar barra de progreso
                        if '_percent_str' in d:
                            try:
                                percent = float(d['_percent_str'].replace('%', ''))
                                progress_bar.progress(min(90, int(10 + percent * 0.8)))
                            except:
                                pass
                                
                    elif d['status'] == 'finished':
                        status_text.text(f"✅ Descarga completada: {Path(d['filename']).name}")
                        progress_bar.progress(90)
                
                ydl_opts['progress_hooks'] = [progress_hook]
                
                # Descargar video
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(video_url, download=True)
                    downloaded_file = ydl.prepare_filename(info)
                
                progress_bar.progress(100)
                status_text.text("✅ ¡Video descargado exitosamente!")
                
                # Guardar información del video descargado para uso posterior
                st.session_state.downloaded_youtube_path = downloaded_file
                st.session_state.downloaded_youtube_info = st.session_state.video_info
                
                st.success(f"✅ **Video descargado exitosamente**")
                st.info(f"📁 **Ubicación:** `{downloaded_file}`")
                st.info(f"📏 **Duración:** `{format_duration(st.session_state.video_info.get('duration', 0))}`")
                
            except Exception as e:
                st.error(f"❌ Error durante la descarga: {str(e)}")
    # Mostrar información del video si ya está disponible (siempre visible)
    if st.session_state.get('video_info') and st.session_state.get('current_clip_url'):
        st.markdown("---")
        st.markdown('<div class="video-info-card">', unsafe_allow_html=True)
        
        # Información técnica del video
        st.write(f"**📺 Título:** {st.session_state.video_info.get('title', 'Sin título')}")
        col_info1, col_info2 = st.columns(2)
        with col_info1:
            st.write(f"**👤 Canal:** {st.session_state.video_info.get('uploader', 'Desconocido')}")
            st.write(f"**⏱️ Duración:** {format_duration(st.session_state.video_info.get('duration', 0))}")
        with col_info2:
            st.write(f"**📅 Subido:** {st.session_state.video_info.get('upload_date', 'Fecha desconocida')}")
            views = st.session_state.video_info.get('view_count', 0)
            st.write(f"**👁️ Visualizaciones:** {views:,}" if views else "**👁️ Visualizaciones:** N/A")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Vista previa del video (misma estructura que videos locales)
        st.markdown("### 🎬 Vista Previa del Video")
        col_preview, col_info_preview = st.columns([2, 1])
        
        with col_preview:
            current_url = st.session_state.current_clip_url
            if 'youtube.com' in current_url or 'youtu.be' in current_url:
                import re
                youtube_regex = r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)'
                match = re.search(youtube_regex, current_url)
                if match:
                    video_id = match.group(1)
                    embed_url = f"https://www.youtube.com/embed/{video_id}"
                    
                    # Contenedor centrado para el video
                    st.markdown("""
                    <div class="video-container">
                        <iframe width="640" height="360" 
                        src="{}" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen>
                        </iframe>
                    </div>
                    """.format(embed_url), unsafe_allow_html=True)
                else:
                    st.warning("⚠️ No se pudo cargar la vista previa del video")
                    st.info("💡 Puedes continuar creando clips sin la vista previa")
            else:
                st.warning("⚠️ URL de video no válida")
        
        with col_info_preview:
            st.markdown("#### 🎮 Controles de Video")
            st.info("🎬 Usa los controles del reproductor para navegar por el video y encontrar los puntos exactos para tu clip")
            st.markdown("**💡 Consejos:**")
            st.markdown("• Pausa en el punto de inicio deseado")
            st.markdown("• Anota los tiempos exactos")
            st.markdown("• Usa los botones rápidos para clips comunes")
            st.markdown("• El video se abrirá en YouTube al hacer clic")
    
    # Timeline interactivo para clips
    if st.session_state.video_info:
        st.subheader("🎬 Timeline Interactivo")
        
        duration = st.session_state.video_info.get('duration', 300)  # Default 5 minutos
        
        # Mostrar duración total
        st.write(f"**Duración total del video:** {format_duration(duration)}")
        
        # Timeline visual con sliders
        st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
        
        # Slider para selección de rango (usando counter para reset de keys)
        col1, col2 = st.columns(2)
        
        with col1:
            start_seconds = st.slider(
                "🕐 Tiempo de Inicio (segundos):", 
                0, max(0, duration-1), st.session_state.youtube_quick_start, 1,
                key=f"youtube_start_time_{st.session_state.youtube_quick_counter}",
                help="Arrastra para seleccionar el inicio del clip"
            )
            start_time = seconds_to_time(start_seconds)
            st.write(f"**Inicio:** {start_time}")
        
        with col2:
            end_seconds = st.slider(
                "🕐 Tiempo de Fin (segundos):", 
                start_seconds+1, max(start_seconds+2, duration), max(st.session_state.youtube_quick_end, start_seconds+1), 1,
                key=f"youtube_end_time_{st.session_state.youtube_quick_counter}",
                help="Arrastra para seleccionar el fin del clip"
            )
            end_time = seconds_to_time(end_seconds)
            st.write(f"**Fin:** {end_time}")
        
        # Visualización del timeline
        timeline_progress = (end_seconds - start_seconds) / duration * 100
        st.progress(timeline_progress / 100)
        st.write(f"**📏 Duración del clip:** {format_duration(end_seconds - start_seconds)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botones rápidos
        st.subheader("⚡ Accesos Rápidos")
        quick_col1, quick_col2, quick_col3, quick_col4 = st.columns(4)
        
        with quick_col1:
            if st.button("📺 Primeros 30s", help="Clip de los primeros 30 segundos", key="youtube_quick_30s"):
                st.session_state.youtube_quick_start = 0
                st.session_state.youtube_quick_end = min(30, duration)
                st.session_state.youtube_quick_counter += 1
                st.rerun()
        with quick_col2:
            if st.button("🎵 Primer minuto", help="Clip de 1 minuto desde el inicio", key="youtube_quick_1min"):
                st.session_state.youtube_quick_start = 0
                st.session_state.youtube_quick_end = min(60, duration)
                st.session_state.youtube_quick_counter += 1
                st.rerun()
        with quick_col3:
            if st.button("📹 Primeros 2min", help="Clip de 2 minutos desde el inicio", key="youtube_quick_2min"):
                st.session_state.youtube_quick_start = 0
                st.session_state.youtube_quick_end = min(120, duration)
                st.session_state.youtube_quick_counter += 1
                st.rerun()
        with quick_col4:
            if st.button("🎬 Primeros 5min", help="Clip de 5 minutos desde el inicio", key="youtube_quick_5min"):
                st.session_state.youtube_quick_start = 0
                st.session_state.youtube_quick_end = min(300, duration)
                st.session_state.youtube_quick_counter += 1
                st.rerun()
        
        # Configuración del clip
        st.subheader("⚙️ Configuración del Clip")
        
        col1, col2 = st.columns(2)
        with col1:
            clip_name = st.text_input("📝 Nombre del Clip:", 
                                    value=f"clip_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        with col2:
            output_format = st.selectbox("🎞️ Formato de Salida:", 
                                       ["mp4", "webm", "mkv"])
        
        # Preview del clip
        st.markdown('<div class="clip-preview">', unsafe_allow_html=True)
        st.subheader("👀 Vista Previa del Clip")
        st.write(f"**📝 Nombre:** {clip_name}.{output_format}")
        st.write(f"**⏱️ Duración:** {format_duration(end_seconds - start_seconds)}")
        st.write(f"**🕐 Rango:** {start_time} → {end_time}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botones de creación
        st.subheader("🚀 Crear Clip")
        
        method_col1, method_col2 = st.columns(2)
        
        with method_col1:
            # Validar que tengamos una URL válida
            has_valid_url = st.session_state.current_clip_url and st.session_state.current_clip_url.strip()
            
            if st.button("🎬 Descargar y Crear Clip", 
                        type="primary", 
                        use_container_width=True, 
                        disabled=not has_valid_url):
                
                if not has_valid_url:
                    st.error("❌ Por favor ingresa una URL de YouTube válida primero")
                else:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        # Usar la URL guardada en session_state
                        video_url = st.session_state.current_clip_url
                        
                        # Paso 1: Descargar video temporal
                        status_text.text("📥 Descargando video temporal...")
                        progress_bar.progress(25)
                        
                        temp_dir = Path("temp_clips")
                        temp_dir.mkdir(exist_ok=True)
                        
                        ydl_opts = {
                            'format': 'best[height<=720]/best',
                            'outtmpl': str(temp_dir / f'auto_{int(time.time())}_%(id)s.%(ext)s'),
                            'noplaylist': True,
                            'restrictfilenames': True,
                        }
                        
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(video_url, download=True)
                            video_filename = ydl.prepare_filename(info)
                            temp_video_path = Path(video_filename)
                            
                            # Buscar archivo descargado
                            if not temp_video_path.exists():
                                files = list(temp_dir.glob("*"))
                                if files:
                                    temp_video_path = files[0]
                        
                        progress_bar.progress(50)
                        status_text.text("✂️ Creando clip...")
                        
                        # Paso 2: Crear clip
                        output_dir = Path("downloads")
                        output_dir.mkdir(exist_ok=True)
                        output_path = output_dir / f"{clip_name}.{output_format}"
                        
                        success, error_msg = create_clip_ffmpeg(
                            str(temp_video_path), start_time, end_time, str(output_path)
                        )
                        
                        progress_bar.progress(75)
                        
                        if success:
                            # Paso 3: Limpiar temporales
                            status_text.text("🧹 Limpiando archivos temporales...")
                            if temp_video_path.exists():
                                temp_video_path.unlink()
                            
                            progress_bar.progress(100)
                            status_text.text("✅ ¡Clip creado exitosamente!")
                            
                            st.session_state.clips_created.append({
                                'name': clip_name,
                                'path': str(output_path),
                                'duration': format_duration(end_seconds - start_seconds),
                                'source': 'youtube_clip',
                                'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                            
                            st.success(f"✅ **Clip creado exitosamente**")
                            st.info(f"📁 **Ubicación:** `{output_path}`")
                            st.info(f"⏱️ **Duración:** `{format_duration(end_seconds - start_seconds)}`")
                        else:
                            st.error(f"❌ Error creando clip: {error_msg}")
                    
                    except Exception as e:
                        st.error(f"❌ Error en proceso automático: {str(e)}")
            
            # Mostrar ayuda si no hay URL
            if not has_valid_url:
                st.info("💡 Ingresa una URL de YouTube arriba para habilitar este botón")
        
        with method_col2:
            # Verificar si hay un video descargado disponible
            has_downloaded_video = (st.session_state.downloaded_youtube_path and 
                                  Path(st.session_state.downloaded_youtube_path).exists())
            
            if st.button("✂️ Crear desde Video Descargado", 
                        use_container_width=True,
                        disabled=not has_downloaded_video):
                
                if not has_downloaded_video:
                    st.error("❌ No hay video descargado disponible. Usa el botón '🎬 Descargar Video Completo' primero")
                else:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        status_text.text("✂️ Creando clip desde video descargado...")
                        progress_bar.progress(20)
                        
                        # Usar el video ya descargado
                        downloaded_video_path = st.session_state.downloaded_youtube_path
                        
                        # Crear directorio de salida
                        output_dir = Path("downloads")
                        output_dir.mkdir(exist_ok=True)
                        output_path = output_dir / f"{clip_name}.{output_format}"
                        
                        progress_bar.progress(40)
                        status_text.text("🎞️ Procesando clip con FFmpeg...")
                        
                        # Crear clip usando FFmpeg
                        success, error_msg = create_clip_ffmpeg(
                            downloaded_video_path, start_time, end_time, str(output_path)
                        )
                        
                        progress_bar.progress(80)
                        
                        if success:
                            progress_bar.progress(100)
                            status_text.text("✅ ¡Clip creado exitosamente!")
                            
                            # Agregar a la lista de clips creados
                            st.session_state.clips_created.append({
                                'name': clip_name,
                                'path': str(output_path),
                                'duration': format_duration(end_seconds - start_seconds),
                                'source': 'youtube_downloaded',
                                'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                            
                            st.success(f"✅ **Clip creado exitosamente**")
                            st.info(f"📁 **Ubicación:** `{output_path}`")
                            st.info(f"⏱️ **Duración:** `{format_duration(end_seconds - start_seconds)}`")
                        else:
                            st.error(f"❌ Error creando clip: {error_msg}")
                    
                    except Exception as e:
                        st.error(f"❌ Error procesando clip: {str(e)}")
            
            # Mostrar estado del video descargado
            if has_downloaded_video:
                st.success("✅ Video descargado disponible")
                if st.session_state.downloaded_youtube_info:
                    st.caption(f"📺 {st.session_state.downloaded_youtube_info.get('title', 'Video descargado')}")
            else:
                st.info("💡 Descarga un video primero usando el botón de arriba")
    
    # Mostrar clips creados
    if st.session_state.clips_created:
        st.subheader("📋 Clips Creados")
        for clip in st.session_state.clips_created:
            with st.expander(f"🎬 {clip['name']}"):
                st.write(f"**📁 Ruta:** {clip['path']}")
                st.write(f"**⏱️ Duración:** {clip['duration']}")
                st.write(f"**📅 Creado:** {clip['created']}")

# ==================== PÁGINA: PROCESAR VIDEOS LOCALES ====================
elif page == "📁 Procesar Videos Locales":
    st.markdown('<div class="section-title">📁 Procesar Videos Locales</div>', unsafe_allow_html=True)
    
    st.markdown("### 📎 Seleccionar Video Local")
    # Selector de archivo con soporte para múltiples formatos
    uploaded_file = st.file_uploader(
        "Arrastra tu archivo de video o haz clic para seleccionar:",
        type=['mp4', 'avi', 'mkv', 'mov', 'wmv', 'flv', 'webm', 'm4v', 'mpg', 'mpeg', '3gp'],
        help="Formatos soportados: MP4, AVI, MKV, MOV, WMV, FLV, WEBM, M4V, MPG, MPEG, 3GP"
    )
    
    if uploaded_file is not None:
        # Guardar archivo temporal
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
            tmp.write(uploaded_file.getvalue())
            st.session_state.local_video_path = tmp.name
        
        # Mostrar información básica del archivo
        file_size_mb = uploaded_file.size / (1024*1024)
        st.success(f"✅ **Archivo cargado:** {uploaded_file.name}")
        st.info(f"� **Tamaño del archivo:** {file_size_mb:.2f} MB")
        
        # Botón para analizar el archivo
        if st.button("🔍 Obtener Información del Archivo", use_container_width=True):
            with st.spinner("🔍 Analizando archivo de video..."):
                try:
                    # Usar ffprobe para obtener información detallada
                    cmd = [
                        "ffprobe", "-v", "quiet", "-print_format", "json", 
                        "-show_format", "-show_streams", st.session_state.local_video_path
                    ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=30)
                    
                    if result.returncode == 0:
                        probe_data = json.loads(result.stdout)
                        
                        # Extraer información del formato y streams
                        format_info = probe_data.get('format', {})
                        video_stream = None
                        audio_streams = []
                        
                        # Encontrar streams de video y audio
                        for stream in probe_data.get('streams', []):
                            if stream.get('codec_type') == 'video' and not video_stream:
                                video_stream = stream
                            elif stream.get('codec_type') == 'audio':
                                audio_streams.append(stream)
                        
                        if video_stream:
                            # Calcular FPS
                            fps_str = video_stream.get('avg_frame_rate', '0/1')
                            try:
                                fps = eval(fps_str) if fps_str and '/' in fps_str else 0
                            except:
                                fps = 0
                            
                            # Crear objeto de información
                            video_info = {
                                'title': Path(uploaded_file.name).stem,
                                'duration': float(format_info.get('duration', 0)),
                                'width': video_stream.get('width', 0),
                                'height': video_stream.get('height', 0),
                                'fps': fps,
                                'codec': video_stream.get('codec_name', 'desconocido'),
                                'filesize': int(format_info.get('size', uploaded_file.size)),
                                'format': format_info.get('format_name', 'desconocido'),
                                'bitrate': int(format_info.get('bit_rate', 0)) if format_info.get('bit_rate') else 0,
                                'audio_codec': audio_streams[0].get('codec_name', 'desconocido') if audio_streams else 'N/A',
                                'audio_bitrate': int(audio_streams[0].get('bit_rate', 0)) if audio_streams and audio_streams[0].get('bit_rate') else 0
                            }
                            
                            st.session_state.local_video_info = video_info
                            
                            # Mostrar información detallada
                            st.markdown("### 📺 Información del Video")
                            st.markdown('<div class="video-info-card">', unsafe_allow_html=True)
                            
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.markdown(f"**📁 Archivo:** {video_info['title']}")
                                st.markdown(f"**⏱️ Duración:** {format_duration(int(video_info['duration']))}")
                                st.markdown(f"**🎞️ Resolución:** {video_info['width']}x{video_info['height']}")
                                st.markdown(f"**⚡ FPS:** {video_info['fps']:.2f}")
                            
                            with col2:
                                st.markdown(f"**🎬 Video Codec:** {video_info['codec']}")
                                st.markdown(f"**🎵 Audio Codec:** {video_info['audio_codec']}")
                                st.markdown(f"**📋 Formato:** {video_info['format']}")
                                st.markdown(f"**📊 Tamaño:** {video_info['filesize'] / (1024*1024):.2f} MB")
                            
                            with col3:
                                if video_info['bitrate'] > 0:
                                    st.markdown(f"**� Bitrate Total:** {video_info['bitrate']:,} bps")
                                else:
                                    st.markdown(f"**� Bitrate Total:** N/A")
                                    
                                if video_info['audio_bitrate'] > 0:
                                    st.markdown(f"**🎵 Audio Bitrate:** {video_info['audio_bitrate']:,} bps")
                                else:
                                    st.markdown(f"**🎵 Audio Bitrate:** N/A")
                                    
                                st.markdown(f"**🎯 Calidad:** {video_info['height']}p")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                        else:
                            st.error("❌ No se encontró stream de video en el archivo")
                            
                    else:
                        st.error("❌ Error analizando el archivo. Verifica que ffprobe esté instalado.")
                        st.code(result.stderr)
                        
                except subprocess.TimeoutExpired:
                    st.error("❌ Tiempo agotado analizando el archivo")
                except FileNotFoundError:
                    st.error("❌ ffprobe no encontrado. Instala FFmpeg para usar esta función.")
                except Exception as e:
                    st.error(f"❌ Error inesperado: {str(e)}")
        
        # Vista previa del video (siempre disponible)
        st.markdown("### 🎬 Vista Previa del Video")
        col_preview, col_info_preview = st.columns([2, 1])
        
        with col_preview:
            try:
                st.video(st.session_state.local_video_path)
            except Exception as e:
                st.warning(f"⚠️ No se pudo reproducir la vista previa: {str(e)}")
                st.info("💡 Puedes continuar creando clips sin la vista previa")
        
        with col_info_preview:
            st.markdown("#### 🎮 Controles de Video")
            st.info("🎬 Usa los controles del reproductor para navegar por el video y encontrar los puntos exactos para tu clip")
            st.markdown("**💡 Consejos:**")
            st.markdown("• Pausa en el punto de inicio deseado")
            st.markdown("• Anota los tiempos exactos")
            st.markdown("• Usa los botones rápidos para clips comunes")
    
    # Configuración de clips (disponible cuando hay archivo cargado)
    if st.session_state.local_video_path:
        st.markdown("---")
        st.markdown("### ✂️ Configuración del Clip")
        
        # Usar duración estimada o por defecto si no tenemos información completa
        if st.session_state.local_video_info:
            duration = int(st.session_state.local_video_info['duration'])
            st.info(f"📊 **Duración del video:** {format_duration(duration)}")
        else:
            # Intentar obtener duración básica con ffprobe
            basic_duration = get_basic_video_duration(st.session_state.local_video_path)
            if basic_duration:
                duration = int(basic_duration)
                st.info(f"📊 **Duración detectada:** {format_duration(duration)}")
            else:
                # Duración por defecto para archivos no analizados
                duration = 300  # 5 minutos por defecto
                st.warning("⚠️ **Duración estimada:** 5 minutos. Haz clic en 'Obtener Información Completa del Archivo' para obtener la duración exacta.")
        
        # Timeline interactivo
        st.markdown('<div class="timeline-container">', unsafe_allow_html=True)
        
        # Sliders para selección de tiempo (usando counter para reset de keys)
        col_start, col_end = st.columns(2)
        
        with col_start:
            local_start = st.slider(
                "🕐 Tiempo de Inicio (segundos):", 
                0, max(0, duration-1), st.session_state.local_quick_start, 1,
                key=f"local_start_time_{st.session_state.local_quick_counter}",
                help="Selecciona el segundo donde comenzará el clip"
            )
            st.markdown(f"**⏰ Inicio:** `{seconds_to_time(local_start)}`")
        
        with col_end:
            local_end = st.slider(
                "🕐 Tiempo de Fin (segundos):", 
                local_start+1, max(local_start+2, duration), max(st.session_state.local_quick_end, local_start+1), 1,
                key=f"local_end_time_{st.session_state.local_quick_counter}",
                help="Selecciona el segundo donde terminará el clip"
            )
            st.markdown(f"**⏰ Fin:** `{seconds_to_time(local_end)}`")
        
        # Información del clip
        clip_duration = local_end - local_start
        progress_value = min(1.0, max(0.0, clip_duration / duration)) if duration > 0 else 0
        st.progress(progress_value)
        st.markdown(f"**📏 Duración del clip:** `{format_duration(clip_duration)}`")
        if st.session_state.local_video_info:
            st.markdown(f"**📊 Porcentaje del video original:** `{(clip_duration/duration*100):.1f}%`")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Botones de tiempo rápido
        st.markdown("#### ⚡ Accesos Rápidos")
        col_q1, col_q2, col_q3, col_q4 = st.columns(4)
        
        with col_q1:
            if st.button("📺 Primeros 30s", help="Clip de los primeros 30 segundos", key="quick_30s"):
                st.session_state.local_quick_start = 0
                st.session_state.local_quick_end = min(30, duration)
                st.session_state.local_quick_counter += 1
                st.rerun()
        
        with col_q2:
            if st.button("🎵 1 minuto", help="Clip de 1 minuto desde el inicio", key="quick_1min"):
                st.session_state.local_quick_start = 0
                st.session_state.local_quick_end = min(60, duration)
                st.session_state.local_quick_counter += 1
                st.rerun()
        
        with col_q3:
            if st.button("📹 2 minutos", help="Clip de 2 minutos desde el inicio", key="quick_2min"):
                st.session_state.local_quick_start = 0
                st.session_state.local_quick_end = min(120, duration)
                st.session_state.local_quick_counter += 1
                st.rerun()
        
        with col_q4:
            if st.button("🎬 5 minutos", help="Clip de 5 minutos desde el inicio", key="quick_5min"):
                st.session_state.local_quick_start = 0
                st.session_state.local_quick_end = min(300, duration)
                st.session_state.local_quick_counter += 1
                st.rerun()
        
        # Configuración del archivo de salida
        st.markdown("#### 📝 Configuración de Salida")
        col_name, col_quality = st.columns([2, 1])
        
        with col_name:
            clip_name = st.text_input(
                "Nombre del clip:",
                value=f"clip_{Path(uploaded_file.name).stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}" if uploaded_file else f"clip_local_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                key="local_clip_name",
                help="Nombre del archivo de salida (sin extensión)"
            )
        
        with col_quality:
            processing_method = st.selectbox(
                "Método de procesamiento:",
                ["✂️ Clip Directo (Rápido)", "🎞️ Convertir y Crear (Calidad)"],
                help="Clip Directo: Copia sin re-codificar (rápido)\nConvertir: Re-codifica para mejor compatibilidad"
            )
        
        # Información sobre los métodos
        st.markdown('<div class="video-info-card">', unsafe_allow_html=True)
        if "Directo" in processing_method:
            st.info("**✂️ Clip Directo:** Copia los streams sin re-codificar. Es más rápido pero mantiene el formato original.")
        else:
            st.info("**🎞️ Convertir y Crear:** Re-codifica a MP4 con H.264/AAC. Es más lento pero garantiza compatibilidad.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Advertencia si no se ha analizado el video
        if not st.session_state.local_video_info:
            st.warning("⚠️ **Recomendación:** Analiza el video para obtener información precisa sobre la duración antes de crear el clip.")
        
        # Botones de acción
        st.markdown("#### 🎬 Crear Clip")
        col_create, col_clear = st.columns([3, 1])
        
        with col_create:
            if st.button("🚀 Crear Clip del Video Local", type="primary", use_container_width=True):
                if not clip_name.strip():
                    st.error("❌ Por favor ingresa un nombre para el clip")
                else:
                    # Crear clip en hilo separado simulado con progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    try:
                        status_text.text(f"⚙️ Preparando procesamiento ({processing_method})...")
                        progress_bar.progress(10)
                        time.sleep(0.5)
                        
                        # Preparar directorio de salida
                        output_dir = Path("downloads")
                        output_dir.mkdir(exist_ok=True)
                        
                        # Determinar extensión y comando según método
                        if "Directo" in processing_method:
                            # Método directo - mantener extensión original
                            if uploaded_file:
                                extension = Path(uploaded_file.name).suffix
                            else:
                                extension = ".mp4"  # Por defecto
                            output_path = output_dir / f"{clip_name}{extension}"
                            
                            # Comando ffmpeg para clip directo
                            cmd = [
                                "ffmpeg", "-y",
                                "-i", st.session_state.local_video_path,
                                "-ss", seconds_to_time(local_start),
                                "-t", str(clip_duration),
                                "-c", "copy",  # Copiar sin re-codificar
                                str(output_path)
                            ]
                        else:
                            # Método de conversión - siempre MP4
                            output_path = output_dir / f"{clip_name}.mp4"
                            
                            # Comando ffmpeg para conversión
                            cmd = [
                                "ffmpeg", "-y",
                                "-i", st.session_state.local_video_path,
                                "-ss", seconds_to_time(local_start),
                                "-t", str(clip_duration),
                                "-c:v", "libx264",  # Codec de video H.264
                                "-c:a", "aac",      # Codec de audio AAC
                                "-preset", "medium", # Preset de velocidad/calidad
                                "-crf", "23",       # Calidad constante (0-51, menor = mejor)
                                str(output_path)
                            ]
                        
                        status_text.text("⚙️ Ejecutando ffmpeg...")
                        progress_bar.progress(30)
                        
                        # Ejecutar comando
                        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
                        
                        progress_bar.progress(80)
                        
                        if result.returncode == 0:
                            # Éxito
                            progress_bar.progress(100)
                            status_text.text("✅ ¡Clip creado exitosamente!")
                            
                            st.success(f"✅ **Clip creado exitosamente**")
                            st.info(f"📁 **Ubicación:** `{output_path}`")
                            st.info(f"⏱️ **Duración:** `{format_duration(clip_duration)}`")
                            
                            # Agregar a la lista de clips creados
                            st.session_state.clips_created.append({
                                'name': clip_name,
                                'path': str(output_path),
                                'duration': format_duration(clip_duration),
                                'source': 'video_local',
                                'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            })
                            
                            # Mostrar información del archivo creado
                            if output_path.exists():
                                file_size = output_path.stat().st_size / (1024*1024)
                                st.info(f"📊 **Tamaño del clip:** `{file_size:.2f} MB`")
                        
                        else:
                            # Error en ffmpeg
                            st.error("❌ Error creando el clip")
                            st.code(result.stderr)
                            
                    except FileNotFoundError:
                        st.error("❌ **ffmpeg no encontrado**. Asegúrate de que esté instalado y en el PATH.")
                        st.info("💡 Instala FFmpeg desde: https://ffmpeg.org/download.html")
                    except Exception as e:
                        st.error(f"❌ **Error inesperado:** {str(e)}")
        
        with col_clear:
            if st.button("🗑️ Limpiar", help="Limpiar selección actual", use_container_width=True):
                # Limpiar archivos temporales
                if st.session_state.local_video_path and os.path.exists(st.session_state.local_video_path):
                    try:
                        os.unlink(st.session_state.local_video_path)
                    except:
                        pass
                
                # Resetear variables
                st.session_state.local_video_path = None
                st.session_state.local_video_info = None
                st.session_state.local_basic_duration = None
                st.success("🗑️ Selección limpiada. Recarga la página para empezar de nuevo.")
    
    else:
        # Instrucciones cuando no hay archivo
        st.markdown("### 📋 Instrucciones")
        st.info("""
        **Para procesar videos locales:**
        
        1. 📎 **Selecciona un archivo** usando el botón de arriba o arrastrándolo
        2. 🎬 **Los controles aparecerán automáticamente** una vez cargado el archivo
        3. 🔍 **Opcional:** Analiza el video para obtener información detallada
        4. ⚙️ **Configura el clip** usando el timeline interactivo
        5. ✂️ **Crea tu clip** eligiendo el método de procesamiento
        """)
        
        st.markdown("#### 🎯 Formatos Soportados")
        st.markdown("""
        - **Video:** MP4, AVI, MKV, MOV, WMV, FLV, WEBM, M4V
        - **Otros:** MPG, MPEG, 3GP
        """)
        
        st.markdown("#### 🔧 Métodos de Procesamiento")
        col_method1, col_method2 = st.columns(2)
        
        with col_method1:
            st.markdown("""
            **✂️ Clip Directo (Rápido)**
            - ⚡ Procesamiento ultrarrápido
            - 📁 Mantiene formato original
            - 💾 No pierde calidad
            - ⭐ Recomendado para la mayoría de casos
            """)
        
        with col_method2:
            st.markdown("""
            **🎞️ Convertir y Crear (Calidad)**
            - 🔄 Re-codifica a MP4 H.264/AAC
            - 🌐 Máxima compatibilidad
            - ⚙️ Control de calidad personalizado
            - 📱 Ideal para compartir en redes sociales
            """)

# ==================== PÁGINA: INFORMACIÓN ====================
elif page == "ℹ️ Información":
    st.header("ℹ️ Información de la Aplicación")
    
    # Información de la app
    st.markdown("""
    ### 🎬 YouTube Downloader Pro - Streamlit Edition
    
    **📅 Versión:** 2.0 (Streamlit)  
    **🗓️ Fecha:** Julio 2025  
    **⚡ Tecnología:** Python + Streamlit + FFmpeg + yt-dlp  
    
    #### ✨ Características Principales:
    - 📥 **Descarga de videos** en múltiples calidades
    - ✂️ **Timeline interactivo** para crear clips precisos
    - 📁 **Procesamiento de videos locales** con drag & drop
    - 🎬 **Vista previa visual** de clips antes de crear
    - 🚀 **Interfaz moderna** y responsive
    - 💾 **Cache inteligente** para mejor rendimiento
    
    #### 🔧 Mejoras vs Versión Tkinter:
    - ✅ Interfaz web moderna y atractiva
    - ✅ Timeline visual para selección de clips
    - ✅ Drag & drop para archivos locales
    - ✅ Vista previa de clips en tiempo real
    - ✅ Mejor experiencia de usuario
    - ✅ Responsive design
    
    ---
    
    #### 📋 Historial de Clips Creados:
    """)
    
    if st.session_state.clips_created:
        for i, clip in enumerate(st.session_state.clips_created, 1):
            st.write(f"**{i}.** {clip['name']} - {clip['duration']} - {clip['created']}")
    else:
        st.info("🎬 No has creado clips aún. ¡Prueba las otras pestañas!")
    
    # Enlaces útiles
    st.markdown("---")
    st.subheader("🔗 Enlaces Útiles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📺 YouTube"):
            st.markdown("[YouTube](https://youtube.com)")
    
    with col2:
        if st.button("📖 yt-dlp Docs"):
            st.markdown("[yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp)")
    
    with col3:
        if st.button("🎞️ FFmpeg Docs"):
            st.markdown("[FFmpeg](https://ffmpeg.org/)")
    
    # Estadísticas
    st.markdown("---")
    st.subheader("📊 Estadísticas de Uso")
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        st.metric("🎬 Clips Creados", len(st.session_state.clips_created))
    
    with metric_col2:
        total_duration = sum([
            time_to_seconds(clip.get('duration', '00:00:00')) 
            for clip in st.session_state.clips_created
        ])
        st.metric("⏱️ Duración Total", format_duration(total_duration))
    
    with metric_col3:
        st.metric("📁 Videos Procesados", 
                 len(set(clip['path'] for clip in st.session_state.clips_created)))

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 1rem;'>
        🎬 <strong>YouTube Downloader Pro</strong> | Creado con ❤️ usando Streamlit<br>
        ⚡ Interfaz moderna para gestión de videos y clips
    </div>
    """, 
    unsafe_allow_html=True
)
