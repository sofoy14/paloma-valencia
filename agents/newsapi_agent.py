"""
NewsAPI Agent - Recolector de noticias vía NewsAPI
"""
import requests
import os
from datetime import datetime, timedelta

class NewsAPIAgent:
    """Agente especializado en recolectar noticias de NewsAPI"""
    
    def __init__(self, api_key=None, keywords=None):
        self.api_key = api_key or os.getenv('NEWS_API_KEY')
        self.base_url = 'https://newsapi.org/v2'
        self.keywords = keywords or [
            'Paloma Valencia',
            'centro democratico Colombia',
            'elecciones Colombia 2026'
        ]
    
    def fetch_all(self, hours_back=24):
        """Recolecta noticias de NewsAPI"""
        if not self.api_key:
            print("NewsAPI key not configured")
            return []
        
        all_articles = []
        
        # Buscar por cada keyword
        for keyword in self.keywords:
            try:
                articles = self._search_news(keyword, hours_back)
                all_articles.extend(articles)
            except Exception as e:
                print(f"Error searching '{keyword}': {e}")
        
        # Remover duplicados por URL
        seen_urls = set()
        unique_articles = []
        for article in all_articles:
            if article['url'] not in seen_urls:
                seen_urls.add(article['url'])
                unique_articles.append(article)
        
        return unique_articles
    
    def _search_news(self, query, hours_back):
        """Busca noticias por query"""
        from_date = (datetime.now() - timedelta(hours=hours_back)).strftime('%Y-%m-%d')
        
        url = f"{self.base_url}/everything"
        params = {
            'q': query,
            'from': from_date,
            'language': 'es',
            'sortBy': 'publishedAt',
            'pageSize': 20,
            'apiKey': self.api_key
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        articles = []
        
        for item in data.get('articles', []):
            try:
                article = {
                    'title': item.get('title', ''),
                    'source': f"NewsAPI - {item.get('source', {}).get('name', 'Unknown')}",
                    'url': item.get('url', ''),
                    'summary': item.get('description', ''),
                    'published_at': item.get('publishedAt'),
                    'author': item.get('author', ''),
                    'content': item.get('content', ''),
                    'collected_via': 'newsapi'
                }
                articles.append(article)
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue
        
        return articles
    
    def get_top_headlines_colombia(self):
        """Obtiene headlines principales de Colombia"""
        if not self.api_key:
            return []
        
        url = f"{self.base_url}/top-headlines"
        params = {
            'country': 'co',
            'pageSize': 20,
            'apiKey': self.api_key
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        articles = []
        
        for item in data.get('articles', []):
            # Solo incluir si es relevante
            title = item.get('title', '').lower()
            desc = item.get('description', '').lower() if item.get('description') else ''
            
            if any(kw.lower() in title or kw.lower() in desc for kw in self.keywords):
                try:
                    article = {
                        'title': item.get('title', ''),
                        'source': f"NewsAPI - {item.get('source', {}).get('name', 'Unknown')}",
                        'url': item.get('url', ''),
                        'summary': item.get('description', ''),
                        'published_at': item.get('publishedAt'),
                        'author': item.get('author', ''),
                        'content': item.get('content', ''),
                        'collected_via': 'newsapi'
                    }
                    articles.append(article)
                except Exception as e:
                    print(f"Error parsing article: {e}")
                    continue
        
        return articles
