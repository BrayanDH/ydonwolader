# 🎬 YouTube Downloader Pro - YTWorker v2.0+

Una aplicación web moderna y potente para descargar videos de YouTube y crear clips personalizados con un **timeline visual interactivo**. Diseñada para ofrecer la mejor experiencia de usuario con un rendimiento excepcional.

## 🌟 Características Principales

### 🚀 **Interfaz Web Moderna (Streamlit)**
- 🎨 **Diseño Moderno**: Interfaz limpia, responsive y atractiva visualmente.
- 📊 **Timeline Visual Interactivo**: Selección precisa de clips mediante sliders dinámicos.
- 🎬 **Vista Previa en Tiempo Real**: Visualiza la duración y el rango seleccionado antes de procesar.
- 📁 **Soporte de Archivos Locales**: Sube tus propios videos (Drag & Drop) para crear clips sin conexión.
- 💾 **Cache Inteligente**: Optimización de descargas para evitar redundancia y mejorar la velocidad.
- ⚡ **Accesos Rápidos**: Botones preconfigurados para clips de 30s, 1min, 2min y 5min.

## 🚀 Instalación y Ejecución

### Requisitos Previos
- **Python 3.8+**
- **FFmpeg** (requerido para el procesamiento de clips)

### 🛠️ Configuración Rápida

1. **Clona el repositorio:**
   ```bash
   git clone <repository-url>
   cd ytworker
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Instala FFmpeg (si no lo tienes):**
   - **Windows (vía winget):** `winget install --id=Gyan.FFmpeg -e`
   - **O usa el instalador incluido:** Ejecuta `install_ffmpeg.bat`

### 🏃 Ejecución

Tienes dos formas de iniciar la aplicación:

**Opción 1: Launcher Pro (Recomendado)**
Simplemente ejecuta el launcher que gestiona el servidor y abre el navegador automáticamente:
```bash
python ytworker_launcher.py
```
*O haz doble clic en `Iniciar_YTWorker_Pro.bat`*

**Opción 2: Streamlit Directo**
```bash
streamlit run streamlit_app.py
```

## ✂️ Guía de Uso: Creador de Clips

### 1. Clips desde YouTube
- Pega la URL del video y presiona **"Obtener Información"**.
- Usa el **Timeline** para seleccionar el rango exacto mediante los sliders.
- Presiona **"Descargar y Crear Clip"**. El sistema se encarga de todo de forma automática.

### 2. Procesamiento de Videos Locales
- Arrastra tu video al área de carga en la pestaña de **"Videos Locales"**.
- El sistema analizará el archivo (resolución, codec, duración).
- Define tu rango en el timeline y crea el clip instantáneamente.

## 📁 Estructura del Proyecto

```
ytworker/
├── streamlit_app.py        # Aplicación principal (Streamlit)
├── ytworker_launcher.py   # Launcher automático inteligente
├── Iniciar_YTWorker_Pro.bat # Atajo de inicio rápido
├── requirements.txt       # Dependencias del proyecto
├── install_ffmpeg.bat     # Instalador automatizado de FFmpeg
├── downloads/             # Carpeta de destino para descargas
└── temp_clips/           # Carpeta temporal de procesamiento
```

## 🛠️ Solución de Problemas

- **FFmpeg no encontrado**: Asegúrate de haber reiniciado tu terminal después de la instalación. Puedes verificarlo ejecutando `ffmpeg -version` en la consola.
- **Error de dependencias**: Recomendamos usar un entorno virtual (`python -m venv venv`).
- **Puerto 8501 ocupado**: Streamlit usa este puerto por defecto. El launcher detectará si ya está corriendo y te redirigirá.

---

**¡Disfruta de la mejor herramienta para creación de clips! 🚀**
