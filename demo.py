#!/usr/bin/env python3
"""
Script de demostración para YouTube Downloader
Muestra ejemplos de uso sin realizar descargas reales
"""

import tkinter as tk
from tkinter import messagebox
import webbrowser

def mostrar_demo():
    """Muestra una ventana de demostración"""
    
    def abrir_gui():
        """Abre la aplicación principal"""
        root_demo.destroy()
        import subprocess
        subprocess.run(["python", "youtube_downloader_gui.py"])
    
    def ver_ejemplos():
        """Muestra ejemplos de URLs"""
        ejemplos = """
🎬 Ejemplos de URLs que puedes probar:

📺 Videos educativos:
• https://www.youtube.com/watch?v=dQw4w9WgXcQ (ejemplo clásico)

🎵 Videos musicales:
• Busca tus canciones favoritas en YouTube

📚 Tutoriales:
• Videos de programación, cocina, etc.

⚠️ Recuerda:
• Solo descarga contenido que tengas derecho a usar
• Respeta los derechos de autor
• Verifica que el video sea público
        """
        messagebox.showinfo("📋 Ejemplos de uso", ejemplos)
    
    def ver_funciones():
        """Muestra las principales funciones"""
        funciones = """
🚀 Funciones principales de YouTube Downloader:

📥 DESCARGA:
• Videos en múltiples calidades (4K, 1080p, 720p, 480p, 360p)
• Solo audio en formato MP3
• Subtítulos automáticos en español e inglés

🎯 INTERFAZ:
• Interfaz gráfica intuitiva con pestañas
• Obtención automática de información del video
• Selector de directorio de descarga
• Barra de progreso en tiempo real

📊 INFORMACIÓN:
• Título, duración y canal del video
• Descripción y fecha de subida
• Formatos disponibles
• Información técnica completa en JSON

⚙️ CONFIGURACIÓN:
• Gestión de directorios
• Enlaces útiles integrados
• Limpieza automática de archivos
        """
        messagebox.showinfo("⚡ Funciones", funciones)
    
    # Crear ventana de demostración
    root_demo = tk.Tk()
    root_demo.title("🎬 YouTube Downloader - Demo")
    root_demo.geometry("500x400")
    root_demo.resizable(False, False)
    
    # Centrar ventana
    root_demo.update_idletasks()
    x = (root_demo.winfo_screenwidth() // 2) - (root_demo.winfo_width() // 2)
    y = (root_demo.winfo_screenheight() // 2) - (root_demo.winfo_height() // 2)
    root_demo.geometry(f"+{x}+{y}")
    
    # Título principal
    titulo = tk.Label(root_demo, text="🎬 YouTube Video Downloader", 
                     font=("Arial", 18, "bold"), fg="#1f4e79")
    titulo.pack(pady=20)
    
    subtitulo = tk.Label(root_demo, text="Descarga videos de YouTube de forma fácil y rápida", 
                        font=("Arial", 12), fg="#666666")
    subtitulo.pack(pady=(0, 20))
    
    # Frame para botones
    frame_botones = tk.Frame(root_demo)
    frame_botones.pack(expand=True)
    
    # Botón principal
    btn_abrir_gui = tk.Button(frame_botones, text="🚀 Abrir Aplicación Principal", 
                             command=abrir_gui, font=("Arial", 14, "bold"),
                             bg="#4CAF50", fg="white", relief="raised", bd=3,
                             width=25, height=2)
    btn_abrir_gui.pack(pady=10)
    
    # Botones informativos
    btn_ejemplos = tk.Button(frame_botones, text="📋 Ver Ejemplos de Uso", 
                            command=ver_ejemplos, font=("Arial", 11),
                            bg="#2196F3", fg="white", relief="raised", bd=2,
                            width=25)
    btn_ejemplos.pack(pady=5)
    
    btn_funciones = tk.Button(frame_botones, text="⚡ Ver Funciones", 
                             command=ver_funciones, font=("Arial", 11),
                             bg="#FF9800", fg="white", relief="raised", bd=2,
                             width=25)
    btn_funciones.pack(pady=5)
    
    # Separador
    separador = tk.Frame(root_demo, height=2, bg="#cccccc")
    separador.pack(fill=tk.X, pady=20, padx=50)
    
    # Enlaces
    frame_enlaces = tk.Frame(root_demo)
    frame_enlaces.pack()
    
    btn_youtube = tk.Button(frame_enlaces, text="📺 Ir a YouTube", 
                           command=lambda: webbrowser.open("https://youtube.com"),
                           bg="#FF0000", fg="white", font=("Arial", 10),
                           width=15)
    btn_youtube.pack(side=tk.LEFT, padx=5)
    
    btn_salir = tk.Button(frame_enlaces, text="❌ Salir", 
                         command=root_demo.destroy,
                         bg="#f44336", fg="white", font=("Arial", 10),
                         width=15)
    btn_salir.pack(side=tk.LEFT, padx=5)
    
    # Información en la parte inferior
    info_footer = tk.Label(root_demo, text="Creado con Python + tkinter | Powered by yt-dlp", 
                          font=("Arial", 8), fg="#999999")
    info_footer.pack(side=tk.BOTTOM, pady=10)
    
    root_demo.mainloop()

def main():
    """Función principal del demo"""
    mostrar_demo()

if __name__ == "__main__":
    main()
