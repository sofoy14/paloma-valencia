# 🚄 Railway - Guía Ultra Rápida

Deploy del sistema en **5 minutos**.

---

## ⚡ Pasos Rápidos

### 1. Subir a GitHub (2 min)
```bash
# Ya debería estar hecho, si no:
git add .
git commit -m "Version lista para Railway"
git push origin main
```

### 2. Crear proyecto en Railway (1 min)
1. Ve a https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Selecciona tu repo `paloma-valencia`
4. Click "Deploy"

### 3. Configurar Variables (2 min)
En Railway, ve a tu proyecto → "Variables" y agrega:

```
CALLMEBOT_APIKEY=tu_apikey
CALLMEBOT_PHONE=573174018932
TELEGRAM_BOT_TOKEN=tu_token
TELEGRAM_CHAT_ID=tu_chat_id
PYTHONUNBUFFERED=1
```

### 4. Listo! (30 seg)
Railway te da una URL tipo:
```
https://paloma-valencia.up.railway.app
```

**Comparte esa URL con tu equipo.**

---

## ⚠️ Importante

### Chrome/Web Scraper NO funciona en Railway
Railway no tiene Chrome. El sistema automáticamente usa:
- ✅ RSS (13 departamentos)
- ✅ NewsAPI
- ✅ Google News
- ✅ Twitter/X
- ✅ Total: ~80% de cobertura

Para 100% cobertura, usa tu PC local.

### Base de datos
Los datos se guardan pero pueden perderse si no configuras Volume.

Para persistencia: Ve a Settings → Volumes → Add Volume:
- Mount Path: `/app/data`
- Size: 1 GB

---

## 🔧 Comandos útiles

### Ver logs:
Railway dashboard → tu servicio → "Logs"

### Reiniciar:
Railway dashboard → tu servicio → "Deploy" → "Redeploy"

### Consola (shell):
Railway dashboard → tu servicio → "Console"

---

## 💰 Costo
- **Gratis:** $5 crédito mensual
- **Consumo real:** ~$3-4/mes
- **Suficiente:** Sí, para este sistema

---

**¿Problemas?** Ve a `RAILWAY_DEPLOY.md` para guía completa.
