# 🤖 Agent Swarm - Monitoreo Electoral Paloma Valencia

Sistema de monitoreo de noticias con **Agent Swarm** para cobertura completa de Colombia (32 departamentos + Bogotá DC) durante las elecciones.

**✅ 100% GRATIS** | **✅ 32 Departamentos** | **✅ Alertas WhatsApp/Telegram**

---

## 🚀 ¿Cómo compartir con tu equipo?

Tienes **4 opciones** según tus necesidades:

| Opción | Costo | Dificultad | Ideal para |
|--------|-------|------------|------------|
| **ngrok** | $0 | ⭐ Fácil | Día de elecciones (temporal) |
| **Render** | $0 | ⭐⭐ Media | Siempre disponible (se duerme) |
| **VPS $5** | $5/mes | ⭐⭐⭐ Difícil | Profesional permanente |
| **Tu PC** | $0 | ⭐ Fácil | Solo tú (local) |

**📖 Guía completa:** [`COMPARTIR_SISTEMA.md`](COMPARTIR_SISTEMA.md)

**⚡ Rápido para HOY:**
```bash
# 1. Instalar ngrok (https://ngrok.com/download)
# 2. Iniciar sistema
python app.py

# 3. En otra terminal
ngrok http 5000

# 4. Comparte la URL que ngrok te da
# Ejemplo: https://abc123.ngrok-free.app
```

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

### Cobertura: 32 Departamentos + Bogotá DC

**Con RSS (13):** Antioquia, Atlántico, Bolívar, Caldas, Casanare, Cesar, Chocó, Huila, Magdalena, Risaralda, Valle del Cauca, Amazonas, Bogotá DC

**Con Web Scraper (20):** Arauca, Boyacá, Caquetá, Cauca, Córdoba, Cundinamarca, Guainía, Guaviare, La Guajira, Meta, Nariño, Norte de Santander, Putumayo, Quindío, Santander, Sucre, Tolima, Vaupés, Vichada

---

## 📱 Configurar Notificaciones (GRATIS)

Tienes **3 opciones gratuitas**:

### Opción 1: WhatsApp via CallMeBot (Más fácil)
1. Ve a https://www.callmebot.com/blog/free-api-whatsapp-messages/
2. Escanea el QR con tu WhatsApp
3. Edita `.env`:
```
CALLMEBOT_APIKEY=tu_apikey
CALLMEBOT_PHONE=573174018932
```

### Opción 2: Telegram Bot
1. Habla con @BotFather en Telegram → `/newbot`
2. Habla con @userinfobot para tu Chat ID
3. Edita `.env`:
```
TELEGRAM_BOT_TOKEN=token_aqui
TELEGRAM_CHAT_ID=chat_id_aqui
```

### Opción 3: Gmail
```
EMAIL_USER=tu@gmail.com
EMAIL_PASSWORD=app_password_aqui
```

**📖 Guía completa:** [`SETUP_NOTIFICACIONES.md`](SETUP_NOTIFICACIONES.md)

---

## ⚡ Instalación Rápida

### Opción A: Windows (doble clic)
```
1. Descargar todo el proyecto
2. Doble clic en START.bat
```

### Opción B: Línea de comandos
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python app.py
```

Abrir: http://localhost:5000

---

## 📊 Dashboard

### Funcionalidades:
- ✅ Monitoreo en tiempo real (WebSocket)
- ✅ Filtros por **32 departamentos**
- ✅ Filtros por sentimiento (positivo/negativo/neutral)
- ✅ Indicador de relevancia (0-100)
- ✅ Alertas visuales para noticias críticas
- ✅ Tab de Twitter/X con métricas de engagement
- ✅ Descarga de reportes Excel
- ✅ Búsqueda manual en Google News

### Tabs:
1. **📰 Noticias** - 32 departamentos + filtros
2. **🐦 Twitter/X** - Redes sociales
3. **🔍 Búsqueda** - Google News
4. **📊 Reportes** - Excel descargables

---

## ⏰ Automatización

| Tarea | Frecuencia |
|-------|------------|
| Monitoreo noticias | Cada 5 minutos |
| Reporte Excel | Cada hora en `/reports/` |
| Alertas | Instantáneo si hay relevancia ≥35 |

---

## 📁 Estructura

```
paloma-valencia/
├── agents/                    # 10 agentes del swarm
│   ├── rss_agent.py          # 32 departamentos
│   ├── web_scraper_agent.py  # Chrome scraping
│   ├── newsapi_agent.py
│   ├── google_news_agent.py
│   ├── twitter_agent.py
│   ├── analyzer_agent.py
│   ├── competitor_agent.py
│   ├── notifications_agent.py # WhatsApp/Telegram/Email
│   ├── excel_reporter.py
│   └── orchestrator.py       # Coordina el swarm
├── static/dashboard.html     # Dashboard web
├── app.py                    # Servidor principal
├── requirements.txt
├── START.bat                 # Ejecutor Windows
├── ngrok_start.bat          # Iniciar con ngrok
├── Dockerfile               # Para cloud
├── render.yaml              # Config Render.com
├── COMPARTIR_SISTEMA.md     # Guía para compartir
├── SETUP_NOTIFICACIONES.md  # Guía notificaciones
└── INSTRUCCIONES.md         # Guía completa
```

---

## 🛡️ Tecnologías

- **Backend:** Flask, Flask-SocketIO, APScheduler
- **Database:** SQLite
- **Scraping:** undetected-chromedriver (Chrome sin detección)
- **Notifications:** CallMeBot API, Telegram API, SMTP
- **Frontend:** HTML5, Chart.js, Socket.IO

---

## 🆘 Solución de Problemas

### "No llegan notificaciones"
1. Revisa archivo `.env` configurado
2. Prueba botón "📱 Probar" en dashboard
3. Verifica [`SETUP_NOTIFICACIONES.md`](SETUP_NOTIFICACIONES.md)

### "No aparecen noticias"
- Espera 5 minutos (primer ciclo)
- Presiona "▶️ Monitorear Ahora" en dashboard

### "ngrok no funciona"
- Asegúrate de tener cuenta en ngrok.com
- Ejecuta: `ngrok config add-authtoken TU_TOKEN`

---

## 💡 Recomendación para Elecciones

### Día de elecciones (domingo):

**La noche anterior:**
```bash
# Probar todo
python app.py
ngrok http 5000
```

**Durante el día:**
1. Mantén tu laptop encendida
2. Inicia sistema: `python app.py`
3. Inicia ngrok: `ngrok http 5000` 
4. Comparte la URL en el grupo de comando
5. Recibe alertas en tu celular

### Ventajas de esta configuración:
- ✅ **Gratis** (ngrok + CallMeBot)
- ✅ **Rápido** (5 minutos de setup)
- ✅ **Escalable** (comparte URL con todo el equipo)
- ✅ **Confiable** (todo el poder de tu PC)

---

## 📞 Soporte

Archivos de ayuda:
- [`INSTRUCCIONES.md`](INSTRUCCIONES.md) - Guía completa
- [`COMPARTIR_SISTEMA.md`](COMPARTIR_SISTEMA.md) - Cómo compartir
- [`SETUP_NOTIFICACIONES.md`](SETUP_NOTIFICACIONES.md) - Configurar alertas
- [`DEPLOY_CLOUD.md`](DEPLOY_CLOUD.md) - Deploy en la nube

---

**Desarrollado para Campaña Paloma Valencia 2026** 🗳️🇨🇴

**¿Preguntas?** Revisa los archivos .md o ejecuta `test_complete.py`
