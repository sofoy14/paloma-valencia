"""
Analyzer Agent - Análisis de sentimiento y detección de alertas
"""
import os
import re
from textblob import TextBlob

try:
    import openai
    OPENAI_AVAILABLE = True
except:
    OPENAI_AVAILABLE = False

class AnalyzerAgent:
    """Agente especializado en analizar sentimiento y detectar alertas"""
    
    # Keywords de crisis/alerta
    ALERT_KEYWORDS = [
        'escándalo', 'denuncia', 'corrupción', 'investigación', 'proceso',
        'imputación', 'detención', 'acusación', 'fiscalía', 'captura',
        ' irregularidades', 'fraude', 'delito', 'penal'
    ]
    
    # Keywords positivas
    POSITIVE_KEYWORDS = [
        'victoria', 'triunfo', 'apoyo', 'liderazgo', 'reconocimiento',
        'avance', 'progreso', 'logro', 'éxito', 'ganar'
    ]
    
    def __init__(self, use_openai=False):
        self.use_openai = use_openai and OPENAI_AVAILABLE
        if self.use_openai:
            openai.api_key = os.getenv('OPENAI_API_KEY')
    
    def analyze_article(self, article):
        """Analiza un artículo completo"""
        text = f"{article.get('title', '')} {article.get('summary', '')}"
        
        # Análisis de sentimiento
        sentiment, score = self._analyze_sentiment(text)
        
        # Detección de alertas
        is_alert, alert_reason = self._detect_alert(text)
        
        # Extracción de keywords
        keywords = self._extract_keywords(text)
        
        return {
            'sentiment': sentiment,
            'sentiment_score': score,
            'is_alert': is_alert,
            'alert_reason': alert_reason,
            'keywords': keywords
        }
    
    def _analyze_sentiment(self, text):
        """Analiza el sentimiento del texto"""
        if not text:
            return 'neutral', 0.0
        
        # Método 1: TextBlob (rápido, gratuito)
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return sentiment, round(polarity, 3)
        except:
            pass
        
        # Método 2: Reglas simples (fallback)
        text_lower = text.lower()
        
        negative_count = sum(1 for word in ['no', 'sin', 'problema', 'crisis', 'mal', 'contra'] if word in text_lower)
        positive_count = sum(1 for word in ['sí', 'bueno', 'excelente', 'logro', 'apoyo', 'progreso'] if word in text_lower)
        
        if negative_count > positive_count:
            return 'negative', -0.3
        elif positive_count > negative_count:
            return 'positive', 0.3
        
        return 'neutral', 0.0
    
    def _detect_alert(self, text):
        """Detecta si el artículo debería generar una alerta"""
        if not text:
            return False, None
        
        text_lower = text.lower()
        
        # Verificar keywords de alerta
        found_alerts = []
        for keyword in self.ALERT_KEYWORDS:
            if keyword.lower() in text_lower:
                found_alerts.append(keyword)
        
        if found_alerts:
            return True, f"Keywords detectadas: {', '.join(found_alerts[:3])}"
        
        # Verificar sentimiento muy negativo
        sentiment, score = self._analyze_sentiment(text)
        if sentiment == 'negative' and score < -0.5:
            return True, "Sentimiento altamente negativo"
        
        return False, None
    
    def _extract_keywords(self, text):
        """Extrae keywords relevantes del texto"""
        if not text:
            return []
        
        # Lista de entidades políticas colombianas relevantes
        political_entities = [
            'paloma valencia', 'uribe', 'duque', 'petro', 'fico',
            'centro democratico', 'partido liberal', 'partido conservador',
            'cambio radical', 'coalicion', 'senado', 'congreso'
        ]
        
        text_lower = text.lower()
        found = []
        
        for entity in political_entities:
            if entity in text_lower:
                found.append(entity)
        
        return found
    
    def generate_summary(self, articles, hours=24):
        """Genera un resumen ejecutivo de las noticias"""
        if not articles:
            return "No hay noticias para analizar en el período."
        
        # Estadísticas
        total = len(articles)
        positive = sum(1 for a in articles if a.get('sentiment') == 'positive')
        negative = sum(1 for a in articles if a.get('sentiment') == 'negative')
        neutral = total - positive - negative
        alerts = sum(1 for a in articles if a.get('is_alert'))
        
        # Fuentes principales
        sources = {}
        for a in articles:
            src = a.get('source', 'Unknown')
            sources[src] = sources.get(src, 0) + 1
        top_sources = sorted(sources.items(), key=lambda x: x[1], reverse=True)[:3]
        
        summary = f"""## Resumen de Monitoreo - Últimas {hours}h

**Estadísticas:**
- Total noticias: {total}
- Sentimiento positivo: {positive} ({positive/total*100:.1f}%)
- Sentimiento negativo: {negative} ({negative/total*100:.1f}%)
- Sentimiento neutral: {neutral} ({neutral/total*100:.1f}%)
- Alertas detectadas: {alerts}

**Principales fuentes:**
"""
        for source, count in top_sources:
            summary += f"- {source}: {count} noticias\n"
        
        if alerts > 0:
            summary += f"\n⚠️ **Se detectaron {alerts} alertas que requieren atención.**\n"
        
        # Noticias más recientes
        summary += "\n**Noticias más recientes:**\n"
        recent = sorted(articles, key=lambda x: x.get('published_at', ''), reverse=True)[:5]
        for i, article in enumerate(recent, 1):
            sentiment_emoji = {'positive': '✅', 'negative': '⚠️', 'neutral': '⚪'}.get(article.get('sentiment'), '⚪')
            summary += f"{i}. {sentiment_emoji} {article.get('title', 'Sin título')[:80]}...\n"
        
        return summary
