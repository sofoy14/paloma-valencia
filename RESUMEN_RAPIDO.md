# ⚡ RESUMEN RÁPIDO - Sistema de Monitoreo

## 🎯 Para empezar AHORA (5 minutos)

### 1. Instalar y probar local
```bash
pip install -r requirements.txt
python app.py
```
Abre: http://localhost:5000

### 2. Compartir con tu equipo (ngrok)
```bash
# Terminal 1
python app.py

# Terminal 2  
ngrok http 5000

# Copia la URL https://xxxx.ngrok-free.app
# Compártela por WhatsApp
```

### 3. Recibir alertas en tu celular
1. Ve a https://www.callmebot.com
2. Escanea QR con tu WhatsApp
3. Pega el API key en archivo `.env`
4. Listo!

---

## 📂 Archivos importantes

| Archivo | Para qué sirve |
|---------|----------------|
| `START.bat` | Iniciar sistema en Windows |
| `ngrok_start.bat` | Iniciar sistema + compartir |
| `app.py` | Servidor principal |
| `.env` | Configuración (API keys, teléfono) |
| `COMPARTIR_SISTEMA.md` | Cómo compartir con otros |
| `SETUP_NOTIFICACIONES.md` | Configurar WhatsApp/Telegram |

---

## 🔧 Comandos útiles

```bash
# Probar que todo funciona
python test_complete.py

# Iniciar sistema
python app.py

# Iniciar con ngrok (compartir)
python app.py
# (en otra terminal)
ngrok http 5000

# Ver reportes Excel
ls reports/
```

---

## 📱 Configuración mínima para funcionar

Edita archivo `.env`:

```
# WhatsApp (CallMeBot) - GRATIS
CALLMEBOT_APIKEY=1234567
CALLMEBOT_PHONE=573174018932

# Opcional - Telegram
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

# Opcional - NewsAPI
NEWS_API_KEY=
```

---

## 🚨 Checklist día de elecciones

- [ ] Laptop encendida y cargada
- [ ] Internet estable (o datos móviles)
- [ ] Sistema funcionando (`python app.py`)
- [ ] ngrok activo (`ngrok http 5000`)
- [ ] URL compartida con el equipo
- [ ] WhatsApp configurado (recibiendo alertas)
- [ ] Probar botón "📱 Probar" en dashboard

---

## 💡 Tips

1. **Si ngrok falla:** Crea cuenta gratis en ngrok.com y configura authtoken
2. **Si no llegan notificaciones:** Usa Telegram en vez de WhatsApp (más confiable)
3. **Para acceso permanente:** Usa Render.com (gratis) o VPS $5/mes
4. **Backup:** Los datos se guardan en `data/news.db` (SQLite)

---

**¿Algo no funciona?** Revisa `INSTRUCCIONES.md` o ejecuta `test_complete.py`
