# 🎬 Solución: Errores de Descarga y Creación de Clips

## Problema: "Requested format is not available"

Este error ocurre cuando intentas descargar o crear un clip de un video que **está protegido o restringido por YouTube**.

### ¿Por qué sucede?

YouTube tiene varios tipos de contenido restringido:
- **Videos protegidos**: Solo imágenes disponibles para descarga
- **Contenido de acceso limitado**: Restringido por región o permisos
- **Videos privados o eliminados**: Ya no están disponibles
- **Contenido con derechos de autor**: No se permite descarga

### Mensajes de Error Específicos

| Error | Causa | Solución |
|-------|-------|----------|
| `Only images are available` | Video completamente protegido | Prueba con otro video |
| `nsig extraction failed` | Problema con yt-dlp desactualizado | `pip install --upgrade yt-dlp` |
| `HTTP Error 403` | Acceso prohibido | Video restringido por región |
| `HTTP Error 404` | Video no encontrado | URL inválida o video eliminado |

## ✅ Soluciones

### 1. **Actualizar yt-dlp**
```powershell
pip install --upgrade yt-dlp
```

El protocolo de YouTube cambia constantemente. Una versión desactualizada causará fallos.

### 2. **Intentar con Otro Video**
- Prueba con videos públicos y sin restricciones
- Evita videos de música protegidos por derechos de autor
- Los videos de canales públicos generalmente funcionan mejor

### 3. **Verificar la URL**
- Asegúrate de que sea una URL válida de YouTube
- `https://www.youtube.com/watch?v=VIDEO_ID`
- Evita URLs acortadas

### 4. **Comprobar Disponibilidad Regional**
Algunos videos solo están disponibles en ciertos países. Si obtienes error 403:
- El video puede no estar disponible en tu región
- Prueba con una VPN (si es legal en tu jurisdicción)

## 📝 Recomendaciones

### Para Crear Clips:
1. **Uso del Botón Correcto**:
   - `✂️ Crear Clip`: Requiere video descargado previamente
   - `🎬 Descargar y Crear Clip`: Descarga automáticamente y crea el clip

2. **Formatos de Clip**:
   - Máximo recomendado: 720p
   - Duración mínima: 1-2 segundos
   - Duración máxima: Depende del video original

3. **Archivos Temporales**:
   - Se eliminan automáticamente después de crear el clip
   - Carpeta: `temp_clips/`
   - Si hay problemas, elimina manualmente esta carpeta

## 🔍 Depuración

Si el problema persiste:

### 1. **Ver Lista de Formatos Disponibles**
```powershell
yt-dlp --list-formats "https://www.youtube.com/watch?v=VIDEO_ID"
```

Esto mostrará qué formatos están realmente disponibles.

### 2. **Actualizar la Herramienta**
Abre una terminal y ejecuta:
```powershell
pip install --upgrade yt-dlp ffmpeg
```

### 3. **Probar Descarga Directa**
Intenta descargar el video completo primero:
```powershell
yt-dlp -f best "https://www.youtube.com/watch?v=VIDEO_ID"
```

## 📞 Problemas Frecuentes

### P: ¿Por qué algunos videos no se descargan?
R: YouTube cambia constantemente su sistema anti-descarga. Mantén yt-dlp actualizado.

### P: ¿Puedo descargar videos privados?
R: No. Solo videos públicos o aquellos a los que tengas acceso.

### P: ¿Hay límite de tamaño para los clips?
R: Depende de tu espacio en disco, pero se recomienda no exceder 5 GB.

### P: ¿Qué formatos de video funcionan?
R: MP4, WebM, MKV (los más comunes).

## 🚀 Próximos Pasos

Si sigues teniendo problemas:

1. Asegúrate de tener **Python 3.8+**
2. Actualiza **yt-dlp** regularmente
3. Verifica que **ffmpeg** esté instalado
4. Prueba con videos diferentes
5. Consulta el repositorio oficial: https://github.com/yt-dlp/yt-dlp

---

**Última actualización**: Diciembre 2025
