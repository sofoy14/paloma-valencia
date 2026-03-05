@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo    DEPLOY A RAILWAY CON API KEY
echo ============================================================
echo.

REM Verificar que railway CLI esta instalado
where railway >nul 2>nul
if %errorlevel% neq 0 (
    echo Instalando Railway CLI...
    npm install -g @railway/cli
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo instalar Railway CLI
        echo Por favor instala manualmente: npm install -g @railway/cli
        pause
        exit /b 1
    )
)

echo ✅ Railway CLI instalado
echo.

REM Login con browser (abrira navegador)
echo PASO 1: Login en Railway
echo Se abrira tu navegador para autorizar...
echo.
railway login
echo.

REM Verificar login
echo Verificando login...
railway whoami
echo.

REM Inicializar proyecto
echo PASO 2: Creando proyecto en Railway...
railway init --name "paloma-monitoreo"
echo.

REM Linkear proyecto local
echo PASO 3: Linkeando proyecto local...
railway link
echo.

REM Configurar variables de entorno
echo PASO 4: Configurando variables de entorno...
echo.

REM Crear archivo temporal con variables
(
echo CALLMEBOT_APIKEY=
echo CALLMEBOT_PHONE=573174018932
echo TELEGRAM_BOT_TOKEN=
echo TELEGRAM_CHAT_ID=
echo NEWS_API_KEY=
echo PYTHONUNBUFFERED=1
) > .env.railway.temp

echo Por favor edita el archivo .env.railway.temp con tus valores reales
echo Luego presiona cualquier tecla para continuar...
pause >nul

echo Cargando variables...
for /f "tokens=1,* delims=" %%a in (.env.railway.temp) do (
    railway variables set "%%a"
)

del .env.railway.temp

echo.
echo PASO 5: Deployando...
railway up

echo.
echo ============================================================
echo    DEPLOY COMPLETADO
echo ============================================================
echo.
echo Tu aplicacion deberia estar disponible en:
railway status
echo.
echo Para ver los logs:
echo   railway logs
echo.
echo Para abrir en navegador:
echo   railway open
echo.
pause
