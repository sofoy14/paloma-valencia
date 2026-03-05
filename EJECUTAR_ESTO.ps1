# Script para completar el deploy a Railway
# Ejecutar esto en PowerShell

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   COMPLETAR DEPLOY A RAILWAY" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$githubUser = Read-Host "1. Escribe tu usuario de GitHub"

if (-not $githubUser) {
    Write-Host "ERROR: Necesito tu usuario de GitHub" -ForegroundColor Red
    exit 1
}

$repoUrl = "https://github.com/$githubUser/paloma-valencia.git"

Write-Host ""
Write-Host "2. Configurando Git..." -ForegroundColor Yellow

# Configurar git
Set-Location D:\Projects\paloma-valencia
git config user.email "deploy@paloma.valencia"
git config user.name "Deploy Bot"

Write-Host "   Conectando con GitHub..." -ForegroundColor Gray
git remote remove origin 2>$null
git remote add origin $repoUrl

Write-Host "   Subiendo codigo..." -ForegroundColor Gray
git branch -M main
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host "   CODIGO SUBIDO A GITHUB!" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "AHORA VE A RAILWAY:" -ForegroundColor Yellow
    Write-Host "  1. Abre: https://railway.app/new" -ForegroundColor White
    Write-Host "  2. Click: 'Deploy from GitHub repo'" -ForegroundColor White
    Write-Host "  3. Selecciona: paloma-valencia" -ForegroundColor White
    Write-Host "  4. Click: 'Deploy'" -ForegroundColor White
    Write-Host ""
    Write-Host "LUEGO CONFIGURA VARIABLES:" -ForegroundColor Yellow
    Write-Host "  Ve a 'Variables' y agrega:" -ForegroundColor White
    Write-Host "    CALLMEBOT_APIKEY=tu_apikey" -ForegroundColor Gray
    Write-Host "    CALLMEBOT_PHONE=573174018932" -ForegroundColor Gray
    Write-Host "    PYTHONUNBUFFERED=1" -ForegroundColor Gray
    Write-Host ""
    Write-Host "TU URL SERA:" -ForegroundColor Yellow
    Write-Host "  https://paloma-valencia.up.railway.app" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "ERROR AL SUBIR A GITHUB" -ForegroundColor Red
    Write-Host ""
    Write-Host "Asegurate de:" -ForegroundColor Yellow
    Write-Host "  1. Haber creado el repo en https://github.com/new" -ForegroundColor White
    Write-Host "  2. Que el nombre del repo sea: paloma-valencia" -ForegroundColor White
    Write-Host "  3. NO inicializar con README" -ForegroundColor White
    Write-Host ""
}

Write-Host "============================================================" -ForegroundColor Cyan
Read-Host "Presiona Enter para salir"
