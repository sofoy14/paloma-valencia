@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo    DEPLOY AUTOMATICO A RAILWAY - Asistente Completo
echo ============================================================
echo.
echo Este script te guiara paso a paso para subir todo a Railway
echo y que corra 24/7 sin tu PC.
echo.
echo Necesitas:
echo - Cuenta en GitHub (crear en https://github.com/signup)
echo - Tu API Key de Railway lista
echo.
pause
cls

echo.
echo ============================================================
echo    PASO 1/4: VERIFICAR ARCHIVOS
echo ============================================================
echo.

if not exist "app.py" (
    echo ERROR: No se encuentra app.py
    echo Asegurate de estar en la carpeta correcta
    pause
    exit /b 1
)

if not exist "Procfile" (
    echo Creando Procfile...
    echo web: gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 2 --timeout 120 > Procfile
)

echo ✅ Archivos verificados
echo.
pause
cls

echo.
echo ============================================================
echo    PASO 2/4: CONFIGURAR GIT Y GITHUB
echo ============================================================
echo.
echo ATENCION: Si no tienes cuenta en GitHub:
echo 1. Ve a https://github.com/signup
echo 2. Crea cuenta (toma 1 minuto)
echo 3. Luego vuelve aqui
echo.
pause

echo.
set /p github_user="Escribe tu usuario de GitHub: "

if "%github_user%"=="" (
    echo ERROR: Usuario requerido
    pause
    exit /b 1
)

echo.
echo Configurando Git...
git config user.email "deploy@paloma.valencia"
git config user.name "Deploy Bot"

echo.
echo Conectando con GitHub...
git remote remove origin 2>nul
git remote add origin https://github.com/%github_user%/paloma-valencia.git

echo.
echo Preparando codigo...
git add -A
git commit -m "Version lista para Railway - Deploy automatico"

echo.
echo Subiendo a GitHub...
git branch -M main
git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ ERROR AL SUBIR A GITHUB
    echo.
    echo Posibles causas:
    echo 1. No has creado el repositorio en GitHub
    echo 2. El nombre del repo no es 'paloma-valencia'
    echo.
    echo SOLUCION:
    echo 1. Ve a https://github.com/new
echo    2. Nombre del repo: paloma-valencia
echo    3. NO marques README ni .gitignore
echo    4. Click "Create repository"
echo    5. Vuelve a ejecutar este script
echo.
    pause
    exit /b 1
)

echo.
echo ✅ Codigo subido a GitHub exitosamente!
echo.
pause
cls

echo.
echo ============================================================
echo    PASO 3/4: DEPLOY EN RAILWAY
echo ============================================================
echo.
echo Ahora Railway se abrira en tu navegador.
echo.
echo SIGUE ESTOS PASOS:
echo 1. Inicia sesion con tu cuenta de GitHub
echo 2. Click "Deploy from GitHub repo"
echo 3. Selecciona "paloma-valencia"
echo 4. Click "Deploy"
echo 5. Espera 2 minutos a que termine
echo.
pause

echo Abriendo Railway...
start https://railway.app/new

echo.
echo Cuando termines el deploy en Railway, presiona cualquier tecla
echo para continuar con la configuracion de variables...
pause >nul
cls

echo.
echo ============================================================
echo    PASO 4/4: CONFIGURAR VARIABLES
echo ============================================================
echo.
echo En Railway, ve a tu proyecto y:
echo 1. Click en la pestaña "Variables"
echo 2. Agrega estas variables:
echo.
echo    CALLMEBOT_APIKEY=(tu apikey de callmebot o dejar vacio)
echo    CALLMEBOT_PHONE=573174018932
echo    PYTHONUNBUFFERED=1
echo.
echo Opcionales (para mas notificaciones):
echo    TELEGRAM_BOT_TOKEN=(tu token)
echo    TELEGRAM_CHAT_ID=(tu chat id)
echo.
echo 3. Click en "Deploy" para aplicar cambios
echo.
pause
cls

echo.
echo ============================================================
echo    DEPLOY COMPLETADO! 🎉
echo ============================================================
echo.
echo Tu sistema estara disponible en:
echo https://paloma-valencia.up.railway.app
echo.
echo (Railway te dara la URL exacta)
echo.
echo ✅ El sistema correra 24/7 sin tu PC
echo.
echo Para actualizar el codigo mas tarde:
echo   1. Haz cambios en los archivos
echo   2. Ejecuta: git add . ^&^& git commit -m "Actualizacion" ^&^& git push
echo   3. Railway se actualizara automaticamente
echo.
pause
