# 📱 Configuración de Notificaciones GRATIS

El sistema ahora usa **notificaciones 100% gratuitas**. Puedes elegir entre 3 opciones:

---

## 🥇 OPCIÓN 1: WhatsApp via CallMeBot (Más fácil)

**Ventajas:**
- ✅ Gratis para siempre
- ✅ Llega directo a tu WhatsApp
- ✅ Muy fácil de configurar

**Pasos:**

1. **Abre tu navegador** y ve a:
   ```
   https://www.callmebot.com/blog/free-api-whatsapp-messages/
   ```

2. **Escanea el QR** con tu WhatsApp (el mismo que usas para WhatsApp Web)

3. **Te darán un API key** como este:
   ```
   1234567
   ```

4. **Edita el archivo `.env`** y pega tu API key:
   ```
   CALLMEBOT_APIKEY=1234567
   CALLMEBOT_PHONE=573174018932
   ```

5. **Reinicia el sistema** y listo!

---

## 🥈 OPCIÓN 2: Telegram Bot (Más confiable)

**Ventajas:**
- ✅ 100% gratis, sin límites
- ✅ Más confiable que WhatsApp
- ✅ Soporta mensajes largos
- ✅ No necesitas escanear QR

**Pasos:**

1. **Abre Telegram** y busca: `@BotFather`

2. **Escribe:** `/newbot`

3. **Elige un nombre:** `Paloma Valencia Alerts`

4. **Elige un username** (debe terminar en bot):
   ```
   paloma_valencia_bot
   ```

5. **Te darán un token** como este:
   ```
   123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

6. **Para obtener tu Chat ID**, busca: `@userinfobot` en Telegram

7. **Edita `.env`:**
   ```
   TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
   TELEGRAM_CHAT_ID=12345678
   ```

---

## 🥉 OPCIÓN 3: Email (Gmail)

**Ventajas:**
- ✅ Llega a cualquier email
- ✅ Formato HTML bonito
- ✅ Archivo adjunto (opcional)

**Pasos:**

1. **Activa verificación 2FA** en tu Gmail

2. **Genera "App Password":**
   - Ve a: https://myaccount.google.com/security
   - Busca "Contraseñas de aplicaciones"
   - Genera una nueva para "Otra (nombre personalizado)"
   - Ponle nombre: "Monitoreo Paloma"

3. **Te darán una contraseña** como:
   ```
   abcd efgh ijkl mnop
   ```

4. **Edita `.env`:**
   ```
   EMAIL_USER=tu_email@gmail.com
   EMAIL_PASSWORD=abcd efgh ijkl mnop
   EMAIL_TO=paloma.campana@email.com
   ```

---

## ✅ Verificar Configuración

1. **Inicia el sistema:**
   ```bash
   python app.py
   ```

2. **Abre el dashboard:** http://localhost:5000

3. **Presiona el botón "📱 Probar"**

4. **Deberías recibir** un mensaje de prueba

---

## 🆘 Si no llegan las notificaciones

### CallMeBot no funciona:
- Verifica que escaneaste el QR correctamente
- Revisa que el número de teléfono esté en formato internacional (573174018932)
- Espera 1 minuto y prueba de nuevo

### Telegram no funciona:
- Asegúrate de haber iniciado el bot (envía `/start` a tu bot)
- Verifica que el Chat ID sea correcto
- El token debe ser exacto

### Email no funciona:
- Usa "App Password", NO tu contraseña normal de Gmail
- Verifica que tienes 2FA activado en Gmail

---

## 🚀 Todas las opciones a la vez

Puedes configurar **las 3 opciones simultáneamente** y el sistema enviará por todas:

```
# WhatsApp
CALLMEBOT_APIKEY=1234567
CALLMEBOT_PHONE=573174018932

# Telegram
TELEGRAM_BOT_TOKEN=123456789:ABC...
TELEGRAM_CHAT_ID=12345678

# Email
EMAIL_USER=tu@gmail.com
EMAIL_PASSWORD=abcd efgh ijkl mnop
EMAIL_TO=paloma@email.com
```

---

**¿Preguntas?** Revisa el archivo `INSTRUCCIONES.md` para más detalles.
