# 🚄 Deploy Final - Opciones con tu API Key

Tienes tu API Key: `f59bca07-45cd-46db-a200-726f1b20b25f`

Aquí las opciones de deploy ordenadas de más fácil a más compleja:

---

## 🥇 OPCIÓN 1: Deploy via Web (RECOMENDADA - 5 minutos)

La forma más rápida y confiable.

### Paso 1: Sube a GitHub
```bash
# Crear repo en GitHub primero (https://github.com/new)
# Nombre: paloma-valencia

# En tu PC:
git remote add origin https://github.com/TU_USUARIO/paloma-valencia.git
git branch -M main
git push -u origin main
```

### Paso 2: Deploy en Railway
1. Ve a https://railway.app/new
2. Click **"Deploy from GitHub repo"**
3. Selecciona `paloma-valencia`
4. Click **"Deploy"**

### Paso 3: Variables de Entorno
1. En tu proyecto Railway, click **"Variables"**
2. Agrega una por una:
```
CALLMEBOT_APIKEY=tu_apikey
CALLMEBOT_PHONE=573174018932
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
NEWS_API_KEY=
PYTHONUNBUFFERED=1
```

### Paso 4: Listo!
Railway te dará una URL como:
```
https://paloma-valencia.up.railway.app
```

---

## 🥈 OPCIÓN 2: Usar CLI de Railway (10 minutos)

### Instalar CLI:
```bash
npm install -g @railway/cli
```

### Login (se abrirá navegador):
```bash
railway login
```

### Crear proyecto y deployar:
```bash
cd paloma-valencia

# Inicializar proyecto
railway init --name "paloma-monitoreo"

# Ver estado
railway status

# Deploy
railway up
```

### Configurar variables:
```bash
railway variables set CALLMEBOT_APIKEY="tu_apikey"
railway variables set CALLMEBOT_PHONE="573174018932"
railway variables set PYTHONUNBUFFERED="1"
```

---

## 🥉 OPCIÓN 3: Script Automático (PowerShell)

Ejecuta el script que creé:

```powershell
# En PowerShell como Administrador
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
.\deploy_api_directo.ps1
```

Este script:
1. Verifica tu API key
2. Intenta crear el proyecto via API
3. Te da instrucciones detalladas

---

## ⚠️ IMPORTANTE: Limitaciones en Railway

### ¿Qué SÍ funciona?
- ✅ RSS (13 departamentos)
- ✅ NewsAPI
- ✅ Google News
- ✅ Twitter/X
- ✅ Dashboard web
- ✅ Notificaciones
- ✅ Base de datos SQLite

### ¿Qué NO funciona?
- ❌ Chrome Web Scraper (Railway no tiene Chrome)

**Resultado:** ~80% de cobertura (19 de 32 departamentos)

### Para 100% cobertura:
Usa tu PC local con Chrome instalado, o un VPS con Chrome.

---

## 🔧 Variables de Entorno Necesarias

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `CALLMEBOT_APIKEY` | WhatsApp via CallMeBot | `1234567` |
| `CALLMEBOT_PHONE` | Tu número | `573174018932` |
| `TELEGRAM_BOT_TOKEN` | Bot de Telegram | `123456:ABC...` |
| `TELEGRAM_CHAT_ID` | Tu chat ID | `12345678` |
| `NEWS_API_KEY` | NewsAPI.org | `abc123...` |
| `PYTHONUNBUFFERED` | Logs en tiempo real | `1` |

---

## 📊 Costo

- **Plan:** Gratuito ($5 crédito/mes)
- **Uso estimado:** $3-4/mes
- **¿Alcanza?:** ✅ Sí, sobra

---

## 🆘 Si algo falla

### "Build failed"
Revisa `requirements.txt` - quita `undetected-chromedriver` si está.

### "Application Error"
Verifica que `Procfile` existe y tiene:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

### "Cannot find module"
Asegúrate de que todos los archivos están en GitHub:
```bash
git status
git add .
git commit -m "Fix"
git push
```

---

## ✅ Checklist antes de deploy

- [ ] Código en GitHub
- [ ] Archivo `requirements.txt` actualizado
- [ ] Archivo `Procfile` creado
- [ ] `.gitignore` configurado (sin .env)
- [ ] Variables de entorno listas

---

## 🚀 Comandos útiles en Railway

```bash
# Ver logs
railway logs

# Ver estado
railway status

# Abrir en navegador
railway open

# Reiniciar
railway restart

# Variables
railway variables
```

---

**¿Cuál opción prefieres?** Te recomiendo la **Opción 1** (Web) porque es la más simple y rápida.
