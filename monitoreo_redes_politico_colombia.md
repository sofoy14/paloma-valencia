# Guía de Monitoreo de Redes Sociales para Campañas Políticas en Colombia
## Alternativas SIN APIs Costosas - 2024-2025

---

## ⚠️ IMPORTANTE: Estado Actual del Scraping de Redes Sociales (2024-2025)

### La realidad del scraping en 2024-2025:
- **Twitter/X**: Ha implementado defensas agresivas contra scrapers. Cambios cada 2-4 semanas.
- **Facebook**: Muy restrictivo, requiere login para la mayoría de contenido.
- **Instagram**: Instaloader sigue funcionando pero con limitaciones.
- **YouTube**: API gratuita disponible y estable - **RECOMENDADO**.

---

## 1. TWITTER/X - Estado y Alternativas

### ❌ SNSCRAPE - YA NO FUNCIONA CORRECTAMENTE

**Estado actual (2024-2025):** snscrape ha dejado de funcionar de forma confiable debido a:
- Cambios en la obtención de guest tokens (enero 2024)
- Bloqueo de IPs de datacenter (octubre 2024)
- Cambios en endpoints GraphQL cada mes
- Bloqueo permanente de IPs de datacenter (enero 2025)

**Error típico:**
```
Error 215: Bad Authentication data
Error 401: Unauthorized
```

### ✅ ALTERNATIVA FUNCIONAL: Selenium + navegador

```python
"""
Twitter/X Scraper usando Selenium
Funciona para: tweets de usuario, búsquedas básicas
Requiere: Chrome/Edge instalado
Limitaciones: Puede requerir ajustes frecuentes por cambios en X
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from datetime import datetime

class TwitterScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Configura el driver de Chrome"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
    
    def scrape_user_tweets(self, username, max_tweets=50):
        """
        Extrae tweets de un usuario específico
        NOTA: X requiere login para ver muchos tweets
        """
        url = f"https://twitter.com/{username}"
        self.driver.get(url)
        time.sleep(5)  # Esperar carga inicial
        
        tweets_data = []
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while len(tweets_data) < max_tweets:
            # Buscar tweets en la página
            tweets = self.driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
            
            for tweet in tweets:
                try:
                    # Extraer texto
                    text_elem = tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                    text = text_elem.text
                    
                    # Extraer fecha (si está disponible)
                    try:
                        time_elem = tweet.find_element(By.TAG_NAME, 'time')
                        timestamp = time_elem.get_attribute('datetime')
                    except:
                        timestamp = None
                    
                    # Extraer métricas de engagement
                    try:
                        stats = tweet.find_elements(By.CSS_SELECTOR, '[data-testid="app-text-transition-container"]')
                        metrics = [s.text for s in stats]
                    except:
                        metrics = []
                    
                    tweet_data = {
                        'username': username,
                        'text': text,
                        'timestamp': timestamp,
                        'metrics': metrics,
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    if tweet_data not in tweets_data:
                        tweets_data.append(tweet_data)
                        
                except Exception as e:
                    continue
            
            # Scroll para cargar más tweets
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        return tweets_data[:max_tweets]
    
    def search_tweets(self, query, max_results=50):
        """
        Busca tweets por palabra clave
        NOTA: X requiere login para búsqueda avanzada
        """
        # X ahora requiere login para búsquedas
        print("ADVERTENCIA: X/Twitter requiere login para búsquedas")
        print("Considera usar Nitter (instancias públicas limitadas) o la API oficial")
        return []
    
    def close(self):
        if self.driver:
            self.driver.quit()

# Ejemplo de uso
if __name__ == "__main__":
    scraper = TwitterScraper(headless=True)
    try:
        # NOTA: Muchas funciones requieren login ahora
        # tweets = scraper.scrape_user_tweets("candidato_ejemplo", max_tweets=20)
        # df = pd.DataFrame(tweets)
        # df.to_csv("tweets.csv", index=False)
        print("Twitter scraping requiere adaptaciones constantes debido a cambios en la plataforma")
    finally:
        scraper.close()
```

### 🔄 ALTERNATIVA: Nitter (Instancias Públicas)

```python
"""
Nitter Scraper - Instancias públicas de Nitter
Nitter es un frontend alternativo de Twitter/X
Estado: Algunas instancias siguen funcionando (2024)
"""

import requests
from bs4 import BeautifulSoup
import time

class NitterScraper:
    def __init__(self, instance="https://nitter.net"):
        self.instance = instance
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def get_user_tweets(self, username, max_tweets=20):
        """Extrae tweets de un usuario vía Nitter"""
        url = f"{self.instance}/{username}"
        tweets = []
        
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code != 200:
                print(f"Error: {response.status_code}")
                return tweets
            
            soup = BeautifulSoup(response.text, 'html.parser')
            tweet_elements = soup.find_all('div', class_='timeline-item')
            
            for tweet in tweet_elements[:max_tweets]:
                try:
                    text_elem = tweet.find('div', class_='tweet-content')
                    text = text_elem.get_text(strip=True) if text_elem else ""
                    
                    time_elem = tweet.find('span', class_='tweet-date')
                    timestamp = time_elem.get_text(strip=True) if time_elem else ""
                    
                    tweets.append({
                        'username': username,
                        'text': text,
                        'timestamp': timestamp
                    })
                except:
                    continue
                    
        except Exception as e:
            print(f"Error: {e}")
        
        return tweets

# Lista de instancias públicas de Nitter (actualizar según disponibilidad)
NITTER_INSTANCES = [
    "https://nitter.net",
    "https://nitter.privacydev.net",
    "https://nitter.cz",
]

# Ejemplo de uso
# scraper = NitterScraper(instance=NITTER_INSTANCES[0])
# tweets = scraper.get_user_tweets("candidato", max_tweets=10)
```

---

## 2. FACEBOOK - Monitoreo de Páginas Públicas

### ✅ facebook-scraper - FUNCIONA (Con Limitaciones)

```bash
# Instalación
pip install facebook-scraper pandas
```

```python
"""
Facebook Scraper usando facebook-scraper
Funciona para: Páginas públicas de Facebook
Requiere: Solo nombre de la página
Limitaciones: No funciona para perfiles personales ni grupos privados
"""

from facebook_scraper import get_posts
import pandas as pd
from datetime import datetime
import json

class FacebookMonitor:
    def __init__(self):
        self.data = []
    
    def scrape_page_posts(self, page_name, pages=5, options=None):
        """
        Extrae posts de una página pública de Facebook
        
        Args:
            page_name: Nombre de la página (ej: 'GustavoPetroOficial')
            pages: Número de páginas a recorrer
            options: Opciones adicionales como cookies
        """
        try:
            posts = get_posts(
                page_name,
                pages=pages,
                options=options or {}
            )
            
            for post in posts:
                self.data.append({
                    'page': page_name,
                    'post_id': post.get('post_id'),
                    'text': post.get('text', ''),
                    'post_text': post.get('post_text', ''),
                    'shared_text': post.get('shared_text', ''),
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
            print(f"Error scraping {page_name}: {e}")
        
        return self.data
    
    def scrape_multiple_pages(self, page_list, pages_per_page=3):
        """Monitorea múltiples páginas"""
        all_data = []
        
        for page in page_list:
            print(f"Scrapeando página: {page}")
            posts = self.scrape_page_posts(page, pages=pages_per_page)
            all_data.extend(posts)
            time.sleep(2)  # Evitar bloqueos
        
        return all_data
    
    def to_dataframe(self):
        """Convierte datos a DataFrame de pandas"""
        return pd.DataFrame(self.data)
    
    def save_to_csv(self, filename="facebook_posts.csv"):
        """Guarda datos en CSV"""
        df = self.to_dataframe()
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Guardado: {filename}")
        return df
    
    def save_to_json(self, filename="facebook_posts.json"):
        """Guarda datos en JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2, default=str)
        print(f"Guardado: {filename}")

# Ejemplo de uso para monitoreo político
if __name__ == "__main__":
    # Lista de páginas políticas colombianas de ejemplo
    paginas_politicas = [
        # "GustavoPetroOficial",  # Ejemplo - reemplazar con páginas reales
        # "IvanDuqueMarquez",
        # "AlvaroUribeVel",
    ]
    
    monitor = FacebookMonitor()
    
    for pagina in paginas_politicas:
        print(f"\nMonitoreando: {pagina}")
        try:
            monitor.scrape_page_posts(pagina, pages=2)
        except Exception as e:
            print(f"Error: {e}")
    
    if monitor.data:
        monitor.save_to_csv()
        monitor.save_to_json()
```

### 📱 Alternativa: Versión Móvil con Selenium

```python
"""
Facebook Mobile Scraper
Usa m.facebook.com que es más simple de scrapear
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

class FacebookMobileScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 10)")
        
        self.driver = webdriver.Chrome(options=chrome_options)
    
    def scrape_page(self, page_name, max_posts=10):
        """Scrapea usando versión móvil"""
        url = f"https://m.facebook.com/{page_name}"
        self.driver.get(url)
        time.sleep(3)
        
        posts = []
        post_elements = self.driver.find_elements(By.XPATH, '//div[@role="article"]')
        
        for elem in post_elements[:max_posts]:
            try:
                text = elem.find_element(By.XPATH, './/span').text
                posts.append({'text': text})
            except:
                continue
        
        return posts
    
    def close(self):
        self.driver.quit()
```

---

## 3. INSTAGRAM - Monitoreo de Hashtags

### ✅ Instaloader - FUNCIONA BIEN

```bash
# Instalación
pip install instaloader pandas
```

```python
"""
Instagram Scraper usando Instaloader
Funciona para: Perfiles públicos, hashtags, posts públicos
Requiere: Cuenta de Instagram para algunas funciones
"""

import instaloader
from instaloader import Profile, Hashtag, Post
import pandas as pd
from datetime import datetime
import time
import os

class InstagramMonitor:
    def __init__(self, login_user=None, login_pass=None):
        """
        Inicializa el monitor de Instagram
        
        Args:
            login_user: Usuario de Instagram (opcional, pero recomendado)
            login_pass: Contraseña (opcional)
        """
        self.L = instaloader.Instaloader(
            download_pictures=False,
            download_videos=False,
            download_video_thumbnails=False,
            download_geotags=False,
            download_comments=False,
            save_metadata=False,
            compress_json=False
        )
        
        if login_user and login_pass:
            try:
                self.L.login(login_user, login_pass)
                print(f"Login exitoso: {login_user}")
            except Exception as e:
                print(f"Error de login: {e}")
                print("Continuando sin login (limitado)")
    
    def monitor_hashtag(self, hashtag_name, max_posts=50):
        """
        Monitorea un hashtag específico
        
        Args:
            hashtag_name: Nombre del hashtag (sin #)
            max_posts: Número máximo de posts a obtener
        """
        posts_data = []
        
        try:
            hashtag = Hashtag.from_name(self.L.context, hashtag_name)
            print(f"Hashtag: #{hashtag_name}")
            print(f"Posts totales aproximados: {hashtag.mediacount}")
            
            for index, post in enumerate(hashtag.get_posts()):
                if index >= max_posts:
                    break
                
                post_data = self._extract_post_data(post)
                posts_data.append(post_data)
                
                if (index + 1) % 10 == 0:
                    print(f"Procesados: {index + 1}/{max_posts}")
                    time.sleep(1)  # Evitar rate limits
            
        except Exception as e:
            print(f"Error monitoreando #{hashtag_name}: {e}")
        
        return posts_data
    
    def monitor_profile(self, username, max_posts=50):
        """
        Monitorea un perfil público
        """
        posts_data = []
        
        try:
            profile = Profile.from_username(self.L.context, username)
            print(f"Perfil: @{username}")
            print(f"Seguidores: {profile.followers}")
            print(f"Posts: {profile.mediacount}")
            
            for index, post in enumerate(profile.get_posts()):
                if index >= max_posts:
                    break
                
                post_data = self._extract_post_data(post)
                posts_data.append(post_data)
                
                if (index + 1) % 10 == 0:
                    print(f"Procesados: {index + 1}/{max_posts}")
                    time.sleep(1)
            
        except Exception as e:
            print(f"Error monitoreando @{username}: {e}")
        
        return posts_data
    
    def monitor_multiple_hashtags(self, hashtags_list, posts_per_hashtag=30):
        """Monitorea múltiples hashtags"""
        all_data = []
        
        for tag in hashtags_list:
            print(f"\n{'='*50}")
            print(f"Monitoreando: #{tag}")
            print('='*50)
            
            data = self.monitor_hashtag(tag, posts_per_hashtag)
            all_data.extend(data)
            
            # Pausa entre hashtags
            time.sleep(5)
        
        return all_data
    
    def _extract_post_data(self, post):
        """Extrae datos de un post"""
        return {
            'shortcode': post.shortcode,
            'url': f"https://instagram.com/p/{post.shortcode}/",
            'caption': post.caption,
            'caption_hashtags': post.caption_hashtags,
            'caption_mentions': post.caption_mentions,
            'date': post.date_local.isoformat(),
            'likes': post.likes,
            'comments': post.comments,
            'is_video': post.is_video,
            'video_view_count': post.video_view_count if post.is_video else 0,
            'owner_username': post.owner_username,
            'owner_id': post.owner_id,
            'scraped_at': datetime.now().isoformat()
        }
    
    def analyze_sentiment_basic(self, posts_data):
        """
        Análisis básico de sentimiento basado en palabras clave
        """
        positive_words = ['bueno', 'excelente', 'gran', 'mejor', 'apoyo', 'voto', 'confianza', 'esperanza']
        negative_words = ['malo', 'terrible', 'peor', 'corrupcion', 'robo', 'mentira', 'decepcion', 'no']
        
        for post in posts_data:
            caption = post.get('caption', '') or ''
            caption_lower = caption.lower()
            
            pos_count = sum(1 for word in positive_words if word in caption_lower)
            neg_count = sum(1 for word in negative_words if word in caption_lower)
            
            if pos_count > neg_count:
                post['sentiment'] = 'positive'
            elif neg_count > pos_count:
                post['sentiment'] = 'negative'
            else:
                post['sentiment'] = 'neutral'
        
        return posts_data
    
    def export_to_csv(self, data, filename="instagram_data.csv"):
        """Exporta datos a CSV"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\nExportado: {filename}")
        print(f"Total registros: {len(df)}")
        return df

# Ejemplo de uso para campaña política
if __name__ == "__main__":
    # Hashtags políticos colombianos comunes
    hashtags_politicos = [
        "colombia",
        "politica",
        "elecciones",
        "voto",
        "cambio",
        "democracia",
        # Añadir hashtags específicos de la campaña
    ]
    
    # Inicializar monitor (sin login para solo público)
    monitor = InstagramMonitor()
    
    # Monitorear hashtags
    datos = monitor.monitor_multiple_hashtags(
        hashtags_politicos[:3],  # Limitar para prueba
        posts_per_hashtag=20
    )
    
    # Análisis básico
    if datos:
        datos = monitor.analyze_sentiment_basic(datos)
        monitor.export_to_csv(datos)
```

---

## 4. YOUTUBE - API Gratuita

### ✅ YouTube Data API v3 - GRATUITA Y ESTABLE

```bash
# Instalación
pip install google-api-python-client pandas
```

```python
"""
YouTube Monitor usando Data API v3
100% GRATIS - 10,000 unidades de cuota diarias
Documentación: https://developers.google.com/youtube/v3

Costos de cuota:
- search.list: 100 unidades
- videos.list: 1 unidad
- channels.list: 1 unidad
- commentThreads.list: 1 unidad

10,000 unidades = ~100 búsquedas diarias
"""

from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pandas as pd
import json

class YouTubeMonitor:
    def __init__(self, api_key):
        """
        Inicializa el monitor de YouTube
        
        Args:
            api_key: API Key de Google Cloud (gratis)
            Obtener en: https://console.cloud.google.com/
        """
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.quota_used = 0
    
    def search_videos(self, query, max_results=50, published_after=None, region_code='CO'):
        """
        Busca videos por palabra clave
        
        Args:
            query: Término de búsqueda
            max_results: Máximo 50 por solicitud
            published_after: Fecha ISO (ej: 2024-01-01T00:00:00Z)
            region_code: Código de país (CO = Colombia)
        """
        videos = []
        
        try:
            # Construir parámetros de búsqueda
            search_params = {
                'q': query,
                'type': 'video',
                'part': 'id,snippet',
                'maxResults': min(max_results, 50),
                'regionCode': region_code,
                'relevanceLanguage': 'es',
                'order': 'date'  # Más recientes primero
            }
            
            if published_after:
                search_params['publishedAfter'] = published_after
            
            response = self.youtube.search().list(**search_params).execute()
            self.quota_used += 100  # Costo de search.list
            
            video_ids = [item['id']['videoId'] for item in response.get('items', [])]
            
            if video_ids:
                # Obtener detalles adicionales
                video_details = self._get_video_details(video_ids)
                videos.extend(video_details)
            
        except Exception as e:
            print(f"Error en búsqueda: {e}")
        
        return videos
    
    def _get_video_details(self, video_ids):
        """Obtiene detalles de videos por sus IDs"""
        details = []
        
        # La API permite hasta 50 IDs por solicitud
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            
            try:
                response = self.youtube.videos().list(
                    part='snippet,contentDetails,statistics',
                    id=','.join(batch)
                ).execute()
                
                self.quota_used += 1  # Costo de videos.list
                
                for item in response.get('items', []):
                    details.append({
                        'video_id': item['id'],
                        'title': item['snippet']['title'],
                        'description': item['snippet']['description'],
                        'published_at': item['snippet']['publishedAt'],
                        'channel_id': item['snippet']['channelId'],
                        'channel_title': item['snippet']['channelTitle'],
                        'tags': item['snippet'].get('tags', []),
                        'category_id': item['snippet']['categoryId'],
                        'duration': item['contentDetails']['duration'],
                        'view_count': int(item['statistics'].get('viewCount', 0)),
                        'like_count': int(item['statistics'].get('likeCount', 0)),
                        'comment_count': int(item['statistics'].get('commentCount', 0)),
                        'url': f"https://youtube.com/watch?v={item['id']}",
                        'thumbnail': item['snippet']['thumbnails'].get('high', {}).get('url', ''),
                        'scraped_at': datetime.now().isoformat()
                    })
                    
            except Exception as e:
                print(f"Error obteniendo detalles: {e}")
        
        return details
    
    def search_multiple_queries(self, queries, results_per_query=20):
        """Busca múltiples términos"""
        all_videos = []
        
        # Fecha de hace 30 días para contenido reciente
        published_after = (datetime.utcnow() - timedelta(days=30)).isoformat() + 'Z'
        
        for query in queries:
            print(f"\nBuscando: '{query}'")
            videos = self.search_videos(
                query, 
                max_results=results_per_query,
                published_after=published_after
            )
            all_videos.extend(videos)
            print(f"Encontrados: {len(videos)} videos")
        
        return all_videos
    
    def get_video_comments(self, video_id, max_results=100):
        """
        Obtiene comentarios de un video
        Costo: 1 unidad por solicitud
        """
        comments = []
        
        try:
            response = self.youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                maxResults=min(max_results, 100),
                order='time'
            ).execute()
            
            self.quota_used += 1
            
            for item in response.get('items', []):
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'video_id': video_id,
                    'comment_id': item['id'],
                    'author': comment['authorDisplayName'],
                    'text': comment['textDisplay'],
                    'like_count': comment['likeCount'],
                    'published_at': comment['publishedAt'],
                    'scraped_at': datetime.now().isoformat()
                })
                
        except Exception as e:
            print(f"Error obteniendo comentarios: {e}")
        
        return comments
    
    def get_channel_videos(self, channel_id, max_results=50):
        """
        Obtiene videos de un canal específico
        """
        videos = []
        
        try:
            # Primero necesitamos el uploads playlist ID
            channel_response = self.youtube.channels().list(
                part='contentDetails',
                id=channel_id
            ).execute()
            
            self.quota_used += 1
            
            if channel_response['items']:
                playlist_id = channel_response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
                
                # Obtener videos del playlist
                playlist_response = self.youtube.playlistItems().list(
                    part='snippet',
                    playlistId=playlist_id,
                    maxResults=min(max_results, 50)
                ).execute()
                
                self.quota_used += 1
                
                video_ids = [item['snippet']['resourceId']['videoId'] 
                           for item in playlist_response.get('items', [])]
                
                if video_ids:
                    videos = self._get_video_details(video_ids)
                    
        except Exception as e:
            print(f"Error obteniendo videos del canal: {e}")
        
        return videos
    
    def export_to_csv(self, data, filename="youtube_data.csv"):
        """Exporta a CSV"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\nExportado: {filename}")
        print(f"Total: {len(df)} registros")
        print(f"Cuota usada estimada: {self.quota_used}")
        return df
    
    def print_quota_status(self):
        """Muestra estado de la cuota"""
        print(f"\n{'='*50}")
        print("ESTADO DE CUOTA YOUTUBE API")
        print('='*50)
        print(f"Usada (estimada): {self.quota_used}")
        print(f"Límite diario: 10,000")
        print(f"Restante: {10000 - self.quota_used}")
        print('='*50)

# Ejemplo de uso para campaña política
if __name__ == "__main__":
    # REEMPLAZAR con tu API key de Google Cloud
    API_KEY = "TU_API_KEY_AQUI"
    
    if API_KEY == "TU_API_KEY_AQUI":
        print("⚠️  IMPORTANTE: Obtén tu API Key gratuita en:")
        print("https://console.cloud.google.com/apis/library/youtube.googleapis.com")
        print("\nPasos:")
        print("1. Crear proyecto en Google Cloud")
        print("2. Habilitar YouTube Data API v3")
        print("3. Crear credenciales > API Key")
        exit()
    
    monitor = YouTubeMonitor(API_KEY)
    
    # Términos de búsqueda políticos
    search_terms = [
        "debate presidencial Colombia",
        "candidatos Colombia 2026",
        "política Colombia",
    ]
    
    # Buscar videos
    videos = monitor.search_multiple_queries(search_terms, results_per_query=20)
    
    if videos:
        monitor.export_to_csv(videos, "youtube_politica.csv")
    
    monitor.print_quota_status()
```

---

## 📋 REQUISITOS Y DEPENDENCIAS

Crear archivo `requirements.txt`:

```txt
# YouTube (API Gratuita)
google-api-python-client>=2.100.0

# Facebook
facebook-scraper>=0.2.59

# Instagram
instaloader>=4.10

# Twitter/X Alternativas
selenium>=4.15.0
webdriver-manager>=4.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0

# Utilidades
pandas>=2.0.0
python-dateutil>=2.8.0
```

Instalar todo:
```bash
pip install -r requirements.txt
```

---

## ⚖️ MARCO LEGAL EN COLOMBIA

### Regulación Electoral y Redes Sociales

#### 1. **Propaganda Electoral en Redes**
Según el Consejo Nacional Electoral (CNE):

- **Plazo**: La propaganda electoral en redes sociales SOLO puede realizarse dentro de los **60 días anteriores a la elección** (Art. 35 Ley 1475 de 2011)
- **Rendición de cuentas**: Todo gasto en publicidad digital debe reportarse en **Cuentas Claras**
- **Tipos de propaganda**:
  - Pagada: Debe reportarse con su costo comercial
  - Orgánica: Se reporta como recurso propio con valor comercial estimado

#### 2. **Resolución 15588 de 2023 del CNE**
Define la propaganda electoral en internet considerando:

| Aspecto | Criterio |
|---------|----------|
| Medio | Difusión por cualquier plataforma digital o red social |
| Contenido | Mensaje que busque captar el vot directa e inequívocamente |
| Característica | Masividad o potencialidad de llegar a ser masivo |

#### 3. **Protección de Datos Personales**

- **Ley 1581 de 2012**: Protección de datos personales
- **Decreto 1377 de 2013**: Reglamentación
- **Autorización requerida**: Para usar datos personales con fines políticos

**⚠️ RESTRICCIONES IMPORTANTES:**
- No se puede hacer scraping de datos personales sin autorización
- No se puede usar información de perfiles privados
- El monitoreo debe limitarse a **INFORMACIÓN PÚBLICA**

#### 4. **Transparencia y Financiación**

Según Transparencia por Colombia:
- Existe opacidad en el reporte de gastos de campañas digitales
- Las redes sociales representan entre 20-40% del gasto de propaganda
- Es obligatorio reportar en tiempo real (una semana después del gasto)

#### 5. **Recomendaciones Legales para Monitoreo**

✅ **PERMITIDO:**
- Monitorear hashtags públicos
- Analizar posts de páginas públicas
- Usar APIs oficiales (YouTube)
- Analizar sentimiento de comentarios públicos
- Reportes de transparencia electoral

❌ **PROHIBIDO:**
- Scraping de perfiles privados
- Almacenar datos personales sin autorización
- Usar bots para manipular opinión
- Publicidad electoral fuera del plazo legal
- No reportar gastos en redes sociales

### Fuentes de Información Legal:
- MOE (Misión de Observación Electoral): https://www.moe.org.co
- CNE (Consejo Nacional Electoral): https://www.cne.gov.co
- Transparencia por Colombia: https://transparenciacolombia.org.co

---

## 🎯 RECOMENDACIONES FINALES

### Opción más estable: **YouTube Data API**
- ✅ 100% gratuita
- ✅ Documentación oficial
- ✅ Cuota generosa (10,000/día)
- ✅ No requiere workarounds

### Para monitoreo general:
| Plataforma | Herramienta | Estado | Dificultad |
|------------|-------------|--------|------------|
| YouTube | API Oficial | ✅ Estable | Baja |
| Instagram | Instaloader | ✅ Funciona | Media |
| Facebook | facebook-scraper | ⚠️ Limitado | Media |
| Twitter/X | Selenium/Nitter | ❌ Difícil | Alta |

### Consejos prácticos:
1. **Usa delays** entre requests para evitar bloqueos
2. **Rota IPs** si es posible (residenciales)
3. **Almacena datos** en formato estructurado (CSV/JSON)
4. **Respeta rate limits** de cada plataforma
5. **Documenta fuentes** para transparencia electoral
6. **Consulta legal** antes de campañas activas

---

*Documento actualizado: Marzo 2025*
