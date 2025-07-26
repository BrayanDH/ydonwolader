# 🎬 YouTube Downloader Pro

Una aplicación moderna para descargar videos de YouTube y crear clips personalizados con **timeline visual interactivo**. Ahora disponible en **dos versiones**: interfaz web moderna (Streamlit) y aplicación de escritorio clásica (Tkinter).

## 🌟 ¿Qué hay de nuevo en la v2.0?

### 🚀 **Interfaz Streamlit (RECOMENDADA)**
- 🎨 **Interfaz web moderna** y responsive
- 📊 **Timeline visual interactivo** para seleccionar clips
- 🎬 **Vista previa en tiempo real** de los clips
- 📁 **Drag & drop** para archivos locales
- 💾 **Cache inteligente** para mejor rendimiento
- 📱 **Diseño responsive** que funciona en cualquier dispositivo

### 🖥️ **Interfaz Tkinter (Legacy)**
- ✅ Mantiene toda la funcionalidad original
- ⚡ Para usuarios que prefieren aplicaciones de escritorio tradicionales

## 🚀 Instalación y Ejecución

### Método 1: Launcher Automático (Recomendado)

1. **Clona el repositorio:**
   ```bash
   git clone <repository-url>
   cd ytworker
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta el launcher:**
   ```bash
   python launcher.py
   ```

4. **Selecciona tu interfaz preferida:**
   - 🌟 **Streamlit** (moderna, timeline visual)
   - 🖥️ **Tkinter** (clásica, familiar)

### Método 2: Ejecución Directa

**Para Streamlit (Recomendado):**
```bash
streamlit run streamlit_app.py
```

**Para Tkinter:**
```bash
python youtube_downloader_gui.py
```

## ✨ Características

### 🎬 **Streamlit App (v2.0)**
- 📊 **Timeline Visual**: Arrastra sliders para seleccionar clips con precisión
- 🎯 **Vista previa instantánea**: Ve la duración y rango antes de crear
- 📁 **Drag & Drop**: Arrastra videos locales directamente
- 🎨 **Interfaz moderna**: Colores, gradientes y animaciones
- 📱 **Responsive**: Funciona en escritorio, tablet y móvil
- ⚡ **Accesos rápidos**: Botones para 30s, 1min, 2min, 5min
- 📋 **Historial de clips**: Rastrea todos los clips creados

### 🖥️ **Tkinter App (Legacy)**
- 📥 **Descarga de videos** en múltiples calidades
- 🎵 **Extracción de audio** a formato MP3
- 📝 **Descarga de subtítulos** automáticos
- ✂️ **Dos métodos de clips**: Rápido y automático
- 📁 **Videos locales**: Procesa archivos desde tu PC
- 🖥️ **Interfaz de pestañas** organizada

## 🎯 Comparación de Interfaces

| Característica | Streamlit v2.0 | Tkinter Legacy |
|---|---|---|
| **Timeline Visual** | ✅ Sliders interactivos | ❌ Solo entrada de texto |
| **Vista Previa** | ✅ Tiempo real | ❌ Solo confirmación |
| **Drag & Drop** | ✅ Archivos locales | ❌ Solo selector |
| **Responsive** | ✅ Todos los dispositivos | ❌ Solo escritorio |
| **Interfaz** | 🎨 Moderna y colorida | 🖥️ Clásica |
| **Performance** | ⚡ Cache inteligente | ⚡ Rápida |
| **Accesibilidad** | 🌐 Web (URL compartible) | 🖥️ Solo local |

## 🎬 Uso del Timeline Visual (Streamlit)

### ✂️ **Crear Clips con Timeline:**

1. **Pega la URL** del video de YouTube
2. **Analiza el video** - Se muestra toda la información
3. **Usa el timeline:**
   - 🎯 **Slider de inicio**: Arrastra para seleccionar dónde empezar
   - 🎯 **Slider de fin**: Arrastra para seleccionar dónde terminar
   - 📊 **Barra de progreso**: Visualiza el rango seleccionado
   - ⏱️ **Vista previa**: Ve la duración exacta en tiempo real

4. **Accesos rápidos:**
   - 📺 **Primeros 30s**: Perfecto para previews
   - 🎵 **1 minuto**: Ideal para highlights musicales
   - 📹 **2 minutos**: Clips de contenido
   - 🎬 **5 minutos**: Segmentos completos

5. **Crea el clip** con un solo click

### 📁 **Videos Locales con Drag & Drop:**

1. **Arrastra tu video** al área de carga
2. **Analiza automáticamente** - ffprobe obtiene toda la info
3. **Usa el mismo timeline** para seleccionar tu clip
4. **Crea clips** directamente sin conversiones

### 📟 Versión de Consola

#### Interactiva:
```bash
python youtube_downloader.py
```

#### Con parámetros:
```bash
python youtube_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

#### Versión avanzada con menús:
```bash
python youtube_downloader_advanced.py
```

## ⚙️ Características

### 🎨 Interfaz Gráfica
- ✅ Diseño moderno con pestañas
- ✅ Obtención automática de información del video
- ✅ Selección visual de calidad (best, 720p, 480p, 360p, worst)
- ✅ Opción para descargar solo audio (MP3)
- ✅ Descarga de subtítulos automáticos
- ✅ **Creación de clips personalizados**
- ✅ **Procesamiento de archivos de video locales**
- ✅ **Herramientas de tiempo con accesos rápidos**
- ✅ Explorador de directorios integrado
- ✅ Barra de progreso en tiempo real
- ✅ Información detallada en formato JSON
- ✅ Enlaces rápidos a recursos útiles
- ✅ Gestión de archivos (abrir/limpiar directorio)

### 📟 Versión de Consola
- ✅ Descarga videos en diferentes calidades
- ✅ Extracción de audio a MP3
- ✅ Descarga de subtítulos
- ✅ Soporte para playlists (versión avanzada)
- ✅ Interfaz interactiva amigable
- ✅ Manejo robusto de errores

## 📁 Estructura del proyecto

```
ytworker/
├── youtube_downloader.py         # Script básico de consola
├── youtube_downloader_advanced.py # Script avanzado con menús
├── youtube_downloader_gui.py     # Interfaz gráfica principal
├── ffmpeg-split.py              # Herramienta de división de videos
├── verify_ffmpeg.py             # Verificador de FFmpeg
├── test_clips.py                # Test de función de clips
├── diagnostico.py               # Diagnóstico completo del sistema
├── requirements.txt              # Dependencias
├── install.bat                   # Instalador automático
├── install_ffmpeg.bat           # Instalador de FFmpeg (batch)
├── install_ffmpeg_simple.bat    # Instalador simple con winget
├── install_ffmpeg.ps1           # Instalador de FFmpeg (PowerShell)
├── post_install_ffmpeg.bat      # Guía post-instalación
├── run_gui.bat                   # Acceso directo a la GUI
├── start.bat                     # Verificador completo + GUI
├── demo.py                      # Script de demostración
├── README.md                     # Este archivo
├── FFMPEG_INSTALL_GUIDE.md      # Guía detallada para instalar FFmpeg
├── downloads/                    # Carpeta por defecto para descargas
└── temp_clips/                  # Carpeta temporal para clips
```

## ✂️ Nueva Funcionalidad: Creador de Clips

### 🎯 ¿Qué hace?
La nueva pestaña "✂️ Crear Clips" te permite:

1. **🎬 Método Automático**: Descarga y crea clips en un solo paso
2. **✂️ Método Manual**: Descarga una vez, crea múltiples clips rápidamente
3. **Seleccionar tiempos específicos** (inicio y fin) con precisión
4. **Usar accesos rápidos** para duraciones comunes (30s, 1min, 2min, 5min)

## 📁 Nueva Funcionalidad: Procesador de Archivos Locales

### 🎯 ¿Qué hace?
La nueva pestaña "📁 Procesar Archivos" te permite:

1. **✂️ Crear Clips Directos**: Procesa archivos de tu PC sin descargar nada
2. **🎞️ Convertir y Crear Clips**: Convierte formatos incompatibles mientras crea clips
3. **Análisis de archivos**: Obtén información detallada de tus videos locales
4. **Todos los formatos**: Soporta MP4, AVI, MKV, MOV, WMV, FLV, WebM y más

### 🚀 Cómo usar el procesador de archivos:

1. **Ve a la pestaña "📁 Procesar Archivos"**
2. **Selecciona tu archivo de video** desde tu PC
3. **Obtén la información** del archivo (duración, resolución, códec, etc.)
4. **Configura los tiempos y nombre:**
   - Tiempo de inicio (ej: `00:01:30`)
   - Tiempo de fin (ej: `00:03:15`)
   - Nombre del clip
5. **Elige tu método:**
   - **✂️ Crear Clip**: Procesamiento directo y rápido
   - **🎞️ Convertir y Crear Clip**: Convierte a MP4 y crea el clip

### 💡 Ventajas del procesador de archivos:
- ✅ **Sin descargas**: Trabaja directamente con tus archivos
- ✅ **Súper rápido**: No necesita conexión a internet
- ✅ **Compatibilidad total**: Soporta todos los formatos de video comunes
- ✅ **Conversión automática**: Convierte formatos incompatibles a MP4
- ✅ **Información detallada**: Muestra resolución, fps, códec, tamaño del archivo

### 🚀 Cómo usar la función de clips (ACTUALIZADO):

**Método 1: 🎬 Proceso Automático (Recomendado)**
1. **Ve a la pestaña "✂️ Crear Clips"**
2. **Pega la URL** del video de YouTube
3. **Obtén la información** del video (duración, título, etc.)
4. **Configura los tiempos y nombre:**
   - Tiempo de inicio (ej: `00:01:30`)
   - Tiempo de fin (ej: `00:03:15`)
   - Nombre del clip
5. **¡Presiona "🎬 Descargar y Crear Clip"** - ¡El proceso es completamente automático!
   - ✅ Descarga el video completo temporalmente
   - ✅ Extrae el clip específico
   - ✅ Borra automáticamente el video original
   - ✅ Solo guarda el clip final

**Método 2: ✂️ Proceso Manual (Para múltiples clips)**
1. **Sigue los pasos 1-4 del método anterior**
2. **Presiona "Descargar Video Temporal"** - descarga el video completo una vez
3. **Configura diferentes tiempos** para múltiples clips
4. **Presiona "✂️ Crear Clip"** - crea clips rápidamente del video ya descargado
5. **Repite el paso 3-4** para crear más clips del mismo video

### ⚡ Accesos Rápidos:
- **📺 Primeros 30s**: Clip desde el inicio de 30 segundos
- **🎵 1 minuto**: Clip de 1 minuto desde el inicio  
- **📹 2 minutos**: Clip de 2 minutos desde el inicio
- **🎬 5 minutos**: Clip de 5 minutos desde el inicio

### 🕐 Formato de tiempo:
- **HH:MM:SS** (ej: `01:23:45`)
- **MM:SS** (ej: `23:45`)
- **SS** (ej: `45`)

## 🎯 Opciones de calidad

- **best**: Mejor calidad disponible
- **worst**: Menor calidad disponible
- **720p**: Máximo 720p
- **480p**: Máximo 480p
- **360p**: Máximo 360p

## 🖼️ Capturas de la GUI

La interfaz gráfica incluye:
- **Pestaña de Descarga**: Interfaz principal con todas las opciones de descarga
- **Pestaña de Clips**: Nueva funcionalidad para crear clips personalizados desde YouTube
- **Pestaña de Archivos**: Procesamiento y creación de clips desde archivos locales
- **Pestaña de Información**: Muestra información detallada del video en formato JSON
- **Pestaña de Configuración**: Enlaces útiles y gestión de archivos

## 🚀 Inicio Rápido

### ⚡ Para usuarios nuevos (Instalación completa):

1. **Descarga e instala Python** desde [python.org](https://python.org)
2. **Descarga este proyecto** y descomprímelo
3. **Ejecuta `install.bat`** para instalar las dependencias automáticamente
4. **Instala FFmpeg:** `winget install --id=Gyan.FFmpeg -e`
5. **Reinicia tu terminal/VS Code**
6. **Ejecuta `start.bat`** - verificará todo y abrirá la aplicación

### 🎯 Acceso rápido (si ya tienes todo instalado):

```bash
# Verificar que todo funciona + abrir GUI
start.bat

# Solo abrir GUI
python youtube_downloader_gui.py

# Verificar FFmpeg
python verify_ffmpeg.py
```

### Para desarrolladores:

```bash
# Clonar el proyecto
git clone <repositorio>
cd ytworker

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la GUI
python youtube_downloader_gui.py
```

## ⚠️ Notas importantes

- Asegúrate de que tienes derecho a descargar el contenido
- Respeta los términos de servicio de YouTube
- Algunos videos pueden no estar disponibles para descarga debido a restricciones regionales o de copyright
- La aplicación requiere conexión a internet para funcionar

## �️ Solución de problemas

### Errores comunes:

**"Python no está instalado"**
- Instala Python desde [python.org](https://python.org)
- Asegúrate de marcar "Add Python to PATH" durante la instalación

**"Error durante la descarga"**
- Verifica que la URL sea válida y el video esté disponible
- Comprueba tu conexión a internet
- Algunos videos pueden tener restricciones geográficas

**"FFmpeg no encontrado" (para clips)**
- **Instalación rápida:** `winget install --id=Gyan.FFmpeg -e`
- **IMPORTANTE:** Reinicia tu terminal/VS Code después de instalar
- Verifica con: `python verify_ffmpeg.py`
- También puedes usar: `powershell -ExecutionPolicy Bypass -File install_ffmpeg.ps1`

**"El botón de crear clips no hace nada"**
- ✅ **SOLUCIONADO:** Ahora el proceso es completamente automático
- Solo necesitas obtener la información del video primero
- El botón "🎬 Descargar y Crear Clip" hace todo automáticamente:
  - Descarga el video completo
  - Crea el clip
  - Borra el video original
- Los mensajes de progreso aparecerán en la interfaz
- Si hay errores, aparecerán mensajes de debug en la consola

**"ModuleNotFoundError"**
- Ejecuta `pip install -r requirements.txt`
- O usa `install.bat` para instalación automática

**"Permisos denegados"**
- Ejecuta como administrador si es necesario
- Verifica que tengas permisos de escritura en el directorio de descarga

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras errores o tienes sugerencias:

1. Reporta issues
2. Propón mejoras
3. Envía pull requests

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

---

**¡Disfruta descargando videos de YouTube de forma fácil y rápida! 🎉**
