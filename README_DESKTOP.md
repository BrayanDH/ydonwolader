# 🎬 YouTube Downloader Pro - Desktop Edition

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Kivy](https://img.shields.io/badge/Kivy-2.2+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightblue.svg)

**Aplicación de escritorio completa para descargar videos de YouTube y crear clips personalizados**

</div>

## 📋 Características Principales

### 🎬 YouTube Downloader & Clip Creator
- ✅ Descarga videos de YouTube en múltiples calidades
- ✅ Timeline interactivo para crear clips personalizados
- ✅ Previsualización en tiempo real del clip
- ✅ Configuraciones rápidas (30s, 1min, 2min, 5min)
- ✅ Análisis completo de metadata del video
- ✅ Interfaz moderna y responsive

### 📁 Procesamiento de Videos Locales
- ✅ Soporte para múltiples formatos (MP4, AVI, MKV, MOV, etc.)
- ✅ Análisis técnico con FFprobe
- ✅ Clip directo (rápido) o conversión con calidad
- ✅ Selector de archivos integrado
- ✅ Timeline adaptativo según duración

### 📥 Centro de Descargas
- ✅ Descargas masivas con control de calidad
- ✅ Extracción de audio (MP3)
- ✅ Subtítulos automáticos
- ✅ Historial de descargas
- ✅ Configuración de directorio personalizado

## 🚀 Instalación y Uso

### Método 1: Instalación Automática (Recomendado)

1. **Clona o descarga el proyecto:**
   ```bash
   git clone https://github.com/tu-usuario/ytworker.git
   cd ytworker
   ```

2. **Ejecuta el instalador:**
   ```batch
   # Doble clic en el archivo o ejecuta desde CMD
   install_kivy.bat
   ```

3. **Inicia la aplicación:**
   ```batch
   # Doble clic en el archivo o ejecuta desde CMD
   run_kivy.bat
   ```

### Método 2: Instalación Manual

1. **Instala Python 3.8+:**
   - Descarga desde [python.org](https://python.org)
   - ✅ Marca "Add Python to PATH" durante la instalación

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements_kivy.txt
   ```

3. **Instala FFmpeg:**
   
   **Opción A - Chocolatey (Recomendado):**
   ```batch
   choco install ffmpeg
   ```
   
   **Opción B - Winget:**
   ```batch
   winget install Gyan.FFmpeg
   ```
   
   **Opción C - Manual:**
   - Descarga desde [ffmpeg.org](https://ffmpeg.org/download.html#build-windows)
   - Extrae en `C:\ffmpeg`
   - Agrega `C:\ffmpeg\bin` al PATH del sistema

4. **Ejecuta la aplicación:**
   ```bash
   python kivy_app.py
   # O la versión moderna
   python kivy_app_modern.py
   ```

## 🎯 Guía de Uso

### YouTube Clips

1. **Analizar Video:**
   - Pega la URL de YouTube en el campo de texto
   - Haz clic en "🔍 Analizar"
   - Espera a que se cargue la información del video

2. **Configurar Timeline:**
   - Ajusta los sliders de inicio y fin
   - Usa los botones rápidos (30s, 1min, 2min, 5min)
   - Observa la previsualización en tiempo real

3. **Descargar y Crear Clip:**
   - Haz clic en "📥 Descargar Video"
   - Una vez descargado, configura el nombre del clip
   - Selecciona el formato (MP4, WEBM, MKV)
   - Haz clic en "✂️ Crear Clip"

### Videos Locales

1. **Seleccionar Archivo:**
   - Haz clic en "📎 Seleccionar Video"
   - Navega y selecciona tu archivo de video
   - Formatos soportados: MP4, AVI, MKV, MOV, WMV, FLV, WEBM, etc.

2. **Analizar Archivo:**
   - Haz clic en "🔍 Analizar Archivo"
   - El sistema analizará la duración y propiedades

3. **Crear Clip:**
   - Ajusta el timeline según tus necesidades
   - Elige el método:
     - **✂️ Clip Directo (Rápido):** Corta sin re-codificar
     - **🎞️ Convertir y Crear (Calidad):** Re-codifica para mejor compatibilidad
   - Haz clic en "🚀 Crear Clip"

### Centro de Descargas

1. **Configurar Descarga:**
   - Ingresa la URL del video
   - Selecciona la calidad deseada
   - Configura el directorio de descarga
   - Activa subtítulos si los necesitas

2. **Iniciar Descarga:**
   - Haz clic en "📥 Descargar Video"
   - Observa el progreso en tiempo real
   - El archivo se guardará en el directorio especificado

## 🛠️ Estructura del Proyecto

```
ytworker/
├── 📱 kivy_app.py              # Aplicación completa con todas las funciones
├── 🎨 kivy_app_modern.py       # Versión moderna con mejor diseño
├── 🌐 streamlit_app.py         # Versión web (Streamlit)
├── 📦 requirements_kivy.txt    # Dependencias para Kivy
├── ⚙️ install_kivy.bat         # Instalador automático
├── 🚀 run_kivy.bat             # Launcher de la aplicación
├── 📁 downloads/               # Directorio de descargas (se crea automáticamente)
└── 🔒 .gitignore              # Archivos excluidos del control de versiones
```

## 🎨 Capturas de Pantalla

### Pantalla Principal
- 🎬 Tabs organizados por funcionalidad
- 🎯 Interfaz moderna y intuitiva
- 📊 Timeline interactivo y visual

### Timeline Interactivo
- 🕐 Sliders para inicio y fin
- 📊 Barra de progreso visual
- ⚡ Botones de configuración rápida
- 📏 Información en tiempo real

### Información de Video
- 📺 Metadata completa del video
- 👤 Canal, duración, fecha, vistas
- 🎯 Resolución y formato
- 📅 Fecha de análisis

## ⚙️ Dependencias

### Principales
- **Python 3.8+** - Lenguaje base
- **Kivy 2.2+** - Framework de interfaz gráfica
- **yt-dlp** - Descarga de videos de YouTube
- **FFmpeg** - Procesamiento de video y audio

### Opcionales
- **KivyMD** - Componentes Material Design
- **Plyer** - Notificaciones del sistema
- **Pillow** - Procesamiento de imágenes

## 🔧 Solución de Problemas

### Error: "Python no encontrado"
```bash
# Verifica la instalación de Python
python --version

# Si no funciona, reinstala Python desde python.org
# ✅ Marca "Add Python to PATH"
```

### Error: "FFmpeg no encontrado"
```bash
# Verifica la instalación
ffmpeg -version

# Si no funciona:
# 1. Instala con Chocolatey: choco install ffmpeg
# 2. O descarga manual y agrega al PATH
```

### Error: "Módulo 'kivy' no encontrado"
```bash
# Reinstala Kivy
pip uninstall kivy
pip install kivy[base]

# O usa el instalador automático
install_kivy.bat
```

### Rendimiento Lento
- ✅ Cierra otras aplicaciones pesadas
- ✅ Usa "Clip Directo" para videos grandes
- ✅ Verifica espacio en disco
- ✅ Actualiza los drivers gráficos

## 🆚 Comparación de Versiones

| Característica | Streamlit Web | Kivy Desktop |
|----------------|---------------|--------------|
| 🌐 Acceso | Navegador web | Aplicación nativa |
| 🎨 Interfaz | Web responsiva | Desktop nativa |
| ⚡ Rendimiento | Depende del navegador | Rendimiento nativo |
| 📁 Archivos locales | Limitado por navegador | Acceso completo |
| 🔄 Hot reload | ✅ Automático | Manual |
| 📱 Móviles | ✅ Compatible | ❌ Solo desktop |
| 🖥️ Offline | ❌ Requiere servidor | ✅ Completamente offline |

## 📈 Funcionalidades Futuras

- [ ] 🎞️ Editor de video avanzado
- [ ] 🔄 Conversión por lotes
- [ ] 🎵 Extractor de audio mejorado
- [ ] 📱 Versión móvil con Kivy
- [ ] 🌐 Integración con más plataformas
- [ ] 🎨 Temas personalizables
- [ ] 📊 Estadísticas de uso
- [ ] 🔗 Playlist manager

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Por favor:

1. 🍴 Fork el proyecto
2. 🌟 Crea una rama para tu feature
3. 💻 Realiza tus cambios
4. 🧪 Prueba exhaustivamente
5. 📝 Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## 🙋‍♂️ Soporte

- 📧 **Email:** tu-email@ejemplo.com
- 🐛 **Issues:** [GitHub Issues](https://github.com/tu-usuario/ytworker/issues)
- 💬 **Discusiones:** [GitHub Discussions](https://github.com/tu-usuario/ytworker/discussions)

---

<div align="center">

**🎬 YouTube Downloader Pro - Convirtiendo ideas en clips desde 2024 🎬**

Made with ❤️ and lots of ☕

</div>
