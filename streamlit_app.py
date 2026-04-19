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
from datetime import datetime, time as dt_time, timedelta
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
    /* Filmora Dark Theme Core */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #0F0F13 !important;
        font-family: 'Inter', sans-serif;
        color: #E0E0E6;
    }

    [data-testid="stHeader"] {
        background-color: #0F0F13 !important;
    }

    [data-testid="stSidebar"] {
        background-color: #17171C !important;
        border-right: 1px solid #2D2D35;
    }

    /* Filmora Cards & Panels */
    .video-info-card, .timeline-container, .clip-preview {
        background-color: #1B1B22 !important;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #2D2D35;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    .video-info-card {
        border-left: 4px solid #28D8A1 !important;
    }

    /* Filmora Teal Buttons */
    .stButton > button {
        width: 100%;
        background-color: #2D2D35 !important;
        color: #E0E0E6 !important;
        border: 1px solid #3F3F48 !important;
        border-radius: 4px !important;
        padding: 0.6rem 1rem;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    /* Primary 'Export' Style Button in Filmora */
    div.stButton > button[kind="primary"] {
        background: #28D8A1 !important;
        color: #0F0F13 !important;
        border: none !important;
        box-shadow: 0 0 10px rgba(40, 216, 161, 0.2);
    }

    div.stButton > button[kind="primary"]:hover {
        background: #34E5AF !important;
        box-shadow: 0 0 15px rgba(40, 216, 161, 0.4);
    }
    
    .stButton > button:hover {
        border-color: #28D8A1 !important;
        background-color: #25252C !important;
    }

    /* Custom Inputs */
    .stTextInput > div > div > input, .stSelectbox > div > div > select {
        background-color: #111116 !important;
        color: #E0E0E6 !important;
        border: 1px solid #2D2D35 !important;
        border-radius: 4px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #28D8A1 !important;
        box-shadow: 0 0 0 1px #28D8A1 !important;
    }

    /* Filmora Slider Styling */
    .stSlider > div > div > div > div {
        background: #28D8A1 !important;
    }
    
    /* Video Container Filmora Style */
    .video-container {
        background: #000000;
        border: 1px solid #2D2D35;
        border-radius: 8px;
        padding: 4px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }

    /* Safe top spacing to avoid cutting off content */
    .block-container {
        padding-top: 4rem !important;
        padding-bottom: 0rem !important;
    }

    /* Hide redundant Streamlit UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
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
    st.session_state.current_clip_url = ""
# Video descargado de YouTube para clips
if 'downloaded_youtube_path' not in st.session_state:
    st.session_state.downloaded_youtube_path = None
if 'downloaded_youtube_info' not in st.session_state:
    st.session_state.downloaded_youtube_info = None

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown('<div style="color: #28D8A1; font-weight: bold; font-size: 1.8rem; margin-bottom: 1rem;">YTWorker Pro</div>', unsafe_allow_html=True)
    st.markdown("### Navegación")
    
    # Navegación compacta en el sidebar
    page = st.radio(
        "Navegación",
        ["Descargar Videos", "Crear Clips YouTube", "Procesar Videos Locales", "Información"],
        label_visibility="collapsed"
    )
    
    st.session_state.active_page = page
    
    st.markdown("---")
    st.markdown("### 📁 Configuración")
    download_dir = st.text_input("Directorio de descarga:", value="downloads", help="Donde se guardarán los archivos")
    
    # Mostrar clips creados en el sidebar (compacto)
    if st.session_state.clips_created:
        st.markdown("---")
        st.markdown("### 📋 Clips Recientes")
        for clip in st.session_state.clips_created[-5:]:
            st.caption(f"🎬 {clip['name']} ({clip['duration']})")

# Mantener la lógica de la página activa
page = st.session_state.active_page

# ==================== PÁGINA: DESCARGAR VIDEOS ====================
if page == "Descargar Videos":
    col_d1, col_d2 = st.columns([1, 1], gap="medium")
    
    with col_d1:
        st.markdown("### Proyecto de Descarga")
        url = st.text_input("URL del Video (YT, TikTok, IG, etc):", placeholder="https://...")
        
        if url:
            platform = "Universal"
            if 'youtube' in url or 'youtu.be' in url: platform = "YouTube"
            elif 'tiktok' in url: platform = "TikTok"
            elif 'instagram' in url: platform = "Instagram"
            st.caption(f"Plataforma: **{platform}**")
        
        if st.button("Analizar Video", use_container_width=True, type="primary") and url:
            with st.spinner("Analizando..."):
                st.session_state.video_info = get_video_info(url)
        
        if st.session_state.get('video_info'):
            info = st.session_state.video_info
            st.markdown(f"**{info.get('title', 'Video')[:60]}...**")
            st.caption(f"{info.get('uploader', 'N/A')} • {format_duration(info.get('duration', 0))}")
            if info.get('thumbnail'):
                st.image(info['thumbnail'], width=280)

    with col_d2:
        st.markdown("### ⚙️ Configuración")
        quality = st.selectbox("Calidad:", ["1080p", "720p", "480p", "best", "worst"])
        audio_only = st.checkbox("🎵 Solo Audio (MP3)")
        
        if st.button("🚀 INICIAR DESCARGA", use_container_width=True, type="primary") and url:
            status_text = st.empty()
            try:
                q_fmt = f"best[height<={quality[:-1]}]" if 'p' in quality else quality
                if audio_only: q_fmt = "bestaudio/best"
                
                download_path = Path(download_dir)
                download_path.mkdir(exist_ok=True)
                
                ydl_opts = {
                    'format': q_fmt,
                    'outtmpl': f'{download_dir}/%(title)s.%(ext)s',
                    'restrictfilenames': True,
                    'noplaylist': True,
                    'progress_hooks': [lambda d: status_text.text(f"📥 {d.get('_percent_str', 'Descargando...')}")]
                }
                if audio_only:
                    ydl_opts['postprocessors'] = [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192'}]
                
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                st.success("✅ Completado")
            except Exception as e: st.error(str(e))

# ==================== PÁGINA: CREAR CLIPS YOUTUBE ====================
elif page == "Crear Clips YouTube":
    col_editor, col_controls = st.columns([2, 1], gap="medium")
    
    with col_controls:
        st.markdown("### Editor YouTube")
        clip_url = st.text_input("URL de YouTube:", value=st.session_state.get('current_clip_url', ''))
        
        if clip_url and clip_url.strip() != st.session_state.get('current_clip_url'):
            st.session_state.current_clip_url = clip_url.strip()
            st.session_state.video_info = None

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Analizar", use_container_width=True, type="primary"):
                with st.spinner("Leyendo..."):
                    info = get_video_info(st.session_state.current_clip_url)
                    if info: st.session_state.video_info = info; st.rerun()
        with c2:
            if st.button("Reset", use_container_width=True):
                st.session_state.video_info = None; st.session_state.current_clip_url = ""; st.rerun()

        if st.session_state.video_info:
            st.markdown("---")
            st.markdown("#### Ajustes")
            clip_name = st.text_input("Nombre del Clip:", value=f"clip_{datetime.now().strftime('%m%d_%H%M')}")
            output_format = st.selectbox("Formato:", ["mp4", "webm", "mkv"])
            if st.button("GENERAR CLIP", use_container_width=True, type="primary"):
                st.session_state.trigger_yt_clip = True

    with col_editor:
        if st.session_state.video_info:
            info = st.session_state.video_info
            st.markdown(f"#### Video: {info.get('title', 'Video')[:70]}...")
            
            # Embed
            import re
            m = None
            if st.session_state.current_clip_url:
                m = re.search(r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)', st.session_state.current_clip_url)
            
            if m:
                st.markdown(f'<div class="video-container"><iframe width="100%" height="380" src="https://www.youtube.com/embed/{m.group(1)}" frameborder="0" allowfullscreen></iframe></div>', unsafe_allow_html=True)

            # Timeline
            duration = int(info.get('duration', 0))
            st.markdown(f"**Timeline** ({format_duration(duration)})")
            
            # Formatear el slider con tiempo real
            start_dt = dt_time(int(st.session_state.youtube_quick_start // 3600), int((st.session_state.youtube_quick_start % 3600) // 60), int(st.session_state.youtube_quick_start % 60))
            end_val = min(st.session_state.youtube_quick_end, duration)
            end_dt = dt_time(int(end_val // 3600), int((end_val % 3600) // 60), int(end_val % 60))
            
            max_dt = dt_time(int(duration // 3600), int((duration % 3600) // 60), int(duration % 60))
            
            # Slider de rango profesional
            time_range = st.slider(
                "Rango del Clip:",
                min_value=dt_time(0,0,0),
                max_value=max_dt,
                value=(start_dt, end_dt),
                format="HH:mm:ss",
                step=timedelta(seconds=1)
            )
            
            start_s = time_range[0].hour * 3600 + time_range[0].minute * 60 + time_range[0].second
            end_s = time_range[1].hour * 3600 + time_range[1].minute * 60 + time_range[1].second
            
            st.caption(f"Selección: **{seconds_to_time(start_s)}** ➔ **{seconds_to_time(end_s)}** ({format_duration(end_s - start_s)})")
            
            if st.session_state.get('trigger_yt_clip'):
                st.session_state.trigger_yt_clip = False
                with st.spinner("Descargando y Cortando..."):
                    try:
                        temp_dir = Path("temp_clips"); temp_dir.mkdir(exist_ok=True)
                        # Usar plantilla sin extensión fija para que yt-dlp maneje el formato final
                        outtmpl = str(temp_dir / f"tmp_{int(time.time())}.%(ext)s")
                        ydl_opts = {
                            'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]',
                            'outtmpl': outtmpl,
                            'restrictfilenames': True
                        }
                        
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(st.session_state.current_clip_url, download=True)
                            downloaded_path = ydl.prepare_filename(info)
                        
                        if os.path.exists(downloaded_path):
                            out_dir = Path(download_dir); out_dir.mkdir(exist_ok=True)
                            out_p = out_dir / f"{clip_name}.{output_format}"
                            success, err = create_clip_ffmpeg(downloaded_path, seconds_to_time(start_s), seconds_to_time(end_s), str(out_p))
                            if success:
                                st.success(f"✅ Clip guardado en {download_dir}/")
                                st.session_state.clips_created.append({'name': clip_name, 'duration': format_duration(end_s-start_s), 'path': str(out_p)})
                                if os.path.exists(downloaded_path): os.remove(downloaded_path)
                            else: st.error(err)
                        else:
                            st.error("❌ No se encontró el archivo descargado.")
                    except Exception as e: st.error(str(e))
        else:
            st.info("👈 Ingresa una URL de YouTube a la derecha para comenzar.")

# ==================== PÁGINA: PROCESAR VIDEOS LOCALES ====================
elif page == "Procesar Videos Locales":
    col_l1, col_l2 = st.columns([1, 2], gap="medium")
    
    with col_l1:
        st.markdown("### Archivo Local")
        uploaded_file = st.file_uploader("Seleccionar video:", type=['mp4', 'mkv', 'mov', 'avi', 'webm'])
        
        if uploaded_file:
            if not st.session_state.get('local_video_path') or st.session_state.get('local_filename') != uploaded_file.name:
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    st.session_state.local_video_path = tmp.name
                    st.session_state.local_filename = uploaded_file.name
                    st.session_state.local_video_info = None
            
            st.success(f"{uploaded_file.name}")
            if st.button("Analizar Video", use_container_width=True, type="primary"):
                with st.spinner("Analizando..."):
                    cmd = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", st.session_state.local_video_path]
                    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
                    if res.returncode == 0:
                        data = json.loads(res.stdout)
                        st.session_state.local_video_info = {
                            'duration': float(data['format']['duration']),
                            'width': data['streams'][0].get('width', 0),
                            'height': data['streams'][0].get('height', 0)
                        }
                    else: st.error("Error al analizar")

        if st.session_state.get('local_video_info'):
            st.markdown("---")
            l_clip_name = st.text_input("Nombre:", value=f"edit_{datetime.now().strftime('%H%M')}")
            if st.button("PROCESAR CLIP", use_container_width=True, type="primary"):
                st.session_state.trigger_local_clip = True

    with col_l2:
        if st.session_state.get('local_video_path'):
            st.video(st.session_state.local_video_path)
            if st.session_state.get('local_video_info'):
                info = st.session_state.local_video_info
                dur = int(info['duration'])
                st.markdown(f"**Timeline** ({format_duration(dur)})")
                
                max_dt = dt_time(int(dur // 3600), int((dur % 3600) // 60), int(dur % 60))
                
                # Slider de rango para video local
                l_range = st.slider(
                    "Selección de Tiempo:",
                    min_value=dt_time(0,0,0),
                    max_value=max_dt,
                    value=(dt_time(0,0,0), max_dt),
                    format="HH:mm:ss",
                    step=timedelta(seconds=1)
                )
                
                ls = l_range[0].hour * 3600 + l_range[0].minute * 60 + l_range[0].second
                le = l_range[1].hour * 3600 + l_range[1].minute * 60 + l_range[1].second
                
                if st.session_state.get('trigger_local_clip'):
                    st.session_state.trigger_local_clip = False
                    with st.spinner("Cortando..."):
                        out_dir = Path(download_dir); out_dir.mkdir(exist_ok=True)
                        out_p = out_dir / f"{l_clip_name}.mp4"
                        success, err = create_clip_ffmpeg(st.session_state.local_video_path, seconds_to_time(ls), seconds_to_time(le), str(out_p))
                        if success:
                            st.success(f"Clip guardado: {out_p.name}")
                            st.session_state.clips_created.append({'name': l_clip_name, 'duration': format_duration(le-ls), 'path': str(out_p)})
                        else: st.error(err)
        else:
            st.info("Sube un video local para comenzar.")

# ==================== PÁGINA: INFORMACIÓN ====================
elif page == "Información":
    st.header("Información")
    st.markdown("""
    ### YTWorker Pro - Video Editor System
    Interfaz profesional para gestión de videos y creación de clips.
    - **Descargar:** Obtén videos de YouTube, TikTok, IG, etc.
    - **Creator:** Recorta clips específicos de YouTube con timeline visual.
    - **Local:** Procesa tus propios archivos de video.
    """)
    if st.session_state.get('clips_created'):
        st.subheader("Clips Recientes")
        for clip in st.session_state.clips_created:
            st.write(f"- {clip['name']} ({clip['duration']})")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #718096;'>🎬 <strong>YTWorker Pro</strong> | Editor Pro Mode 2.0</div>", unsafe_allow_html=True)
