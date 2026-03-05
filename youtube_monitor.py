"""
YouTube Monitor - API Gratuita
Para campañas políticas en Colombia

Requiere API Key gratuita de Google Cloud:
https://console.cloud.google.com/apis/library/youtube.googleapis.com
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
            search_params = {
                'q': query,
                'type': 'video',
                'part': 'id,snippet',
                'maxResults': min(max_results, 50),
                'regionCode': region_code,
                'relevanceLanguage': 'es',
                'order': 'date'
            }
            
            if published_after:
                search_params['publishedAfter'] = published_after
            
            response = self.youtube.search().list(**search_params).execute()
            self.quota_used += 100
            
            video_ids = [item['id']['videoId'] for item in response.get('items', [])]
            
            if video_ids:
                video_details = self._get_video_details(video_ids)
                videos.extend(video_details)
            
        except Exception as e:
            print(f"Error en búsqueda: {e}")
        
        return videos
    
    def _get_video_details(self, video_ids):
        """Obtiene detalles de videos"""
        details = []
        
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            
            try:
                response = self.youtube.videos().list(
                    part='snippet,contentDetails,statistics',
                    id=','.join(batch)
                ).execute()
                
                self.quota_used += 1
                
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
                print(f"Error: {e}")
        
        return details
    
    def get_video_comments(self, video_id, max_results=100):
        """Obtiene comentarios de un video"""
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
            print(f"Error: {e}")
        
        return comments
    
    def export_to_csv(self, data, filename="youtube_data.csv"):
        """Exporta a CSV"""
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Exportado: {filename} ({len(df)} registros)")
        return df
    
    def print_quota_status(self):
        """Muestra estado de la cuota"""
        print(f"\nCuota usada: {self.quota_used}/10,000")


# EJEMPLO DE USO
if __name__ == "__main__":
    # REEMPLAZAR con tu API Key
    API_KEY = "TU_API_KEY_AQUI"
    
    if API_KEY == "TU_API_KEY_AQUI":
        print("⚠️ Obtén tu API Key gratuita en Google Cloud Console")
        exit()
    
    monitor = YouTubeMonitor(API_KEY)
    
    # Buscar videos políticos
    videos = monitor.search_videos(
        "debate político Colombia",
        max_results=25,
        published_after=(datetime.utcnow() - timedelta(days=30)).isoformat() + 'Z'
    )
    
    if videos:
        monitor.export_to_csv(videos)
    
    monitor.print_quota_status()
