# Vercel API - Obtener noticias (serverless)
import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.rss_agent import RSSAgent
from agents.newsapi_agent import NewsAPIAgent
from agents.google_news_agent import GoogleNewsAgent

class handler:
    def __call__(self, request):
        """Entry point for Vercel serverless"""
        method = request.get('method', 'GET')
        return self.get_news()
    
    def get_news(self):
        """Fetch news from all sources"""
        all_articles = []
        
        try:
            rss = RSSAgent()
            rss_articles = rss.fetch_all(max_age_hours=48, limit_per_source=3)
            all_articles.extend(rss_articles)
        except Exception as e:
            print(f"RSS error: {e}")
        
        try:
            newsapi = NewsAPIAgent()
            newsapi_articles = newsapi.fetch_all(hours_back=48)
            all_articles.extend(newsapi_articles)
        except Exception as e:
            print(f"NewsAPI error: {e}")
        
        try:
            gn = GoogleNewsAgent()
            gn_articles = gn.search_political()
            all_articles.extend(gn_articles)
        except Exception as e:
            print(f"Google News error: {e}")
        
        # Analizar cada artículo
        for article in all_articles:
            content = (article.get('title', '') + ' ' + article.get('content', '')).lower()
            article['sentiment'] = 'neutral'
            article['is_alert'] = False
            article['relevance_score'] = 0
            
            if any(w in content for w in ['violencia', 'ataque', 'secuestro', 'paro armado', 'bloqueo', 'fraude', 'amenaza', 'disidencia', 'eln', 'clan del golfo', 'farc']):
                article['is_alert'] = True
                article['relevance_score'] += 50
            
            if any(w in content for w in ['paloma valencia', 'centro democratico', 'centro democrático', 'senadora valencia']):
                article['relevance_score'] += 30
                article['sentiment'] = 'positive' if any(w in content for w in ['logro', 'apoyo', 'victoria', 'lidera']) else article['sentiment']
        
        sorted_articles = sorted(all_articles, key=lambda x: x.get('published_at', ''), reverse=True)[:30]
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST'
            },
            'body': json.dumps({
                'articles': sorted_articles,
                'count': len(sorted_articles),
                'timestamp': datetime.now().isoformat()
            })
        }
