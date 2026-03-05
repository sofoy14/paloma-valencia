# 🗳️ Sistema de Monitoreo Electoral - Paloma Valencia

Sistema de monitoreo con **Agent Swarm** para cobertura completa de Colombia (32 departamentos + Bogotá DC) durante las elecciones.

**100% GRATIS** - Sin Twilio, sin costos.

---

## 🎯 Características

### 6 Agentes Especializados

| Agente | Función | Cobertura |
|--------|---------|-----------|
| **RSS Agent** | Feeds RSS | Nacionales + 13 departamentos |
| **Web Scraper Agent** | Chrome scraping | 19 departamentos sin RSS |
| **NewsAPI Agent** | API de noticias | Fuentes internacionales |
| **Google News Agent** | Búsquedas | Noticias en tiempo real |
| **Twitter/X Agent** | Redes sociales | snscrape (sin API key) |
| **Analyzer Agent** | NLP/Sentimiento | Procesamiento de contenido |

### Cobertura Territorial
- ✅ **32 departamentos** + Bogotá DC
- ✅ **50+ medios de comunicación**
- ✅ Monitoreo de **competencia electoral**
- ✅ Alertas **GRATIS** (WhatsApp/Telegram/Email)
- ✅ Reportes **Excel** cada hora

---

## 🚀 Instalación Rápida

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar notificaciones (opcional)
# Edita .env con tus datos (ver SETUP_NOTIFICACIONES.md)

# 3. Ejecutar
python app.py
# o doble clic en START.bat
```

Abrir: http://localhost:5000

---

## 📱 Configurar Notificaciones (GRATIS)

Tienes **3 opciones gratuitas**:

### Opción 1: WhatsApp via CallMeBot (Más fácil)
1. Ve a https://www.callmebot.com/blog/free-api-whatsapp-messages/
2. Escanea el QR con tu WhatsApp
3. Te darán un API key
4. Edita `.env`:
```
CALLMEBOT_APIKEY=tu_apikey
CALLMEBOT_PHONE=573174018932
```

### Opción 2: Telegram Bot (Recomendado)
1. Habla con @BotFather en Telegram
2. Crea bot nuevo (`/newbot`)
3. Habla con @userinfobot para tu Chat ID
4. Edita `.env`:
```
TELEGRAM_BOT_TOKEN=123456:ABC...
TELEGRAM_CHAT_ID=12345678
```

### Opción 3: Email (Gmail)
1. Activa 2FA en Gmail
2. Genera "App Password" en https://myaccount.google.com/security
3. Edita `.env`:
```
EMAIL_USER=tu@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
EMAIL_TO=destino@email.com
```

**Ver guía completa:** `SETUP_NOTIFICACIONES.md`

---

## ☁️ ¿Funciona en Vercel?

**No recomendado** para este sistema porque:
- ❌ No soporta SQLite (filesystem read-only)
- ❌ No puedes instalar Chrome para scraping
- ❌ WebSockets son limitados

### Alternativas en la nube (gratis):
- **Render.com** - Tiene tier gratuito (se duerme después de 15min)
- **Railway.app** - $5 crédito/mes
- **Tu PC** - Mejor opción para elecciones

**Ver guía:** `DEPLOY_CLOUD.md`

---

## 📁 Estructura del Proyecto

```
paloma-valencia/
├── agents/                    # Agentes del swarm
│   ├── rss_agent.py          # 32 departamentos
│   ├── web_scraper_agent.py  # Chrome scraping
│   ├── newsapi_agent.py
│   ├── google_news_agent.py
│   ├── twitter_agent.py
│   ├── analyzer_agent.py
│   ├── competitor_agent.py
│   ├── notifications_agent.py # WhatsApp/Telegram/Email
│   ├── excel_reporter.py
│   └── orchestrator.py
├── models/
│   └── database.py
├── static/
│   └── dashboard.html
├── reports/                   # Excel generados
├── data/                      # SQLite
├── app.py
├── requirements.txt
├── START.bat
├── SETUP_NOTIFICACIONES.md   # Guía notificaciones
├── DEPLOY_CLOUD.md           # Guía cloud
└── INSTRUCCIONES.md
```

---

## 📊 Dashboard

### Tabs disponibles:
1. **📰 Noticias** - Filtros por región y sentimiento
2. **🐦 Twitter/X** - Redes sociales
3. **🔍 Búsqueda** - Google News
4. **📊 Reportes** - Excel descargables

### Filtros:
- Por departamento (32 regiones)
- Por sentimiento (positivo/negativo/neutral)
- Por relevancia (0-100)
- Alertas prioritarias

---

## ⏰ Automatización

| Tarea | Frecuencia |
|-------|------------|
| Monitoreo | Cada 5 minutos |
| Reporte Excel | Cada hora |
| Alertas | Instantáneo |

---

## 🛡️ Tecnologías

- **Backend:** Flask, Flask-SocketIO
- **Database:** SQLite
- **Scraping:** undetected-chromedriver
- **Notifications:** CallMeBot, Telegram API, SMTP
- **Scheduling:** APScheduler
- **Frontend:** HTML5, Chart.js, Socket.IO

---

## 🔧 Troubleshooting

### "No llegan notificaciones"
1. Revisa que configuraste `.env` correctamente
2. Prueba con el botón "📱 Probar" en el dashboard
3. Verifica guía en `SETUP_NOTIFICACIONES.md`

### "No aparecen noticias"
- Espera 5 minutos (primer ciclo)
- Presiona "▶️ Monitorear Ahora" en dashboard
- Verifica conexión a internet

### "Error al instalar"
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 📝 Reportes Excel

Generados automáticamente cada hora en `reports/`:

1. **Resumen** - Estadísticas
2. **Noticias** - Todas las noticias
3. **Alertas** - Solo alertas
4. **Sentimiento** - Análisis

---

## 💡 Recomendación para Elecciones

Para el **domingo de elecciones**:

1. **Usa tu computadora** (opción más simple)
2. Configura **CallMeBot** para WhatsApp (5 minutos)
3. Deja corriendo 24/7
4. Revisa WhatsApp para alertas importantes

**No necesitas pagar nada ni usar la nube.**

---

**Desarrollado para Campaña Paloma Valencia 2026** 🗳️🇨🇴
