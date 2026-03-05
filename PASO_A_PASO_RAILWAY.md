# 🚀 PASO A PASO - Deploy en Railway (Sin tener la PC encendida)

Vamos a subir tu sistema a Railway para que corra 24/7 en la nube.

---

## 📋 ANTES DE EMPEZAR

Necesitas:
1. ✅ Cuenta en GitHub (gratis) → https://github.com/signup
2. ✅ Cuenta en Railway (con tu API key ya tienes) 
3. ✅ Tu API Key: `f59bca07-45cd-46db-a200-726f1b20b25f`

---

## 🐙 PASO 1: Crear Repo en GitHub (2 min)

### 1.1 Ve a GitHub
Abre: https://github.com/new

### 1.2 Configura el repo:
- **Repository name:** `paloma-valencia`
- **Description:** `Sistema de monitoreo electoral`
- ✅ Público (o privado si prefieres)
- ❌ NO marques "Add a README file"
- ❌ NO marques "Add .gitignore"
- ❌ NO marques "Choose a license"

### 1.3 Click "Create repository"

### 1.4 Copia la URL del repo
Te aparecerá algo como:
```
https://github.com/TU_USUARIO/paloma-valencia.git
```

**Guárdala, la necesitamos en el Paso 2.**

---

## 💻 PASO 2: Subir Código a GitHub (3 min)

### 2.1 Abre PowerShell en la carpeta del proyecto

### 2.2 Ejecuta estos comandos uno por uno:

```powershell
cd D:\Projects\paloma-valencia
```

```powershell
git remote add origin https://github.com/TU_USUARIO/paloma-valencia.git
```
(Reemplaza `TU_USUARIO` con tu usuario de GitHub)

```powershell
git branch -M main
```

```powershell
git push -u origin main
```

### 2.3 Verifica en GitHub
Ve a `https://github.com/TU_USUARIO/paloma-valencia`
Deberías ver todos los archivos subidos.

**✅ Listo, tu código está en la nube.**

---

## 🚄 PASO 3: Crear Proyecto en Railway (2 min)

### 3.1 Ve a Railway
Abre: https://railway.app/new

### 3.2 Selecciona fuente
Click en: **"Deploy from GitHub repo"**

### 3.3 Configura GitHub
- Click en "Configure GitHub App"
- Selecciona tu cuenta de GitHub
- Dale permiso a Railway para acceder a tus repos
- Busca y selecciona: `paloma-valencia`

### 3.4 Click "Deploy"
Railway empezará a descargar y construir tu proyecto.

**⏳ Espera ~2 minutos...**

---

## ⚙️ PASO 4: Configurar Variables (2 min)

### 4.1 Ve a Variables
En tu proyecto Railway, click en la pestaña **"Variables"**

### 4.2 Agrega las variables una por una:

Click "New Variable" y agrega:

```
Key: CALLMEBOT_APIKEY
Value: (tu apikey de callmebot)
```

```
Key: CALLMEBOT_PHONE
Value: 573174018932
```

```
Key: PYTHONUNBUFFERED
Value: 1
```

(Opcionales - si quieres más notificaciones):
```
Key: TELEGRAM_BOT_TOKEN
Value: (tu token de telegram)
```

```
Key: TELEGRAM_CHAT_ID
Value: (tu chat id)
```

### 4.3 Click "Deploy" para aplicar cambios

---

## 🌐 PASO 5: Obtener URL y Probar (1 min)

### 5.1 Ve a Settings
Click en pestaña **"Settings"**

### 5.2 Generar dominio
En "Public Networking", click **"Generate Domain"**

Railway te dará una URL como:
```
https://paloma-valencia.up.railway.app
```

### 5.3 Abre la URL en tu navegador
Deberías ver el dashboard del sistema de monitoreo.

### 5.4 Prueba el sistema
- Click en "▶️ Monitorear Ahora"
- Click en "📱 Probar" (para probar notificaciones)

**🎉 ¡Listo! Tu sistema está corriendo 24/7 en Railway.**

---

## 📱 PASO 6: Configurar Notificaciones (Opcional)

### Para recibir alertas en tu celular:

**Opción A: WhatsApp (Más fácil)**
1. Ve a https://www.callmebot.com/blog/free-api-whatsapp-messages/
2. Escanea el QR con tu WhatsApp
3. Te darán un API key (número)
4. Edita las variables en Railway y agrega `CALLMEBOT_APIKEY`

**Opción B: Telegram (Más confiable)**
1. Busca @BotFather en Telegram
2. Crea bot nuevo: `/newbot`
3. Te dará un token
4. Busca @userinfobot para tu Chat ID
5. Agrega `TELEGRAM_BOT_TOKEN` y `TELEGRAM_CHAT_ID` en Railway

---

## ✅ CHECKLIST FINAL

- [ ] Repo creado en GitHub
- [ ] Código subido a GitHub (`git push`)
- [ ] Proyecto creado en Railway
- [ ] Variables de entorno configuradas
- [ ] Dominio generado (URL pública)
- [ ] Dashboard cargando correctamente
- [ ] Botón "Probar" funcionando

---

## 🔧 COMANDOS ÚTILES

Si necesitas actualizar el código más tarde:

```powershell
cd D:\Projects\paloma-valencia

# Hacer cambios en los archivos...

# Subir cambios
git add .
git commit -m "Actualización"
git push
```

Railway se actualizará automáticamente.

---

## ⚠️ LIMITACIONES EN RAILWAY

| Característica | Estado |
|----------------|--------|
| RSS (13 deptos) | ✅ Funciona |
| NewsAPI | ✅ Funciona |
| Google News | ✅ Funciona |
| Twitter/X | ✅ Funciona |
| Dashboard | ✅ Funciona |
| Chrome Scraper | ❌ NO funciona |

**Cobertura:** ~19 departamentos (de 32)

**¿Por qué?** Railway no tiene Chrome instalado para hacer scraping.

---

## 💰 COSTO

- **Plan:** Gratuito ($5 crédito/mes)
- **Consumo:** ~$3-4/mes
- **¿Se acaba?** A fin de mes se reinicia el crédito

---

## 🆘 SI ALGO FALLA

### "Build Failed"
Revisa los logs en Railway: Dashboard → tu proyecto → "Deploy" → click en el deploy fallido.

### "Application Error"
Verifica que el `Procfile` existe y tiene:
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

### "Cannot find module"
Asegúrate que `requirements.txt` tiene todas las dependencias.

---

## 📞 SOPORTE

- Railway Discord: https://discord.gg/railway
- Railway Docs: https://docs.railway.app

---

**¿Necesitas ayuda con algún paso específico?**
