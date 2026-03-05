import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

# Detectar si estamos en Railway u otro cloud
if os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('RAILWAY_STATIC_URL'):
    DB_PATH = Path("/app/data/news.db")
else:
    DB_PATH = Path("data/news.db")

class NewsDatabase:
    def __init__(self):
        DB_PATH.parent.mkdir(exist_ok=True)
        self.init_db()
    
    def get_conn(self):
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_db(self):
        conn = self.get_conn()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                source TEXT NOT NULL,
                url TEXT UNIQUE NOT NULL,
                summary TEXT,
                published_at TIMESTAMP,
                collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                sentiment TEXT,
                sentiment_score REAL,
                keywords TEXT,
                category TEXT,
                author TEXT,
                content TEXT,
                is_alert BOOLEAN DEFAULT 0
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                article_id INTEGER,
                alert_type TEXT,
                message TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (article_id) REFERENCES articles (id)
            )
        ''')
        
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_articles_url ON articles(url)
        ''')
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_articles_published ON articles(published_at)
        ''')
        
        conn.commit()
        conn.close()
    
    def save_article(self, article):
        """Guarda un artículo, evitando duplicados por URL"""
        conn = self.get_conn()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO articles 
                (title, source, url, summary, published_at, sentiment, sentiment_score, keywords, category, author, content, is_alert)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                article.get('title'),
                article.get('source'),
                article.get('url'),
                article.get('summary'),
                article.get('published_at'),
                article.get('sentiment'),
                article.get('sentiment_score'),
                json.dumps(article.get('keywords', [])),
                article.get('category'),
                article.get('author'),
                article.get('content'),
                article.get('is_alert', False)
            ))
            
            conn.commit()
            return cursor.lastrowid if cursor.lastrowid else None
        except Exception as e:
            print(f"Error saving article: {e}")
            return None
        finally:
            conn.close()
    
    def get_recent_articles(self, hours=24, limit=100):
        """Obtiene artículos recientes"""
        conn = self.get_conn()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM articles 
            WHERE collected_at >= datetime('now', '-{} hours')
            ORDER BY published_at DESC
            LIMIT {}
        '''.format(hours, limit))
        
        articles = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return articles
    
    def get_stats(self, hours=24):
        """Obtiene estadísticas de noticias"""
        conn = self.get_conn()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total,
                SUM(CASE WHEN sentiment = 'positive' THEN 1 ELSE 0 END) as positive,
                SUM(CASE WHEN sentiment = 'negative' THEN 1 ELSE 0 END) as negative,
                SUM(CASE WHEN sentiment = 'neutral' THEN 1 ELSE 0 END) as neutral,
                SUM(CASE WHEN is_alert = 1 THEN 1 ELSE 0 END) as alerts
            FROM articles 
            WHERE collected_at >= datetime('now', '-{} hours')
        '''.format(hours))
        
        row = cursor.fetchone()
        conn.close()
        
        return {
            'total': row['total'] or 0,
            'positive': row['positive'] or 0,
            'negative': row['negative'] or 0,
            'neutral': row['neutral'] or 0,
            'alerts': row['alerts'] or 0
        }
