#!/usr/bin/env python3
"""
Script de debug específico para el botón de crear clips
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
from pathlib import Path

def test_button_function():
    """Simula exactamente lo que hace el botón de crear clips"""
    
    print("🔍 INICIANDO DEBUG DEL BOTÓN CREAR CLIPS")
    print("="*50)
    
    # Simular los datos que tendría la GUI
    video_temp_path = None
    inicio_clip = "00:00:00"
    fin_clip = "00:00:30"
    nombre_clip = "test_clip"
    directorio_descarga = "downloads"
    
    print(f"📋 Datos simulados:")
    print(f"   Video temporal: {video_temp_path}")
    print(f"   Inicio: {inicio_clip}")
    print(f"   Fin: {fin_clip}")
    print(f"   Nombre: {nombre_clip}")
    print(f"   Directorio: {directorio_descarga}")
    print()
    
    # Verificar si hay videos temporales
    temp_dir = Path("temp_clips")
    print(f"🔍 Verificando directorio temporal: {temp_dir}")
    
    if temp_dir.exists():
        video_files = list(temp_dir.glob("*.mp4")) + list(temp_dir.glob("*.webm")) + list(temp_dir.glob("*.mkv"))
        print(f"   Archivos encontrados: {len(video_files)}")
        for i, file in enumerate(video_files[:3]):  # Solo mostrar los primeros 3
            print(f"   {i+1}. {file.name}")
            
        if video_files:
            video_temp_path = str(video_files[0])
            print(f"   ✅ Usando: {video_temp_path}")
        else:
            print("   ❌ No se encontraron videos")
    else:
        print("   ❌ Directorio no existe")
    
    print()
    
    # Simular la lógica del botón
    print("🎯 SIMULANDO LÓGICA DEL BOTÓN:")
    
    # Verificación 1: Video temporal
    if not video_temp_path or not os.path.exists(video_temp_path):
        print("❌ FALLA EN VERIFICACIÓN 1: Video temporal no encontrado")
        print("💡 SOLUCIÓN: Primero debes descargar un video en la pestaña de clips")
        return False
    else:
        print("✅ VERIFICACIÓN 1 PASADA: Video temporal existe")
    
    # Verificación 2: Campos completos
    if not all([inicio_clip, fin_clip, nombre_clip]):
        print("❌ FALLA EN VERIFICACIÓN 2: Campos incompletos")
        return False
    else:
        print("✅ VERIFICACIÓN 2 PASADA: Todos los campos completos")
    
    # Verificación 3: Tiempos válidos
    def tiempo_a_segundos(tiempo_str):
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
    
    inicio_seg = tiempo_a_segundos(inicio_clip)
    fin_seg = tiempo_a_segundos(fin_clip)
    
    print(f"   Inicio: {inicio_clip} = {inicio_seg} segundos")
    print(f"   Fin: {fin_clip} = {fin_seg} segundos")
    
    if inicio_seg >= fin_seg:
        print("❌ FALLA EN VERIFICACIÓN 3: Tiempo inicio >= tiempo fin")
        return False
    else:
        print("✅ VERIFICACIÓN 3 PASADA: Tiempos válidos")
    
    print()
    print("🎉 TODAS LAS VERIFICACIONES PASADAS")
    print("📍 El botón debería ejecutar el hilo de creación de clips")
    
    return True

def test_gui_button():
    """Crea una ventana simple con un botón para probar"""
    
    print("\n🎨 CREANDO VENTANA DE PRUEBA")
    print("-" * 30)
    
    def on_button_click():
        print("🖱️ ¡BOTÓN PRESIONADO!")
        messagebox.showinfo("Test", "¡El botón funciona!")
    
    root = tk.Tk()
    root.title("Test Botón")
    root.geometry("300x200")
    
    label = tk.Label(root, text="Test del botón de crear clips", font=("Arial", 12))
    label.pack(pady=20)
    
    button = tk.Button(root, text="✂️ Test Crear Clip", 
                      command=on_button_click, 
                      font=("Arial", 12, "bold"),
                      bg="#FF9800", fg="white")
    button.pack(pady=20)
    
    close_btn = tk.Button(root, text="Cerrar", command=root.destroy)
    close_btn.pack(pady=10)
    
    print("✅ Ventana creada. Si el botón no responde, hay un problema con tkinter")
    root.mainloop()

def main():
    """Función principal de debug"""
    
    print("🔧 DEBUG AVANZADO: Botón Crear Clips")
    print("=" * 60)
    print()
    
    # Test 1: Lógica del botón
    print("TEST 1: Lógica del botón")
    success = test_button_function()
    
    if not success:
        print("\n❌ El problema está en la lógica de validación")
        print("🚨 NECESITAS:")
        print("1. Ir a la pestaña 'Crear Clips'")
        print("2. Pegar una URL de YouTube")
        print("3. Presionar 'Obtener Info'")
        print("4. Presionar 'Descargar Video Completo'")
        print("5. LUEGO presionar 'Crear Clip'")
        print()
    else:
        print("\n✅ La lógica está bien")
        print()
    
    # Test 2: GUI básica
    print("TEST 2: Interfaz gráfica básica")
    response = input("¿Quieres probar un botón simple de tkinter? (s/n): ").strip().lower()
    
    if response == 's':
        test_gui_button()
    
    print("\n🎯 DIAGNÓSTICO COMPLETO")
    print("=" * 60)
    
    if success:
        print("✅ La lógica del botón está correcta")
        print("💡 El problema puede ser:")
        print("   1. No has descargado el video temporal primero")
        print("   2. Problema en la GUI (event binding)")
        print("   3. Problema en el threading")
    else:
        print("❌ Problema en la lógica o falta video temporal")
    
    print("\n🔧 PRÓXIMOS PASOS:")
    print("1. Ejecuta la GUI: python youtube_downloader_gui.py")
    print("2. Ve a 'Crear Clips' y sigue el proceso completo")
    print("3. Observa los mensajes de debug en la consola")
    print("4. Si no ves mensajes, el botón no está conectado")

if __name__ == "__main__":
    main()
