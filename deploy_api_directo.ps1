# Script para deployar a Railway usando la API directamente
# API Key: f59bca07-45cd-46db-a200-726f1b20b25f

$API_KEY = "f59bca07-45cd-46db-a200-726f1b20b25f"
$HEADERS = @{
    "Authorization" = "Bearer $API_KEY"
    "Content-Type" = "application/json"
}

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   DEPLOY A RAILWAY VIA API" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Paso 1: Verificar API Key
Write-Host "[1/5] Verificando API Key..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "https://backboard.railway.app/graphql/v2" -Method POST -Headers $HEADERS -Body '{"query": "query { me { id name email } }"}' -ErrorAction Stop
    Write-Host "   ✅ Logueado como: $($response.data.me.name)" -ForegroundColor Green
    Write-Host "   📧 Email: $($response.data.me.email)" -ForegroundColor Gray
} catch {
    Write-Host "   ❌ Error: API Key invalida o sin permisos" -ForegroundColor Red
    Write-Host "   Error: $_" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[2/5] Creando proyecto..." -ForegroundColor Yellow

# Crear proyecto
$createProjectMutation = @"
{
  "query": "mutation { projectCreate(input: { name: \"paloma-monitoreo\" }) { id name } }"
}
"@

try {
    $projectResponse = Invoke-RestMethod -Uri "https://backboard.railway.app/graphql/v2" -Method POST -Headers $HEADERS -Body $createProjectMutation
    $PROJECT_ID = $projectResponse.data.projectCreate.id
    Write-Host "   ✅ Proyecto creado: $($projectResponse.data.projectCreate.name)" -ForegroundColor Green
    Write-Host "   🆔 ID: $PROJECT_ID" -ForegroundColor Gray
} catch {
    Write-Host "   ⚠️  El proyecto puede ya existir o hubo un error" -ForegroundColor Yellow
    Write-Host "   Error: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "[3/5] Configuracion necesaria:" -ForegroundColor Yellow
Write-Host ""
Write-Host "   Para completar el deploy necesitas:" -ForegroundColor White
Write-Host ""
Write-Host "   1. Ve a: https://railway.app/dashboard" -ForegroundColor Cyan
Write-Host "   2. Busca el proyecto 'paloma-monitoreo'" -ForegroundColor White
Write-Host "   3. Click en 'New' -> 'Empty Service'" -ForegroundColor White
Write-Host "   4. En el servicio, ve a 'Settings'" -ForegroundColor White
Write-Host "   5. Cambia 'Source' a 'GitHub'" -ForegroundColor White
Write-Host "   6. Conecta tu repo de GitHub" -ForegroundColor White
Write-Host ""
Write-Host "   O usa el CLI:" -ForegroundColor White
Write-Host "   npm install -g @railway/cli" -ForegroundColor Gray
Write-Host "   railway login" -ForegroundColor Gray
Write-Host "   railway init" -ForegroundColor Gray
Write-Host "   railway up" -ForegroundColor Gray

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   INSTRUCCIONES ALTERNATIVAS" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "OPCION A: Deploy manual via web (RECOMENDADO)" -ForegroundColor Green
Write-Host "   1. Sube el codigo a GitHub" -ForegroundColor White
Write-Host "   2. Ve a https://railway.app/new" -ForegroundColor White  
Write-Host "   3. Selecciona 'Deploy from GitHub repo'" -ForegroundColor White
Write-Host "   4. Elige tu repo" -ForegroundColor White
Write-Host "   5. Click 'Deploy'" -ForegroundColor White
Write-Host ""
Write-Host "OPCION B: Usar CLI de Railway" -ForegroundColor Green
Write-Host "   1. npm install -g @railway/cli" -ForegroundColor Gray
Write-Host "   2. railway login" -ForegroundColor Gray
Write-Host "   3. railway init --name paloma-monitoreo" -ForegroundColor Gray
Write-Host "   4. railway up" -ForegroundColor Gray
Write-Host ""

# Crear archivo de configuracion
$configContent = @"
# Configuracion para Railway
# Guarda estas variables en Railway dashboard -> Variables

CALLMEBOT_APIKEY=tu_apikey_aqui
CALLMEBOT_PHONE=573174018932
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
NEWS_API_KEY=
PYTHONUNBUFFERED=1
"@

$configContent | Out-File -FilePath ".env.railway.example" -Encoding UTF8
Write-Host "✅ Archivo .env.railway.example creado con las variables necesarias" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
