import socket
import webbrowser
import subprocess
import time
import os
from pathlib import Path

def is_running(port=8501):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex(('localhost', port)) == 0
    except:
        return False

def launch():
    # Obtener la ruta absoluta del directorio del script actual
    base_dir = Path(__file__).parent.absolute()
    app_path = base_dir / "streamlit_app.py"
    url = "http://localhost:8501"
    
    if is_running():
        print("\n[+] YTWorker Pro ya esta en ejecucion.")
        print("[+] Abriendo nueva pestaña en el navegador...")
        webbrowser.open(url)
    else:
        print("\n[!] YTWorker Pro no esta iniciado.")
        print("[!] Iniciando servidor Streamlit...")
        
        # Ejecutar streamlit run en segundo plano
        # Usamos creationflags=subprocess.CREATE_NEW_CONSOLE para que tenga su propia ventana si se desea
        # o lo dejamos normal para que el batch lo maneje.
        subprocess.Popen(["streamlit", "run", str(app_path)], shell=True, cwd=str(base_dir))
        
        print("[...] Esperando a que el servicio este listo...")
        # Esperar hasta 10 segundos a que el puerto se abra
        for i in range(15):
            if is_running():
                print("[+] Servidor listo!")
                break
            time.sleep(1)
            
        webbrowser.open(url)

if __name__ == "__main__":
    launch()
