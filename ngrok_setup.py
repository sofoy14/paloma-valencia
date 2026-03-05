"""
Script para configurar ngrok automáticamente
Expone el dashboard a internet para que otros lo vean
"""
import subprocess
import sys
import os
import time

def install_ngrok():
    """Instala ngrok si no está instalado"""
    try:
        subprocess.run(['ngrok', '--version'], capture_output=True, check=True)
        print("✓ ngrok ya está instalado")
        return True
    except:
        print("⚠️  ngrok no está instalado")
        print("\n📥 Descargando ngrok...")
        print("   Ve a: https://ngrok.com/download")
        print("   Descarga la versión para Windows")
        print("   Descomprime y coloca ngrok.exe en esta carpeta")
        print("\n   O ejecuta: choco install ngrok (si tienes Chocolatey)")
        return False

def setup_ngrok():
    """Configura ngrok con token"""
    token = input("\n🔑 Ingresa tu ngrok authtoken (regístrate gratis en ngrok.com): ").strip()
    
    if not token:
        print("❌ Token requerido")
        return False
    
    try:
        result = subprocess.run(
            ['ngrok', 'config', 'add-authtoken', token],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✓ Token configurado correctamente")
            return True
        else:
            print(f"❌ Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def start_ngrok():
    """Inicia ngrok en puerto 5000"""
    print("\n🚀 Iniciando ngrok...")
    print("   Tu dashboard será accesible desde internet en:")
    print("   https://xxxxx.ngrok-free.app")
    print("\n   Comparte esa URL con tu equipo")
    print("   Presiona Ctrl+C para detener\n")
    
    try:
        # Iniciar ngrok
        process = subprocess.Popen(
            ['ngrok', 'http', '5000', '--domain', 'paloma-valencia.ngrok-free.app'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Esperar y mostrar info
        time.sleep(3)
        print("✓ ngrok ejecutándose")
        print("\n📱 URLs de acceso:")
        print("   Local:    http://localhost:5000")
        print("   Público:  https://paloma-valencia.ngrok-free.app")
        print("             (o revisa la URL que muestra ngrok arriba)")
        
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n👋 Deteniendo ngrok...")
        process.terminate()
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == '__main__':
    print("="*70)
    print("CONFIGURACIÓN NGROK - Acceso Remoto al Dashboard")
    print("="*70)
    print("\nEsto permitirá que otros miembros del equipo vean el dashboard")
    print("desde sus celulares/computadoras sin estar en tu red.\n")
    
    if not install_ngrok():
        input("\nPresiona Enter cuando hayas instalado ngrok...")
    
    # Verificar si ya tiene token
    config_path = os.path.expanduser('~/.ngrok2/ngrok.yml')
    if not os.path.exists(config_path):
        print("\n🔐 Primera vez usando ngrok")
        if not setup_ngrok():
            sys.exit(1)
    
    start_ngrok()
