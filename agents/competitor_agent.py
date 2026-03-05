"""
Competitor Agent - Monitorea a otros candidatos y partidos
"""
from datetime import datetime, timezone

class CompetitorAgent:
    """Agente que monitorea la competencia electoral"""
    
    COMPETITORS = {
        'Gustavo Petro': {
            'keywords': ['petro', 'gustavo petro', 'presidente petro'],
            'party': 'Pacto Histórico'
        },
        'Federico Gutiérrez': {
            'keywords': ['fico', 'federico gutierrez', 'gutierrez'],
            'party': 'Centro Democrático'  # Aunque es del mismo partido, es competencia en algunos escenarios
        },
        'Sergio Fajardo': {
            'keywords': ['fajardo', 'sergio fajardo'],
            'party': 'Centro Esperanza'
        },
        'Partido Liberal': {
            'keywords': ['partido liberal', 'candidatos liberales'],
            'party': 'Liberal'
        },
        'Partido Conservador': {
            'keywords': ['partido conservador', 'candidatos conservadores'],
            'party': 'Conservador'
        }
    }
    
    def __init__(self):
        self.competitor_mentions = {name: [] for name in self.COMPETITORS.keys()}
    
    def analyze_competitor_mentions(self, articles):
        """Analiza menciones a competidores en artículos"""
        results = []
        
        for article in articles:
            text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
            
            for competitor, data in self.COMPETITORS.items():
                for keyword in data['keywords']:
                    if keyword.lower() in text:
                        results.append({
                            'article': article,
                            'competitor': competitor,
                            'party': data['party'],
                            'keyword_matched': keyword
                        })
                        break
        
        return results
    
    def get_competitor_summary(self, articles):
        """Genera resumen de actividad de competidores"""
        mentions = self.analyze_competitor_mentions(articles)
        
        summary = {}
        for competitor in self.COMPETITORS.keys():
            competitor_mentions = [m for m in mentions if m['competitor'] == competitor]
            if competitor_mentions:
                summary[competitor] = {
                    'mentions': len(competitor_mentions),
                    'latest': competitor_mentions[0]['article']['title'],
                    'sentiment': self._avg_sentiment([m['article'] for m in competitor_mentions])
                }
        
        return summary
    
    def _avg_sentiment(self, articles):
        """Calcula sentimiento promedio de artículos"""
        scores = []
        for a in articles:
            if a.get('sentiment') == 'positive':
                scores.append(1)
            elif a.get('sentiment') == 'negative':
                scores.append(-1)
            else:
                scores.append(0)
        
        if not scores:
            return 'neutral'
        
        avg = sum(scores) / len(scores)
        if avg > 0.2:
            return 'positive'
        elif avg < -0.2:
            return 'negative'
        return 'neutral'
