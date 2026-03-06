# 🕊️ Paloma Valencia - Monitor Electoral

Monitor de noticias electorales para la campaña de Paloma Valencia - Elecciones Colombia 2026.

## Despliegue en Vercel

```bash
# 1. Instalar Vercel CLI
npm i -g vercel

# 2. Login
vercel login

# 3. Desplegar
vercel --prod
```

## Estructura

```
api/
  index.py    # Health check
  news.py     # Endpoint de noticias
static/
  dashboard-vercel.html  # Dashboard
  app-vercel.js         # Frontend
```

## Funcionalidad

- **RSS**: Fuentes de El Tiempo, El Espectador, Semana, etc.
- **NewsAPI**: Noticias por keywords
- **Google News**: Búsquedas políticas
- **Sin base de datos**: Todo en memoria, cliente guarda en localStorage
- **Sin procesos background**: Se ejecuta on-demand cuando el usuario visita
