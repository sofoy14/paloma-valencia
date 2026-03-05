# ☁️ Despliegue en la Nube (Opcional)

El sistema **funciona perfectamente en tu computadora local**. Pero si necesitas ponerlo en la nube, aquí tienes opciones gratis:

---

## ⚠️ IMPORTANTE: Limitaciones

El sistema usa **Chrome para scraping** y **SQLite para base de datos**. Esto limita las opciones gratuitas:

| Servicio | Chrome | SQLite | Cron Jobs | Opinión |
|----------|--------|--------|-----------|---------|
| **Vercel** | ❌ No | ❌ Read-only | ⚠️ Limitado | ❌ No recomendado |
| **Render** | ✅ Sí | ✅ Sí | ✅ Sí | ✅ **Recomendado** |
| **Railway** | ✅ Sí | ✅ Sí | ✅ Sí | ✅ Bueno |
| **PythonAnywhere** | ⚠️ Limitado | ✅ Sí | ✅ Sí | ⚠️ Complicado |

---

## 🥇 OPCIÓN RECOMENDADA: Render.com (Gratis)

### Pasos:

1. **Crea cuenta** en https://render.com

2. **Crea un "Web Service"** nuevo

3. **Conecta tu repo** de GitHub o sube los archivos

4. **Configuración:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Plan:** Free

5. **Variables de entorno:**
   Agrega todas las de tu archivo `.env`

6. **Crear "Disk" para persistencia:**
   - Ve a "Disks" en el dashboard
   - Crea un disco de 1GB
   - Mount path: `/opt/render/project/src/data`

7. **Deploy!**

### Limitaciones del plan gratis:
- Se "duerme" después de 15 min de inactividad
- Se despierta en ~30 segundos cuando hay tráfico
- 750 horas/mes (suficiente para 1 app)

---

## 🥈 OPCIÓN 2: Railway.app (Gratis)

1. **Crea cuenta** en https://railway.app

2. **Nuevo proyecto** → Deploy from GitHub

3. **Railway detectará automáticamente** que es Python

4. **Agrega variables de entorno** en la sección "Variables"

5. **Deploy!**

### Limitaciones:
- $5 de crédito gratis/mes
- Se consume rápido si hay mucho tráfico
- Mejor para corto plazo

---

## 🥉 OPCIÓN 3: Dejarlo en tu PC (Recomendado para elecciones)

Para el **domingo de elecciones**, la mejor opción es:

### Opción A: Tu laptop/PC
1. Dejar la computadora encendida
2. Conectar a internet estable
3. Ejecutar `python app.py`
4. Minimizar la ventana y listo

### Opción B: Raspberry Pi (si tienes)
1. Instalar Raspberry Pi OS
2. Instalar Python y Chrome
3. Clonar el repo
4. Ejecutar 24/7 (consume muy poca energía)

### Opción C: VPS barato (DigitalOcean, Linode)
- $5/mes
- Siempre encendido
- IP fija

---

## 🔄 Configuración de Cron Jobs (en la nube)

En Render/Railway, los cron jobs se configuran en el código (ya está hecho):

```python
# app.py - Ya incluido
scheduler.add_job(
    run_monitoring_job,
    'interval',
    minutes=5,
    id='monitoring_job'
)
```

---

## 📊 Comparativa para Elecciones

| Opción | Costo | Confiabilidad | Esfuerzo | Recomendación |
|--------|-------|---------------|----------|---------------|
| Tu PC | $0 | ⭐⭐⭐⭐ | Bajo | ✅ **Usar esto** |
| Raspberry Pi | $0 | ⭐⭐⭐⭐⭐ | Medio | ✅ Si tienes |
| Render Free | $0 | ⭐⭐⭐ | Medio | ⚠️ Se duerme |
| VPS $5/mes | $5 | ⭐⭐⭐⭐⭐ | Medio | ✅ Si puedes pagar |

---

## ✅ Recomendación Final

Para el **domingo de elecciones**:

1. **No te compliques con la nube**
2. **Usa tu computadora** o laptop vieja
3. **Conecta a un UPS** si tienes (por si hay cortes de luz)
4. **Comparte el dashboard** por ngrok si quieres acceso remoto:
   ```bash
   # Instalar ngrok
   ngrok http 5000
   # Te dará una URL tipo: https://abc123.ngrok.io
   ```

**El sistema está diseñado para funcionar localmente sin problemas.**

---

¿Quieres que te ayude a configurar ngrok para acceso remoto?
