"""
Google News Agent - Scraper de Google News Colombia
"""
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from datetime import datetime, timezone
import re
import time

class GoogleNewsAgent:
    """Agente que scrapea Google News para noticias de Colombia"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def search(self, query, hours_back=24):
        """Busca noticias en Google News"""
        articles = []
        
        try:
            # Construir URL de búsqueda
            encoded_query = quote(query)
            url = f"https://news.google.com/search?q={encoded_query}+when:1d&hl=es-419&gl=CO&ceid=CO:es-419"
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraer artículos
            article_elements = soup.find_all('article', limit=20)
            
            for element in article_elements:
                try:
                    article = self._parse_article(element)
                    if article:
                        articles.append(article)
                except Exception as e:
                    continue
            
            time.sleep(1)  # Respetar rate limit
            
        except Exception as e:
            print(f"[GoogleNews] Error: {e}")
        
        return articles
    
    def search_political(self):
        """Búsquedas predefinidas para política colombiana"""
        all_articles = []
        
        queries = [
            "Paloma Valencia senado",
            "Centro Democratico elecciones 2026",
            "Uribe Colombia política",
            "Senado Colombia elecciones",
            "Consulta interpartidista Colombia"
        ]
        
        for query in queries:
            try:
                articles = self.search(query, hours_back=24)
                all_articles.extend(articles)
                time.sleep(1.5)
            except Exception as e:
                print(f"[GoogleNews] Error en query '{query}': {e}")
        
        # Remover duplicados
        seen = set()
        unique = []
        for a in all_articles:
            key = a.get('title', '')[:50]
            if key not in seen:
                seen.add(key)
                unique.append(a)
        
        return unique
    
    def _parse_article(self, element):
        """Parsea un elemento de artículo de Google News"""
        try:
            # Título
            title_elem = element.find('a', class_=re.compile('DY5T1d|JtKRv'))
            if not title_elem:
                title_elem = element.find('h3')
            
            title = title_elem.get_text(strip=True) if title_elem else 'Sin título'
            
            # Link
            link_elem = element.find('a', href=True)
            link = link_elem['href'] if link_elem else ''
            if link.startswith('./'):
                link = 'https://news.google.com' + link[1:]
            
            # Fuente
            source_elem = element.find('div', class_=re.compile('vr1PYe|wEwyrc|LEwnzc'))
            if not source_elem:
                source_elem = element.find('span', class_=re.compile('vr1PYe|wEwyrc'))
            source = source_elem.get_text(strip=True) if source_elem else 'Google News'
            
            # Tiempo
            time_elem = element.find('time')
            if time_elem and time_elem.get('datetime'):
                published = time_elem['datetime']
            else:
                time_text_elem = element.find('div', class_=re.compile('hvbAAd|WW6dff'))
                time_text = time_text_elem.get_text(strip=True) if time_text_elem else ''
                published = self._parse_relative_time(time_text)
            
            return {
                'title': title,
                'source': f"Google News - {source}",
                'url': link,
                'summary': '',  # Google News no muestra resumen completo
                'published_at': published if isinstance(published, str) else datetime.now(timezone.utc).isoformat(),
                'collected_via': 'google_news'
            }
            
        except Exception as e:
            return None
    
    def _parse_relative_time(self, text):
        """Convierte 'hace 2 horas' a datetime"""
        now = datetime.now(timezone.utc)
        
        if 'hora' in text.lower():
            hours = int(re.search(r'(\d+)', text).group(1)) if re.search(r'(\d+)', text) else 1
            return (now - __import__('datetime').timedelta(hours=hours)).isoformat()
        elif 'minuto' in text.lower():
            mins = int(re.search(r'(\d+)', text).group(1)) if re.search(r'(\d+)', text) else 5
            return (now - __import__('datetime').timedelta(minutes=mins)).isoformat()
        
        return now.isoformat()
