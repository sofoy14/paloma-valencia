# 📰 RSS Feeds de Medios Colombianos - Estado Actual (Marzo 2025)

## Resumen Ejecutivo

Después de investigar exhaustivamente los RSS feeds de los principales medios colombianos, encontré que **la mayoría han descontinuado sus feeds RSS tradicionales**. A continuación presento el estado detallado de cada medio y las alternativas disponibles.

---

## ✅ MEDIOS CON RSS FUNCIONAL

### 1. **PULZO** ✅ RSS Activo
| Aspecto | Detalle |
|---------|---------|
| **RSS URL** | `https://www.pulzo.com/rss/new/news/ultimas-noticias.xml` |
| **Secciones disponibles** | últimas-noticias, nacion, mundo, politica, deportes, entretenimiento, tecnologia |
| **Estado** | ✅ Funcional y actualizado |
| **Método recomendado** | feedparser |

**URLs de RSS por sección:**
- Últimas noticias: `https://www.pulzo.com/rss/new/news/ultimas-noticias.xml`
- Nación: `https://www.pulzo.com/rss/new/news/nacion.xml`
- Política: `https://www.pulzo.com/rss/new/news/politica.xml`
- Mundo: `https://www.pulzo.com/rss/new/news/mundo.xml`
- Deportes: `https://www.pulzo.com/rss/new/news/deportes.xml`

---

### 2. **RCN RADIO** ✅ RSS Activo
| Aspecto | Detalle |
|---------|---------|
| **RSS URL** | `https://www.rcnradio.com/rss.xml` |
| **Estado** | ✅ Funcional y actualizado |
| **Método recomendado** | feedparser |

---

### 3. **NOTICIAS CARACOL** ⚠️ Sitemap disponible
| Aspecto | Detalle |
|---------|---------|
| **RSS tradicional** | ❌ No disponible (404) |
| **Sitemap URL** | `https://www.noticiascaracol.com/sitemap.xml` |
| **Sitemap latest** | `https://www.noticiascaracol.com/sitemap-latest.xml` |
| **Estado** | ⚠️ Sin RSS, pero con sitemap activo |
| **Método recomendado** | Parsing XML del sitemap + scraping |

---

### 4. **BLU RADIO** ⚠️ Sitemap disponible
| Aspecto | Detalle |
|---------|---------|
| **RSS tradicional** | ❌ No disponible (404) |
| **Sitemap URL** | `https://www.bluradio.com/sitemap.xml` |
| **Sitemap latest** | `https://www.bluradio.com/sitemap-latest.xml` |
| **Estado** | ⚠️ Sin RSS, pero con sitemap activo |
| **Método recomendado** | Parsing XML del sitemap + scraping |

---

## ❌ MEDIOS SIN RSS (Requieren alternativas)

### 5. **EL TIEMPO** ❌ RSS Descontinuado
| Aspecto | Detalle |
|---------|---------|
| **RSS tradicional** | ❌ Descontinuado |
| **Página RSS** | `https://www.eltiempo.com/rss` (informativa, no feed) |
| **Estado** | 🔴 No funciona - redirige a página informativa |
| **Alternativa 1** | Google News RSS: `https://news.google.com/rss/search?q=site:eltiempo.com&hl=es-419&gl=CO` |
| **Alternativa 2** | Web scraping directo |
| **Alternativa 3** | Sitemap (si está disponible) |

---

### 6. **EL ESPECTADOR** ❌ RSS Descontinuado
| Aspecto | Detalle |
|---------|---------|
| **RSS tradicional** | ❌ Descontinuado (404) |
| **Feed antiguo** | `https://www.elespectador.com/feed` - No funciona |
| **Estado** | 🔴 No funciona |
| **Alternativa 1** | Google News RSS: `https://news.google.com/rss/search?q=site:elespectador.com&hl=es-419&gl=CO` |
| **Alternativa 2** | Web scraping directo |

---

### 7. **SEMANA** ❌ RSS Descontinuado
| Aspecto | Detalle |
|---------|---------|
| **RSS tradicional** | ❌ Descontinuado (404) |
| **Feed antiguo** | `https://www.semana.com/feed` - No funciona |
| **Estado** | 🔴 No funciona |
| **Alternativa 1** | Google News RSS: `https://news.google.com/rss/search?q=site:semana.com&hl=es-419&gl=CO` |
| **Alternativa 2** | Web scraping directo |

---

## 🔧 MÉTODOS ALTERNATIVOS RECOMENDADOS

### Opción 1: Google News RSS (Fácil)
Para medios sin RSS propio, usar Google News como intermediario:

```python
# Ejemplo para El Tiempo
def leer_el_tiempo_gnews(tema="politica"):
    url = f"https://news.google.com/rss/search?q=site:eltiempo.com+{tema}&hl=es-419&gl=CO&ceid=CO:es-419"
    return feedparser.parse(url)
```

**Ventajas:**
- No requiere scraping
- Formato RSS estándar
- Funciona con cualquier medio indexado por Google

**Desventajas:**
- Delay de indexación (15-30 minutos)
- No todas las noticias aparecen
- Dependencia de Google

---

### Opción 2: Sitemap XML (Medio)
Muchos sitios tienen sitemaps que listan todas las URLs:

```python
import xml.etree.ElementTree as ET

def parse_sitemap(url):
    response = requests.get(url)
    root = ET.fromstring(response.content)
    urls = [elem.text for elem in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    return urls
```

**Funciona con:**
- ✅ Noticias Caracol
- ✅ Blu Radio
- ✅ La mayoría de sitios WordPress

---

### Opción 3: Web Scraping (Avanzado)
Extraer directamente del HTML:

```python
import requests
from bs4 import BeautifulSoup

def scrap_noticias(url):
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = soup.find_all('article')
    return articles
```

**Consideraciones:**
- Requiere mantenimiento (cambios en el HTML)
- Posibles bloqueos por rate limiting
- Requiere identificar selectores CSS específicos

---

## 📋 TABLA RESUMEN

| Medio | RSS | Sitemap | Google News | Scraping | Recomendación |
|-------|-----|---------|-------------|----------|---------------|
| **Pulzo** | ✅ | ❓ | ✅ | ✅ | Usar RSS nativo |
| **RCN Radio** | ✅ | ❓ | ✅ | ✅ | Usar RSS nativo |
| **Noticias Caracol** | ❌ | ✅ | ✅ | ✅ | Usar Sitemap + Scraping |
| **Blu Radio** | ❌ | ✅ | ✅ | ✅ | Usar Sitemap + Scraping |
| **El Tiempo** | ❌ | ❓ | ✅ | ✅ | Usar Google News |
| **El Espectador** | ❌ | ❓ | ✅ | ✅ | Usar Google News |
| **Semana** | ❌ | ❓ | ✅ | ✅ | Usar Google News |

---

## 🚀 CÓDIGO DE EJEMPLO

```python
import feedparser

# 1. RSS Nativo - Pulzo (Funciona ✅)
feed = feedparser.parse("https://www.pulzo.com/rss/new/news/politica.xml")
for entry in feed.entries[:5]:
    print(f"{entry.title} - {entry.link}")

# 2. RSS Nativo - RCN Radio (Funciona ✅)
feed = feedparser.parse("https://www.rcnradio.com/rss.xml")
for entry in feed.entries[:5]:
    print(f"{entry.title} - {entry.link}")

# 3. Google News - El Tiempo (Alternativa)
feed = feedparser.parse(
    "https://news.google.com/rss/search?q=site:eltiempo.com+politica&hl=es-419&gl=CO&ceid=CO:es-419"
)
for entry in feed.entries[:5]:
    print(f"{entry.title} - {entry.link}")
```

---

## 📦 DEPENDENCIAS REQUERIDAS

```bash
pip install feedparser requests beautifulsoup4 lxml
```

---

## ⚠️ NOTAS IMPORTANTES

1. **Términos de uso**: Algunos medios prohíben el scraping en sus Términos de Servicio. El Tiempo explícitamente reserva el derecho de desactivar RSS.

2. **Rate limiting**: Al hacer scraping, respetar los rate limits (1-2 segundos entre requests).

3. **RSS vs API**: Algunos medios ofrecen APIs pagadas (como El Tiempo) como alternativa a RSS.

4. **Actualización**: Los feeds RSS suelen actualizarse cada 15-30 minutos.

---

## 🔗 RECURSOS ADICIONALES

- **Feedparser docs**: https://feedparser.readthedocs.io/
- **BeautifulSoup docs**: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- **Google News RSS**: https://news.google.com/rss
- **Sitemap protocol**: https://www.sitemaps.org/protocol.html

---

*Investigación realizada: Marzo 2025*
*Última verificación de URLs: 2026-03-04*
