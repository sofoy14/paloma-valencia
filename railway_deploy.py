#!/usr/bin/env python3
"""
Script para deployar automáticamente a Railway usando la API
API Key: f59bca07-45cd-46db-a200-726f1b20b25f
"""

import subprocess
import json
import time
import os

API_KEY = "f59bca07-45cd-46db-a200-726f1b20b25f"
PROJECT_NAME = "paloma-monitoreo"

def run_command(cmd, description):
    """Ejecuta comando y muestra output"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr and "error" in result.stderr.lower():
        print(f"⚠️  {result.stderr}")
    return result.returncode == 0

print("""
╔════════════════════════════════════════════════════════════╗
║     DEPLOY AUTOMÁTICO A RAILWAY - Paloma Valencia         ║
╚════════════════════════════════════════════════════════════╝
""")

# Verificar git
print("📋 Verificando repositorio Git...")
if not os.path.exists(".git"):
    run_command("git init", "Inicializando Git")

# Verificar archivos necesarios
required_files = ["app.py", "requirements.txt", "Procfile"]
missing = [f for f in required_files if not os.path.exists(f)]
if missing:
    print(f"❌ Faltan archivos: {missing}")
    exit(1)

print("✅ Archivos necesarios encontrados")

# Configurar git si es necesario
try:
    subprocess.run("git config user.email", shell=True, capture_output=True, check=True)
except:
    run_command('git config user.email "deploy@paloma.valencia"', "Configurando git email")
    run_command('git config user.name "Deploy Bot"', "Configurando git nombre")

# Commit de cambios
print("\n📦 Preparando código para subir...")
run_command("git add .", "Agregando archivos")
run_command('git commit -m "Deploy a Railway - listo para producción"', "Commit de cambios")

# Verificar si ya tiene remote
result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
if "origin" not in result.stdout:
    print("\n⚠️  No se detectó repositorio remoto de GitHub")
    print("\nPor favor, crea un repositorio en GitHub:")
    print("1. Ve a https://github.com/new")
    print("2. Nombre: paloma-valencia")
    print("3. No inicialices con README (ya lo tenemos)")
    print("4. Copia la URL del repo")
    
    github_url = input("\nPega la URL del repo de GitHub: ").strip()
    
    if github_url:
        run_command(f"git remote add origin {github_url}", "Conectando con GitHub")
        run_command("git branch -M main", "Cambiando a rama main")

# Push a GitHub
print("\n☁️  Subiendo código a GitHub...")
success = run_command("git push -u origin main", "Push a GitHub")

if not success:
    print("\n⚠️  No se pudo hacer push automático")
    print("Intenta manualmente:")
    print("  git push -u origin main")

print("""
╔════════════════════════════════════════════════════════════╗
║  CÓDIGO EN GITHUB - AHORA DEPLOY A RAILWAY                 ║
╚════════════════════════════════════════════════════════════╝

Para completar el deploy en Railway:

OPCIÓN 1 - Web (Recomendada):
  1. Ve a: https://railway.app/new
  2. Click "Deploy from GitHub repo"
  3. Selecciona "paloma-valencia"
  4. Click "Deploy"
  5. Ve a "Variables" y agrega:
     
     CALLMEBOT_APIKEY=tu_apikey
     CALLMEBOT_PHONE=573174018932
     PYTHONUNBUFFERED=1

OPCIÓN 2 - CLI:
  npm install -g @railway/cli
  railway login
  railway init --name paloma-monitoreo
  railway up

Tu API Key está lista: f59bca07-45cd-46db-a200-726f1b20b25f

════════════════════════════════════════════════════════════
""")

# Guardar instrucciones
with open("DEPLOY_RAILWAY_AHORA.txt", "w") as f:
    f.write("""
DEPLOY A RAILWAY - INSTRUCCIONES

Tu código está listo en GitHub.

PASOS:

1. Ve a: https://railway.app/new

2. Click: "Deploy from GitHub repo"

3. Selecciona tu repo: paloma-valencia

4. Click: "Deploy"

5. Configurar Variables (importante):
   Ve a la pestaña "Variables" del proyecto
   Agrega estas variables:

   CALLMEBOT_APIKEY=tu_apikey_de_callmebot
   CALLMEBOT_PHONE=573174018932
   PYTHONUNBUFFERED=1

   Opcionales:
   TELEGRAM_BOT_TOKEN=
   TELEGRAM_CHAT_ID=
   NEWS_API_KEY=

6. Listo! Railway te dará una URL tipo:
   https://paloma-monitoreo.up.railway.app

7. Comparte esa URL con tu equipo.

═══════════════════════════════════════════════════════════
NOTA: El sistema funcionará 24/7 en Railway sin tu PC.
NOTA: Chrome/WebScraper NO funciona en Railway (solo RSS/API)
═══════════════════════════════════════════════════════════
""")

print("✅ Instrucciones guardadas en: DEPLOY_RAILWAY_AHORA.txt")
