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

# --- Sidebar Navigation ---
with st.sidebar:
    st.markdown('<h2 style="text-align: center; color: #4ECDC4; margin-bottom: 0;">🎬 YTWorker Pro</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #718096; font-size: 0.8rem; margin-bottom: 1rem;">Video Editor Style Interface</p>', unsafe_allow_html=True)
    
    # Navegación compacta en el sidebar
    page = st.radio(
        "Navegación",
        ["📥 Descargar Videos", "✂️ Crear Clips YouTube", "📁 Procesar Videos Locales", "ℹ️ Información"],
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

# ============# ==================== PÁGINA: DESCARGAR VIDEOS ====================
if page == "📥 Descargar Videos":
    col_d1, col_d2 = st.columns([1, 1], gap="medium")
    
    with col_d1:
        st.markdown("### 🔗 Proyecto de Descarga")
        url = st.text_input("URL del Video (YT, TikTok, IG, etc):", placeholder="https://...")
        
        if url:
            platform = "Universal"
            if 'youtube' in url or 'youtu.be' in url: platform = "YouTube"
            elif 'tiktok' in url: platform = "TikTok"
            elif 'instagram' in url: platform = "Instagram"
            st.caption(f"🌐 Plataforma: **{platform}**")
        
        if st.button("🔍 Analizar Video", use_container_width=True, type="primary") and url:
            with st.spinner("Analizando..."):
                st.session_state.video_info = get_video_info(url)
        
        if st.session_state.get('video_info'):
            info = st.session_state.video_info
            st.markdown(f"**🎬 {info.get('title', 'Video')[:60]}...**")
            st.caption(f"👤 {info.get('uploader', 'N/A')} • ⏱️ {format_duration(info.get('duration', 0))}")
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
elif page == "✂️ Crear Clips YouTube":
    col_editor, col_controls = st.columns([2, 1], gap="medium")
    
    with col_controls:
        st.markdown("### 🛠️ Editor YouTube")
        clip_url = st.text_input("🔗 URL de YouTube:", value=st.session_state.get('current_clip_url', ''))
        
        if clip_url and clip_url.strip() != st.session_state.get('current_clip_url'):
            st.session_state.current_clip_url = clip_url.strip()
            st.session_state.video_info = None

        c1, c2 = st.columns(2)
        with c1:
            if st.button("🔍 Cargar", use_container_width=True, type="primary"):
                with st.spinner("Leyendo..."):
                    info = get_video_info(st.session_state.current_clip_url)
                    if info: st.session_state.video_info = info; st.rerun()
        with c2:
            if st.button("🗑️ Reset", use_container_width=True):
                st.session_state.video_info = None; st.rerun()

        if st.session_state.video_info:
            st.markdown("---")
            st.markdown("#### ⚙️ Ajustes")
            clip_name = st.text_input("Nombre del Clip:", value=f"clip_{datetime.now().strftime('%m%d_%H%M')}")
            output_format = st.selectbox("Formato:", ["mp4", "webm", "mkv"])
            if st.button("🎬 GENERAR CLIP", use_container_width=True, type="primary"):
                st.session_state.trigger_yt_clip = True

    with col_editor:
        if st.session_state.video_info:
            info = st.session_state.video_info
            st.markdown(f"#### 📺 {info.get('title', 'Video')[:70]}...")
            
            # Embed
            import re
            m = re.search(r'(?:youtube\.com\/watch\?v=|youtu\.be\/)([^&\n?#]+)', st.session_state.current_clip_url)
            if m:
                st.markdown(f'<div class="video-container"><iframe width="100%" height="380" src="https://www.youtube.com/embed/{m.group(1)}" frameborder="0" allowfullscreen></iframe></div>', unsafe_allow_html=True)

            # Timeline
            duration = info.get('duration', 0)
            st.markdown(f"**⏱️ Timeline** ({format_duration(duration)})")
            t1, t2 = st.columns(2)
            with t1: start_s = st.slider("In:", 0, int(duration)-1, st.session_state.youtube_quick_start, key="yt_s")
            with t2: end_s = st.slider("Out:", start_s+1, int(duration), max(st.session_state.youtube_quick_end, start_s+1), key="yt_e")
            
            st.caption(f"📐 Clip: **{seconds_to_time(start_s)}** ➔ **{seconds_to_time(end_s)}** ({format_duration(end_s - start_s)})")
            
            if st.session_state.get('trigger_yt_clip'):
                st.session_state.trigger_yt_clip = False
                with st.spinner("Descargando y Cortando..."):
                    try:
                        temp_dir = Path("temp_clips"); temp_dir.mkdir(exist_ok=True)
                        tmp_out = str(temp_dir / f"tmp_{int(time.time())}.mp4")
                        ydl_opts = {'format': 'bestvideo[height<=720]+bestaudio/best[height<=720]', 'outtmpl': tmp_out, 'restrictfilenames': True}
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([st.session_state.current_clip_url])
                        
                        out_dir = Path(download_dir); out_dir.mkdir(exist_ok=True)
                        out_p = out_dir / f"{clip_name}.{output_format}"
                        success, err = create_clip_ffmpeg(tmp_out, seconds_to_time(start_s), seconds_to_time(end_s), str(out_p))
                        if success:
                            st.success(f"✅ Clip guardado en {download_dir}/")
                            st.session_state.clips_created.append({'name': clip_name, 'duration': format_duration(end_s-start_s), 'path': str(out_p)})
                            if os.path.exists(tmp_out): os.remove(tmp_out)
                        else: st.error(err)
                    except Exception as e: st.error(str(e))
        else:
            st.info("👈 Ingresa una URL de YouTube a la derecha para comenzar.")

# ==================== PÁGINA: PROCESAR VIDEOS LOCALES ====================
elif page == "📁 Procesar Videos Locales":
    col_l1, col_l2 = st.columns([1, 2], gap="medium")
    
    with col_l1:
        st.markdown("### 📁 Archivo Local")
        uploaded_file = st.file_uploader("Seleccionar video:", type=['mp4', 'mkv', 'mov', 'avi', 'webm'])
        
        if uploaded_file:
            if not st.session_state.get('local_video_path') or st.session_state.get('local_filename') != uploaded_file.name:
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp:
                    tmp.write(uploaded_file.getvalue())
                    st.session_state.local_video_path = tmp.name
                    st.session_state.local_filename = uploaded_file.name
                    st.session_state.local_video_info = None
            
            st.success(f"✅ {uploaded_file.name}")
            if st.button("🔍 Analizar Video", use_container_width=True, type="primary"):
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
            if st.button("✂️ PROCESAR CLIP", use_container_width=True, type="primary"):
                st.session_state.trigger_local_clip = True

    with col_l2:
        if st.session_state.get('local_video_path'):
            st.video(st.session_state.local_video_path)
            if st.session_state.get('local_video_info'):
                info = st.session_state.local_video_info
                dur = info['duration']
                st.markdown(f"**⏱️ Timeline** ({format_duration(dur)})")
                ls = st.slider("Inicio:", 0, int(dur)-1, 0, key="lc_s")
                le = st.slider("Fin:", ls+1, int(dur), int(dur), key="lc_e")
                
                if st.session_state.get('trigger_local_clip'):
                    st.session_state.trigger_local_clip = False
                    with st.spinner("Cortando..."):
                        out_dir = Path(download_dir); out_dir.mkdir(exist_ok=True)
                        out_p = out_dir / f"{l_clip_name}.mp4"
                        success, err = create_clip_ffmpeg(st.session_state.local_video_path, seconds_to_time(ls), seconds_to_time(le), str(out_p))
                        if success:
                            st.success(f"✅ Clip guardado: {out_p.name}")
                            st.session_state.clips_created.append({'name': l_clip_name, 'duration': format_duration(le-ls), 'path': str(out_p)})
                        else: st.error(err)
        else:
            st.info("👈 Sube un video local para comenzar.")

# ==================== PÁGINA: INFORMACIÓN ====================
elif page == "ℹ️ Información":
    st.header("ℹ️ Información")
    st.markdown("""
    ### 🎬 YTWorker Pro - Video Editor Mode
    Interfaz profesional para gestión de videos y creación de clips.
    - **Descargar:** Obtén videos de YouTube, TikTok, IG, etc.
    - **Creator:** Recorta clips específicos de YouTube con timeline visual.
    - **Local:** Procesa tus propios archivos de video.
    """)
    if st.session_state.get('clips_created'):
        st.subheader("📋 Clips Recientes")
        for clip in st.session_state.clips_created:
            st.write(f"- {clip['name']} ({clip['duration']})")

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #718096;'>🎬 <strong>YTWorker Pro</strong> | Editor Pro Mode 2.0</div>", unsafe_allow_html=True)
