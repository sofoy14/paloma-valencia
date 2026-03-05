@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo    CONTINUAR DEPLOY - PASO 2: SUBIR A GITHUB
echo ============================================================
echo.

cd /d D:\Projects\paloma-valencia

echo Subiendo codigo a GitHub...
git push -u origin main

if errorlevel 1 (
    echo.
    echo ❌ ERROR: No se pudo subir
    echo Asegurate de haber creado el repo en GitHub (sin README)
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ Codigo subido exitosamente!
echo.
pause
cls

echo.
echo ============================================================
echo    PASO 3: DEPLOY EN RAILWAY
echo ============================================================
echo.
echo Abriendo Railway...
start https://railway.app/new

echo.
echo INSTRUCCIONES:
echo 1. Click "Deploy from GitHub repo"
echo 2. Selecciona "paloma-valencia"
echo 3. Click "Deploy"
echo 4. Espera 2 minutos
echo 5. Ve a "Variables" y agrega:
echo    CALLMEBOT_APIKEY=tu_apikey
echo    CALLMEBOT_PHONE=573174018932
echo    PYTHONUNBUFFERED=1
echo 6. Listo! Tu URL sera: https://paloma-valencia.up.railway.app
echo.
pause
