"""
Facebook Monitor usando facebook-scraper
Para campañas políticas en Colombia

Instalación: pip install facebook-scraper pandas

NOTA: Solo funciona con páginas públicas
"""

from facebook_scraper import get_posts
import pandas as pd
from datetime import datetime
import time

class FacebookMonitor:
    def __init__(self):
        self.data = []
    
    def scrape_page_posts(self, page_name, pages=3):
        """
        Extrae posts de una página pública
        
        Args:
            page_name: Nombre de la página (ej: 'GustavoPetroOficial')
            pages: Número de páginas a recorrer
        """
        try:
            posts = get_posts(page_name, pages=pages)
            
            for post in posts:
                self.data.append({
                    'page': page_name,
                    'post_id': post.get('post_id'),
                    'text': post.get('text', ''),
                    'time': post.get('time'),
                    'likes': post.get('likes', 0),
                    'comments': post.get('comments', 0),
                    'shares': post.get('shares', 0),
                    'post_url': post.get('post_url'),
                    'link': post.get('link'),
                    'image': post.get('image'),
                    'scraped_at': datetime.now().isoformat()
                })
                    
        except Exception as e:
            print(f"Error: {e}")
        
        return self.data
    
    def export_to_csv(self, filename="facebook_posts.csv"):
        """Exporta a CSV"""
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Exportado: {filename} ({len(df)} posts)")
        return df


# EJEMPLO DE USO
if __name__ == "__main__":
    monitor = FacebookMonitor()
    
    # Scrapear página pública
    # NOTA: Reemplazar con página real
    # monitor.scrape_page_posts("nombre_pagina", pages=2)
    
    if monitor.data:
        monitor.export_to_csv()
    else:
        print("No se encontraron datos. Verifica que la página sea pública.")
