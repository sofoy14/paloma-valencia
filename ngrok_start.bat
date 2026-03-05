@echo off
chcp 65001 >nul
echo.
echo ============================================================
echo    INICIAR SISTEMA + NGROK (Para compartir con otros)
echo ============================================================
echo.
echo Este script iniciara:
echo   1. El sistema de monitoreo (localhost:5000)
echo   2. ngrok (tunnel publico)
echo.
echo NOTA: Asegurate de tener ngrok instalado y configurado
echo       https://ngrok.com/download
echo.
pause

start "Sistema Monitoreo" cmd /k "python app.py"
timeout /t 5 /nobreak

echo.
echo Iniciando ngrok...
echo.
ngrok http 5000

echo.
echo ============================================================
echo Si ngrok no inicio, instala desde: https://ngrok.com/download
echo ============================================================
pause
