"""
Twitter/X Agent - Monitoreo de tweets usando snscrape
Gratis, sin API key requerida
"""
import subprocess
import json
import re
from datetime import datetime, timezone, timedelta

class TwitterAgent:
    """Agente para monitorear Twitter/X sin usar API oficial"""
    
    def __init__(self):
        self.keywords = [
            'Paloma Valencia',
            'PalomaValencia',
            'Centro Democratico',
            'elecciones 2026',
            '#EleccionesColombia2026'
        ]
        self.influencers = [
            'mluciaramirez',  # María Lucía Ramírez
            'FicoGutierrez',  # Federico Gutiérrez
            'AlvaroUribeVel', # Álvaro Uribe
            'petrogustavo',   # Gustavo Petro
            'JC_Restrepo',    # Periodista
            'VickyDavilaH',   # Vicky Dávila
            'DanielSamperO',  # Daniel Samper
        ]
    
    def search_tweets(self, query, limit=20):
        """Busca tweets por query usando snscrape"""
        tweets = []
        
        try:
            # Ejecutar snscrape
            cmd = [
                'snscrape', '--jsonl', '--max-results', str(limit),
                f'twitter-search', f'{query} since:{(datetime.now() - timedelta(hours=24)).strftime("%Y-%m-%d")}'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        try:
                            data = json.loads(line)
                            tweets.append(self._parse_tweet(data))
                        except:
                            continue
            else:
                print(f"[Twitter] snscrape error: {result.stderr}")
                
        except Exception as e:
            print(f"[Twitter] Error: {e}")
        
        return tweets
    
    def get_user_tweets(self, username, limit=10):
        """Obtiene tweets de un usuario específico"""
        tweets = []
        
        try:
            cmd = [
                'snscrape', '--jsonl', '--max-results', str(limit),
                'twitter-user', username
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        try:
                            data = json.loads(line)
                            # Solo tweets recientes
                            tweet_date = datetime.fromisoformat(data.get('date', '').replace('Z', '+00:00'))
                            if datetime.now(timezone.utc) - tweet_date < timedelta(hours=24):
                                tweets.append(self._parse_tweet(data))
                        except:
                            continue
                            
        except Exception as e:
            print(f"[Twitter] Error getting user {username}: {e}")
        
        return tweets
    
    def monitor_all(self):
        """Monitorea todo: keywords + influencers"""
        all_tweets = []
        
        # Buscar por keywords
        for keyword in self.keywords[:3]:  # Limitar para velocidad
            try:
                tweets = self.search_tweets(keyword, limit=10)
                all_tweets.extend(tweets)
            except Exception as e:
                print(f"[Twitter] Error keyword '{keyword}': {e}")
        
        # Monitorear influencers clave
        for username in self.influencers[:5]:  # Top 5
            try:
                tweets = self.get_user_tweets(username, limit=5)
                all_tweets.extend(tweets)
            except Exception as e:
                print(f"[Twitter] Error user @{username}: {e}")
        
        # Remover duplicados
        seen = set()
        unique = []
        for t in all_tweets:
            if t['id'] not in seen:
                seen.add(t['id'])
                unique.append(t)
        
        return sorted(unique, key=lambda x: x['date'], reverse=True)[:30]
    
    def _parse_tweet(self, data):
        """Parsea datos de snscrape a formato estándar"""
        return {
            'id': data.get('id', ''),
            'title': f"Tweet de @{data.get('user', {}).get('username', 'unknown')}: {data.get('content', '')[:100]}...",
            'source': f"Twitter - @{data.get('user', {}).get('username', 'unknown')}",
            'url': f"https://twitter.com/i/web/status/{data.get('id', '')}",
            'summary': data.get('content', ''),
            'published_at': data.get('date'),
            'author': data.get('user', {}).get('displayname', ''),
            'collected_via': 'twitter',
            'retweets': data.get('retweetCount', 0),
            'likes': data.get('likeCount', 0),
            'replies': data.get('replyCount', 0),
            'engagement': data.get('retweetCount', 0) + data.get('likeCount', 0)
        }
    
    def analyze_tweet_sentiment(self, tweet):
        """Análisis básico de sentimiento de tweet"""
        text = tweet.get('summary', '').lower()
        
        positive_words = ['excelente', 'bueno', 'gran', 'apoyo', 'logro', 'victoria', 'éxito']
        negative_words = ['malo', 'terrible', 'corrupto', 'problema', 'crisis', 'urgente', 'denuncia']
        
        pos_count = sum(1 for w in positive_words if w in text)
        neg_count = sum(1 for w in negative_words if w in text)
        
        if neg_count > pos_count:
            return 'negative', -0.5
        elif pos_count > neg_count:
            return 'positive', 0.5
        return 'neutral', 0.0
