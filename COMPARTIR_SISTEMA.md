# 🌐 Cómo Compartir el Sistema con Otros

Guía para que otras personas puedan ver y usar el monitoreo.

---

## 🥇 OPCIÓN 1: ngrok (GRATIS - Para usar HOY)

La forma más rápida de compartir tu sistema local. Perfecto para el día de elecciones.

### Paso 1: Instalar ngrok
```bash
# Windows (PowerShell como Admin)
choco install ngrok

# O descarga desde:
# https://ngrok.com/download
```

### Paso 2: Crear cuenta gratis
1. Ve a https://ngrok.com
2. Regístrate (solo email)
3. Copia tu authtoken

### Paso 3: Configurar
```bash
ngrok config add-authtoken TU_AUTHTOKEN
```

### Paso 4: Iniciar todo

**Terminal 1 - Iniciar el sistema:**
```bash
cd D:\Projects\paloma-valencia
python app.py
```

**Terminal 2 - Iniciar ngrok:**
```bash
ngrok http 5000
```

### Paso 5: Compartir URL
ngrok te dará algo como:
```
Forwarding: https://abc123-def.ngrok-free.app -> http://localhost:5000
```

**Esa URL (`https://abc123-def.ngrok-free.app`) la puedes compartir con:**
- Tu equipo de campaña
- Asesores
- Cualquier persona

Ellos verán el dashboard en tiempo real desde su celular/computadora.

### ⚠️ Limitaciones ngrok gratuito:
- URL cambia cada vez que reinicias ngrok
- 40 conexiones/minuto límite
- Para elecciones: Suficiente para 10-20 personas

---

## 🥈 OPCIÓN 2: Render.com (GRATIS - Permanente)

Para tener el sistema siempre disponible sin depender de tu PC.

### Paso 1: Subir a GitHub
```bash
# Crear repo en GitHub
# Subir todo el código
git init
git add .
git commit -m "Sistema de monitoreo"
git push origin main
```

### Paso 2: Crear cuenta en Render
1. Ve a https://render.com
2. Regístrate con GitHub

### Paso 3: Crear Web Service
1. "New" → "Web Service"
2. Conecta tu repo de GitHub
3. Configuración:
   - **Name:** `paloma-monitoreo`
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan:** Free

### Paso 4: Variables de Entorno
En el dashboard de Render, agrega:
```
CALLMEBOT_APIKEY=tu_apikey
CALLMEBOT_PHONE=573174018932
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
```

### Paso 5: Crear Disco (para SQLite)
1. Ve a "Disks" en el sidebar
2. "Create Disk"
   - Name: `data`
   - Mount Path: `/opt/render/project/src/data`
   - Size: 1 GB

### Paso 6: Deploy
- Click "Deploy"
- Espera ~2 minutos
- Te dará URL tipo: `https://paloma-monitoreo.onrender.com`

**URL permanente para compartir con todos.**

### ⚠️ Limitaciones plan gratuito:
- Se "duerme" después de 15 minutos de inactividad
- Se despierta solo cuando alguien entra (tarda ~30 segundos)
- 750 horas/mes (suficiente para 1 app)

**Solución:** Configura un "pinger" (ver abajo)

---

## 🥉 OPCIÓN 3: Railway.app ($5 crédito/mes)

Similar a Render pero con crédito mensual.

1. Cuenta en https://railway.app
2. "New Project" → "Deploy from GitHub"
3. Variables de entorno en "Variables"
4. Deploy automático

---

## 🏆 OPCIÓN 4: VPS $5/mes (Profesional)

Si el comité de campaña puede pagar $5/mes:

### Opciones:
- **DigitalOcean:** https://m.do.co/c/tu-link (crédito gratis)
- **Linode:** https://linode.com
- **Vultr:** https://vultr.com

### VPS mínimo necesario:
- 1 GB RAM
- 1 CPU
- 25 GB SSD
- Ubuntu 20.04

### Instalación rápida:
```bash
# En el servidor VPS
sudo apt update
sudo apt install python3-pip chromium-chromedriver git

git clone https://github.com/tuusuario/paloma-valencia.git
cd paloma-valencia
pip3 install -r requirements.txt

# Iniciar
python3 app.py
```

### Mantener prendido con systemd (opcional):
Crear archivo `/etc/systemd/system/paloma.service`:
```ini
[Unit]
Description=Paloma Valencia Monitoreo
After=network.target

[Service]
User=root
WorkingDirectory=/root/paloma-valencia
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Activar:
```bash
sudo systemctl enable paloma
sudo systemctl start paloma
```

---

## 📱 Mantener Render Despierto (Opcional)

Para evitar que Render se "duerma":

### Opción A: Cron-job.org (Gratis)
1. Ve a https://cron-job.org
2. Crea cuenta gratis
3. "Create cronjob"
   - URL: `https://tu-app.onrender.com/api/stats`
   - Schedule: Every 5 minutes

### Opción B: UptimeRobot (Gratis)
1. https://uptimerobot.com
2. "Add New Monitor"
   - Type: HTTP(s)
   - URL: Tu URL de Render
   - Interval: 5 minutes

---

## 🔐 Seguridad al Compartir

### Si usas ngrok:
- La URL es temporal (cambia cada vez)
- No necesitas preocuparte mucho por seguridad
- Comparte solo con personas de confianza

### Si usas Render/Railway:
- Cualquiera con la URL puede ver el dashboard
- **NO expongas información sensible**
- Considera agregar contraseña básica

### Agregar contraseña simple (opcional):
Edita `app.py` y agrega:
```python
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

auth = HTTPBasicAuth()
users = {
    "paloma": generate_password_hash("elecciones2026")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route('/')
@auth.login_required
def index():
    return send_from_directory('static', 'dashboard.html')
```

Instalar: `pip install flask-httpauth`

---

## 🚀 Recomendación para Elecciones

### Para el día de elecciones (domingo):

**Opción recomendada: ngrok + tu laptop**

1. **Preparar la noche anterior:**
   ```bash
   # Probar que todo funciona
   python app.py
   ngrok http 5000
   ```

2. **El día de elecciones:**
   - Prende tu laptop temprano
   - Inicia el sistema
   - Inicia ngrok
   - Comparte la URL en el grupo de WhatsApp del comando

3. **Durante el día:**
   - No apagues la laptop
   - Mantén conectado a internet
   - Las alertas llegarán al celular configurado

### Ventajas:
- ✅ Gratis
- ✅ Rápido de configurar
- ✅ Funciona inmediatamente
- ✅ Toda la potencia de tu computadora

---

## 📋 Checklist antes de compartir

- [ ] Sistema funcionando local (`python app.py`)
- [ ] ngrok instalado y configurado (u otro servicio)
- [ ] Notificaciones configuradas (CallMeBot/Telegram)
- [ ] URL de acceso pública funcionando
- [ ] Equipo de campaña tiene la URL
- [ ] Probado en celular (responsive)

---

**¿Necesitas ayuda configurando alguna de estas opciones?**
