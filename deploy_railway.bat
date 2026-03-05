@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo    DEPLOY A RAILWAY - Sistema Paloma Valencia
echo ============================================================
echo.
echo Este script preparara el proyecto para subir a Railway
echo.
echo Pasos manuales que debes hacer:
echo.
echo 1. Crear cuenta en https://railway.app (usar GitHub)
echo 2. Crear repo en GitHub y subir este codigo:
echo    git remote add origin https://github.com/TU_USUARIO/paloma-valencia.git
necho    git push origin main
echo 3. En Railway: New Project ^> Deploy from GitHub repo
echo 4. Configurar variables de entorno en Railway
echo 5. Listo! Railway te da la URL
echo.
echo -----------------------------------------------------------
echo.

REM Verificar git
if not exist .git (
    echo Inicializando repositorio git...
    git init
    git add .
    git commit -m "Version 1.0 para Railway"
    echo.
    echo ✅ Repo git creado localmente
) else (
    echo ✅ Repo git ya existe
)

echo.
echo -----------------------------------------------------------
echo Estado actual del repo:
git status --short

echo.
echo -----------------------------------------------------------
echo Si hay cambios sin commitear:
echo   git add .
echo   git commit -m "Actualizacion"
echo   git push origin main
echo.
echo Para conectar con GitHub:
echo   git remote add origin https://github.com/TU_USUARIO/paloma-valencia.git
gecho   git push -u origin main
echo.
echo -----------------------------------------------------------
pause
