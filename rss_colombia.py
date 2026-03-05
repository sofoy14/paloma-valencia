#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSS Feeds de Medios Colombianos
================================
Investigación de RSS feeds actuales de principales medios colombianos.
Fecha de investigación: Marzo 2025

ESTADO DE LOS RSS:
------------------
✅ FUNCIONALES:
   - Pulzo: Sí tiene RSS activo
   - RCN Radio: Sí tiene RSS activo  
   - Noticias Caracol: Sitemap disponible
   - Blu Radio: Sitemap disponible

❌ NO FUNCIONALES / DESCONTINUADOS:
   - El Tiempo: RSS descontinuado (redirige a página informativa)
   - El Espectador: RSS descontinuado (404)
   - Semana: RSS descontinuado (404)

ALTERNATIVAS RECOMENDADAS:
--------------------------
Para medios sin RSS, usar:
1. Sitemaps XML (para crawling)
2. Web scraping directo
3. Google News RSS como intermediario
"""

import feedparser
import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from datetime import datetime
import json


# ============================================================
# 1. PULZO - RSS FUNCIONAL ✅
# ============================================================

PULZO_RSS_FEEDS = {
    "ultimas_noticias": "https://www.pulzo.com/rss/new/news/ultimas-noticias.xml",
    "nacion": "https://www.pulzo.com/rss/new/news/nacion.xml",
    "mundo": "https://www.pulzo.com/rss/new/news/mundo.xml",
    "politica": "https://www.pulzo.com/rss/new/news/politica.xml",
    "deportes": "https://www.pulzo.com/rss/new/news/deportes.xml",
    "entretenimiento": "https://www.pulzo.com/rss/new/news/entretenimiento.xml",
    "tecnologia": "https://www.pulzo.com/rss/new/news/tecnologia.xml",
}


def leer_pulzo(seccion="ultimas_noticias", limite=10):
    """
    Lee noticias de Pulzo vía RSS.
    
    Args:
        seccion: Una de las claves en PULZO_RSS_FEEDS
        limite: Número máximo de noticias a retornar
    
    Returns:
        Lista de diccionarios con título, link, descripción, fecha
    """
    url = PULZO_RSS_FEEDS.get(seccion, PULZO_RSS_FEEDS["ultimas_noticias"])
    feed = feedparser.parse(url)
    
    noticias = []
    for entry in feed.entries[:limite]:
        noticias.append({
            "titulo": entry.get("title", ""),
            "link": entry.get("link", ""),
            "descripcion": entry.get("description", ""),
            "fecha": entry.get("published", ""),
            "fuente": "Pulzo"
        })
    return noticias


# ============================================================
# 2. RCN RADIO - RSS FUNCIONAL ✅
# ============================================================

RCN_RSS_URL = "https://www.rcnradio.com/rss.xml"


def leer_rcn_radio(limite=10):
    """
    Lee noticias de RCN Radio vía RSS.
    
    Args:
        limite: Número máximo de noticias a retornar
    
    Returns:
        Lista de diccionarios con título, link, descripción, fecha
    """
    feed = feedparser.parse(RCN_RSS_URL)
    
    noticias = []
    for entry in feed.entries[:limite]:
        noticias.append({
            "titulo": entry.get("title", ""),
            "link": entry.get("link", ""),
            "descripcion": entry.get("description", ""),
            "fecha": entry.get("published", ""),
            "fuente": "RCN Radio"
        })
    return noticias


# ============================================================
# 3. NOTICIAS CARACOL - SITEMAP (Alternativa a RSS)
# ============================================================

CARACOL_SITEMAP_INDEX = "https://www.noticiascaracol.com/sitemap.xml"
CARACOL_SITEMAP_LATEST = "https://www.noticiascaracol.com/sitemap-latest.xml"


def leer_caracol_sitemap(limite=10):
    """
    Lee noticias de Noticias Caracol vía sitemap XML.
    
    Args:
        limite: Número máximo de noticias a retornar
    
    Returns:
        Lista de diccionarios con link y última modificación
    """
    try:
        response = requests.get(CARACOL_SITEMAP_LATEST, timeout=10)
        response.raise_for_status()
        
        # Parsear XML
        root = ET.fromstring(response.content)
        
        # Namespace para sitemap
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        noticias = []
        for url in root.findall('ns:url', ns)[:limite]:
            loc = url.find('ns:loc', ns)
            lastmod = url.find('ns:lastmod', ns)
            
            if loc is not None:
                noticias.append({
                    "titulo": "",  # El sitemap no incluye títulos
                    "link": loc.text,
                    "descripcion": "",
                    "fecha": lastmod.text if lastmod is not None else "",
                    "fuente": "Noticias Caracol"
                })
        return noticias
    except Exception as e:
        print(f"Error leyendo sitemap de Caracol: {e}")
        return []


def leer_caracol_scraping(seccion="colombia", limite=10):
    """
    Lee noticias de Noticias Caracol vía web scraping.
    
    Args:
        seccion: Sección a leer (colombia, mundo, politica, etc.)
        limite: Número máximo de noticias a retornar
    
    Returns:
        Lista de diccionarios con título, link, descripción
    """
    url = f"https://www.noticiascaracol.com/{seccion}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        noticias = []
        # Selectores comunes para noticias (ajustar según estructura actual)
        articles = soup.find_all('article', limit=limite)
        
        for article in articles:
            # Intentar extraer título
            title_elem = article.find('h2') or article.find('h3') or article.find('a')
            link_elem = article.find('a', href=True)
            desc_elem = article.find('p')
            
            titulo = title_elem.get_text(strip=True) if title_elem else ""
            link = link_elem['href'] if link_elem else ""
            descripcion = desc_elem.get_text(strip=True) if desc_elem else ""
            
            # Asegurar que el link sea absoluto
            if link and link.startswith('/'):
                link = f"https://www.noticiascaracol.com{link}"
            
            if titulo and link:
                noticias.append({
                    "titulo": titulo,
                    "link": link,
                    "descripcion": descripcion,
                    "fecha": "",
                    "fuente": "Noticias Caracol"
                })
        
        return noticias
    except Exception as e:
        print(f"Error haciendo scraping de Caracol: {e}")
        return []


# ============================================================
# 4. BLU RADIO - SITEMAP (Alternativa a RSS)
# ============================================================

BLU_SITEMAP_LATEST = "https://www.bluradio.com/sitemap-latest.xml"


def leer_blu_sitemap(limite=10):
    """
    Lee noticias de Blu Radio vía sitemap XML.
    
    Args:
        limite: Número máximo de noticias a retornar
    
    Returns:
        Lista de diccionarios con link y última modificación
    """
    try:
        response = requests.get(BLU_SITEMAP_LATEST, timeout=10)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        noticias = []
        for url in root.findall('ns:url', ns)[:limite]:
            loc = url.find('ns:loc', ns)
            lastmod = url.find('ns:lastmod', ns)
            
            if loc is not None:
                noticias.append({
                    "titulo": "",
                    "link": loc.text,
                    "descripcion": "",
                    "fecha": lastmod.text if lastmod is not None else "",
                    "fuente": "Blu Radio"
                })
        return noticias
    except Exception as e:
        print(f"Error leyendo sitemap de Blu Radio: {e}")
        return []


# ============================================================
# 5. EL TIEMPO - GOOGLE NEWS RSS (Alternativa)
# ============================================================

EL_TIEMPO_GOOGLE_NEWS = "https://news.google.com/rss/search?q=site:eltiempo.com+colombia&hl=es-419&gl=CO&ceid=CO:es-419"
EL_TIEMPO_POLITICA_GNEWS = "https://news.google.com/rss/search?q=site:eltiempo.com+politica&hl=es-419&gl=CO&ceid=CO:es-419"


def leer_el_tiempo_google_news(tema="colombia", limite=10):
    """
    Lee noticias de El Tiempo vía Google News RSS.
    
    Args:
        tema: Tema a buscar (colombia, politica, etc.)
        limite: Número máximo de noticias a retornar
    
    Returns:
        Lista de diccionarios con título, link, descripción, fecha
    """
    url = f"https://news.google.com/rss/search?q=site:eltiempo.com+{tema}&hl=es-419&gl=CO&ceid=CO:es-419"
    feed = feedparser.parse(url)
    
    noticias = []
    for entry in feed.entries[:limite]:
        noticias.append({
            "titulo": entry.get("title", ""),
            "link": entry.get("link", ""),
            "descripcion": entry.get("description", ""),
            "fecha": entry.get("published", ""),
            "fuente": "El Tiempo (vía Google News)"
        })
    return noticias


def leer_el_tiempo_scraping(seccion="politica", limite=10):
    """
    Lee noticias de El Tiempo vía web scraping directo.
    
    Args:
        seccion: Sección a leer (politica, justicia, economia, etc.)
        limite: Número máximo de noticias a retornar
    
    Returns:
        Lista de diccionarios con título, link, descripción
    """
    url = f"https://www.eltiempo.com/{seccion}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        noticias = []
        # El Tiempo usa clases específicas
        articles = soup.find_all('article', limit=limite)
        
        for article in articles:
            title_elem = article.find('h2') or article.find('h3')
            link_elem = article.find('a', href=True)
            
            titulo = title_elem.get_text(strip=True) if title_elem else ""
            link = link_elem['href'] if link_elem else ""
            
            if link and link.startswith('/'):
                link = f"https://www.eltiempo.com{link}"
            
            if titulo and link:
                noticias.append({
                    "titulo": titulo,
                    "link": link,
                    "descripcion": "",
                    "fecha": "",
                    "fuente": "El Tiempo"
                })
        
        return noticias
    except Exception as e:
        print(f"Error haciendo scraping de El Tiempo: {e}")
        return []


# ============================================================
# 6. EL ESPECTADOR - GOOGLE NEWS / SCRAPING (Alternativa)
# ============================================================

def leer_el_espectador_google_news(tema="politica", limite=10):
    """
    Lee noticias de El Espectador vía Google News RSS.
    
    Args:
        tema: Tema a buscar (politica, judicial, economia, etc.)
        limite: Número máximo de noticias a retornar
    
    Returns:
        Lista de diccionarios con título, link, descripción, fecha
    """
    url = f"https://news.google.com/rss/search?q=site:elespectador.com+{tema}&hl=es-419&gl=CO&ceid=CO:es-419"
    feed = feedparser.parse(url)
    
    noticias = []
    for entry in feed.entries[:limite]:
        noticias.append({
            "titulo": entry.get("title", ""),
            "link": entry.get("link", ""),
            "descripcion": entry.get("description", ""),
            "fecha": entry.get("published", ""),
            "fuente": "El Espectador (vía Google News)"
        })
    return noticias


def leer_el_espectador_scraping(seccion="politica", limite=10):
    """
    Lee noticias de El Espectador vía web scraping directo.
    
    Args:
        seccion: Sección a leer (politica, judicial, economia, etc.)
        limite: Número máximo de noticias a retornar
    
    Returns:
        Lista de diccionarios con título, link, descripción
    """
    url = f"https://www.elespectador.com/{seccion}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        noticias = []
        articles = soup.find_all('article', limit=limite)
        
        for article in articles:
            title_elem = article.find('h2') or article.find('h3')
            link_elem = article.find('a', href=True)
            desc_elem = article.find('p')
            
            titulo = title_elem.get_text(strip=True) if title_elem else ""
            link = link_elem['href'] if link_elem else ""
            descripcion = desc_elem.get_text(strip=True) if desc_elem else ""
            
            if link and link.startswith('/'):
                link = f"https://www.elespectador.com{link}"
            
            if titulo and link:
                noticias.append({
                    "titulo": titulo,
                    "link": link,
                    "descripcion": descripcion,
                    "fecha": "",
                    "fuente": "El Espectador"
                })
        
        return noticias
    except Exception as e:
        print(f"Error haciendo scraping de El Espectador: {e}")
        return []


# ============================================================
# 7. SEMANA - GOOGLE NEWS / SCRAPING (Alternativa)
# ============================================================

def leer_semana_google_news(tema="colombia", limite=10):
    """
    Lee noticias de Semana vía Google News RSS.
    
    Args:
        tema: Tema a buscar
        limite: Número máximo de noticias a retornar
    
    Returns:
        Lista de diccionarios con título, link, descripción, fecha
    """
    url = f"https://news.google.com/rss/search?q=site:semana.com+{tema}&hl=es-419&gl=CO&ceid=CO:es-419"
    feed = feedparser.parse(url)
    
    noticias = []
    for entry in feed.entries[:limite]:
        noticias.append({
            "titulo": entry.get("title", ""),
            "link": entry.get("link", ""),
            "descripcion": entry.get("description", ""),
            "fecha": entry.get("published", ""),
            "fuente": "Semana (vía Google News)"
        })
    return noticias


def leer_semana_scraping(seccion="noticias", limite=10):
    """
    Lee noticias de Semana vía web scraping directo.
    
    Args:
        seccion: Sección a leer
        limite: Número máximo de noticias a retornar
    
    Returns:
        Lista de diccionarios con título, link, descripción
    """
    url = f"https://www.semana.com/{seccion}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        noticias = []
        articles = soup.find_all('article', limit=limite)
        
        for article in articles:
            title_elem = article.find('h2') or article.find('h3')
            link_elem = article.find('a', href=True)
            
            titulo = title_elem.get_text(strip=True) if title_elem else ""
            link = link_elem['href'] if link_elem else ""
            
            if link and link.startswith('/'):
                link = f"https://www.semana.com{link}"
            
            if titulo and link:
                noticias.append({
                    "titulo": titulo,
                    "link": link,
                    "descripcion": "",
                    "fecha": "",
                    "fuente": "Semana"
                })
        
        return noticias
    except Exception as e:
        print(f"Error haciendo scraping de Semana: {e}")
        return []


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def imprimir_noticias(noticias, titulo="Noticias"):
    """Imprime noticias de forma legible."""
    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")
    
    for i, noticia in enumerate(noticias, 1):
        print(f"\n{i}. {noticia['titulo']}")
        print(f"   Fuente: {noticia['fuente']}")
        print(f"   Link: {noticia['link']}")
        if noticia['descripcion']:
            print(f"   Descripción: {noticia['descripcion'][:150]}...")
        if noticia['fecha']:
            print(f"   Fecha: {noticia['fecha']}")
        print("-" * 60)


def guardar_json(noticias, filename="noticias.json"):
    """Guarda noticias en formato JSON."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(noticias, f, ensure_ascii=False, indent=2)
    print(f"\nNoticias guardadas en: {filename}")


# ============================================================
# EJEMPLOS DE USO
# ============================================================

if __name__ == "__main__":
    print("=" * 60)
    print("RSS FEEDS DE MEDIOS COLOMBIANOS")
    print("=" * 60)
    
    # 1. Pulzo - RSS Funcional
    print("\n📰 Leyendo Pulzo (RSS)...")
    noticias_pulzo = leer_pulzo("politica", 5)
    imprimir_noticias(noticias_pulzo, "PULZO - Política")
    
    # 2. RCN Radio - RSS Funcional
    print("\n📰 Leyendo RCN Radio (RSS)...")
    noticias_rcn = leer_rcn_radio(5)
    imprimir_noticias(noticias_rcn, "RCN RADIO")
    
    # 3. Noticias Caracol - Sitemap
    print("\n📰 Leyendo Noticias Caracol (Sitemap)...")
    noticias_caracol = leer_caracol_sitemap(5)
    imprimir_noticias(noticias_caracol, "NOTICIAS CARACOL - Sitemap")
    
    # 4. Blu Radio - Sitemap
    print("\n📰 Leyendo Blu Radio (Sitemap)...")
    noticias_blu = leer_blu_sitemap(5)
    imprimir_noticias(noticias_blu, "BLU RADIO - Sitemap")
    
    # 5. El Tiempo - Google News
    print("\n📰 Leyendo El Tiempo (Google News)...")
    noticias_tiempo = leer_el_tiempo_google_news("politica", 5)
    imprimir_noticias(noticias_tiempo, "EL TIEMPO - Política (vía Google News)")
    
    # 6. El Espectador - Google News
    print("\n📰 Leyendo El Espectador (Google News)...")
    noticias_espectador = leer_el_espectador_google_news("politica", 5)
    imprimir_noticias(noticias_espectador, "EL ESPECTADOR - Política (vía Google News)")
    
    # 7. Semana - Google News
    print("\n📰 Leyendo Semana (Google News)...")
    noticias_semana = leer_semana_google_news("colombia", 5)
    imprimir_noticias(noticias_semana, "SEMANA (vía Google News)")
    
    # Guardar todas las noticias
    todas = (noticias_pulzo + noticias_rcn + noticias_caracol + 
             noticias_blu + noticias_tiempo + noticias_espectador + noticias_semana)
    guardar_json(todas, "noticias_colombia.json")
