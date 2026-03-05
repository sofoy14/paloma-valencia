"""
RSS Agent - Recolector de noticias de medios colombianos vía RSS
COBERTURA COMPLETA: 32 Departamentos + Bogotá DC
"""
import feedparser
from datetime import datetime, timedelta, timezone
import re

class RSSAgent:
    """Agente especializado en recolectar noticias de RSS feeds colombianos - 32 departamentos"""
    
    # ============================================================
    # FUENTES NACIONALES
    # ============================================================
    NATIONAL_SOURCES = {
        'El Tiempo': {
            'colombia': 'https://www.eltiempo.com/rss/colombia.xml',
            'politica': 'https://www.eltiempo.com/rss/politica.xml',
            'bogota': 'https://www.eltiempo.com/rss/bogota.xml',
            'judicial': 'https://www.eltiempo.com/rss/justicia.xml',
        },
        'El Espectador': {
            'politica': 'https://www.elespectador.com/politica/rss.xml',
            'judicial': 'https://www.elespectador.com/judicial/rss.xml',
            'colombia': 'https://www.elespectador.com/colombia/rss.xml',
        },
        'Semana': {
            'principal': 'https://www.semana.com/rss.xml',
            'politica': 'https://www.semana.com/rss/politica.xml',
        },
        'Caracol Radio': {
            'politica': 'https://caracol.com.co/rss.aspx?idSeccion=17',
            'judicial': 'https://caracol.com.co/rss.aspx?idSeccion=22',
        },
        'Blu Radio': {
            'politica': 'https://www.bluradio.com/rss/politica',
        },
        'RCN Radio': {
            'politica': 'https://www.rcnradio.com/rss/politica',
        },
        'Pulzo': {
            'principal': 'https://www.pulzo.com/rss',
        },
        'Infobae Colombia': {
            'principal': 'https://www.infobae.com/arc/outboundfeeds/rss/colombia/',
        },
        'La FM': {
            'principal': 'https://www.lafm.com.co/rss',
        },
        'City Paper Bogotá': {
            'principal': 'https://thecitypaperbogota.com/feed/',
        }
    }
    
    # ============================================================
    # FUENTES POR DEPARTAMENTO (32 + Bogotá)
    # ============================================================
    DEPARTAMENTAL_SOURCES = {
        # 1. AMAZONAS
        'Amazonas': {
            'El Espectador Amazonas': 'https://www.elespectador.com/tags/amazonas/rss.xml',
        },
        
        # 2. ANTIOQUIA
        'Antioquia': {
            'El Colombiano': 'https://www.elcolombiano.com/rss.xml',
            'Telemedellín': 'https://www.telemedellin.tv/feed/',
        },
        
        # 3. ARAUCA - Sin RSS confirmado (usa scraper)
        'Arauca': {},
        
        # 4. ATLÁNTICO
        'Atlántico': {
            'El Heraldo': 'https://www.elheraldo.co/rss',
            'Qhubo Barranquilla': 'https://qhubo.com/barranquilla/feed/',
        },
        
        # 5. BOLÍVAR
        'Bolívar': {
            'El Universal': 'https://www.eluniversal.com.co/feed',
        },
        
        # 6. BOYACÁ - Sin RSS confirmado (usa scraper)
        'Boyacá': {},
        
        # 7. CALDAS
        'Caldas': {
            'La Patria': 'https://www.lapatria.com/rss.xml',
        },
        
        # 8. CAQUETÁ - Sin RSS confirmado
        'Caquetá': {},
        
        # 9. CASANARE
        'Casanare': {
            'El Diario del Llano': 'https://eldiariodelllano.com/feed/',
        },
        
        # 10. CAUCA - Sin RSS confirmado
        'Cauca': {},
        
        # 11. CESAR
        'Cesar': {
            'El Pilón': 'https://elpilon.com.co/feed/',
        },
        
        # 12. CHOCÓ
        'Chocó': {
            'Chocó 7 Días': 'https://choco7dias.com/feed/',
        },
        
        # 13. CÓRDOBA - Sin RSS confirmado
        'Córdoba': {},
        
        # 14. CUNDINAMARCA - Sin RSS confirmado
        'Cundinamarca': {},
        
        # 15. GUAINÍA - Sin RSS confirmado
        'Guainía': {},
        
        # 16. GUAVIARE - Sin RSS confirmado
        'Guaviare': {},
        
        # 17. HUILA
        'Huila': {
            'Diario del Huila': 'https://www.diariodelhuila.com/feed/',
        },
        
        # 18. LA GUAJIRA - Sin RSS confirmado
        'La Guajira': {},
        
        # 19. MAGDALENA
        'Magdalena': {
            'El Informador': 'https://www.elinformador.com.co/feed/',
        },
        
        # 20. META - Sin RSS confirmado
        'Meta': {},
        
        # 21. NARIÑO - Sin RSS confirmado
        'Nariño': {},
        
        # 22. NORTE DE SANTANDER - Sin RSS confirmado
        'Norte de Santander': {},
        
        # 23. PUTUMAYO - Sin RSS confirmado
        'Putumayo': {},
        
        # 24. QUINDÍO - Sin RSS confirmado
        'Quindío': {},
        
        # 25. RISARALDA
        'Risaralda': {
            'El Diario': 'https://www.eldiario.com.co/feed/',
        },
        
        # 26. SAN ANDRÉS - Sin RSS confirmado
        'San Andrés y Providencia': {},
        
        # 27. SANTANDER - Sin RSS confirmado
        'Santander': {},
        
        # 28. SUCRE - Sin RSS confirmado
        'Sucre': {},
        
        # 29. TOLIMA - Sin RSS confirmado
        'Tolima': {},
        
        # 30. VALLE DEL CAUCA
        'Valle del Cauca': {
            'El País': 'https://www.elpais.com.co/feed/',
            'Occidente': 'https://occidente.co/feed/',
        },
        
        # 31. VAUPÉS - Sin RSS confirmado
        'Vaupés': {},
        
        # 32. VICHADA - Sin RSS confirmado
        'Vichada': {},
        
        # 33. BOGOTÁ DC
        'Bogotá DC': {
            'City TV': 'https://citytv.eltiempo.com/feed/',
            'Canal 1': 'https://canal1.com.co/feed/',
        }
    }
    
    CAMPAIGN_KEYWORDS = [
        'paloma valencia', 'palomavalencia', 'centro democratico',
        'elecciones 2026', 'elecciones colombia', 'jornada electoral',
        'urnas', 'puestos de votacion', 'mesa electoral',
        'testigo electoral', 'votacion', 'sufragio'
    ]
    
    ALERT_KEYWORDS = [
        'grupos armados', 'eln', 'clan del golfo', 'farc disidencias',
        'intimidacion', 'amenaza', 'violencia', 'ataque',
        'bloqueo', 'cierre de via', 'impedir votar',
        'irregularidades', 'fraude electoral', 'compra de votos',
        'urnas', 'logistica electoral', 'transporte electoral',
        'denuncia', 'fiscalia electoral', 'delito electoral'
    ]
    
    def __init__(self, mode='campaign'):
        self.mode = mode
    
    def fetch_all(self, max_age_hours=24, limit_per_source=10):
        """Recolecta noticias de TODAS las fuentes RSS disponibles"""
        all_articles = []
        
        # Nacionales
        for source_name, feeds in self.NATIONAL_SOURCES.items():
            for section, url in feeds.items():
                try:
                    articles = self._fetch_feed(source_name, section, url, max_age_hours, limit_per_source, 'Nacional')
                    all_articles.extend(articles)
                except Exception as e:
                    print(f"[RSS][Nacional] Error {source_name}: {e}")
        
        # Departamentales (solo los que tienen RSS)
        for depto, medios in self.DEPARTAMENTAL_SOURCES.items():
            if not medios:  # Skip si no hay medios con RSS
                continue
            for medio_name, url in medios.items():
                try:
                    articles = self._fetch_feed(medio_name, 'principal', url, max_age_hours, 5, depto)
                    all_articles.extend(articles)
                except Exception as e:
                    print(f"[RSS][{depto}] Error {medio_name}: {e}")
        
        all_articles.sort(key=lambda x: x.get('published_at', ''), reverse=True)
        return all_articles
    
    def _fetch_feed(self, source, section, url, max_age_hours, limit, region):
        """Obtiene noticias de un feed RSS"""
        articles = []
        
        feed = feedparser.parse(url)
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=max_age_hours)
        
        for entry in feed.entries[:limit]:
            try:
                published = self._parse_date(entry.get('published', entry.get('updated', '')))
                if published:
                    if published.tzinfo is None:
                        published = published.replace(tzinfo=timezone.utc)
                    if published < cutoff_time:
                        continue
                
                title = entry.get('title', '')
                summary = entry.get('summary', entry.get('description', ''))
                link = entry.get('link', '')
                
                relevance = self._calculate_relevance(title, summary)
                
                article = {
                    'title': title,
                    'source': source,
                    'url': link,
                    'summary': self._clean_html(summary)[:500] if summary else '',
                    'published_at': published.isoformat() if published else datetime.now(timezone.utc).isoformat(),
                    'author': entry.get('author', ''),
                    'collected_via': 'rss',
                    'relevance_score': relevance,
                    'region': region,
                    'mentions_candidate': 'paloma' in title.lower() or 'paloma' in str(summary).lower()
                }
                
                articles.append(article)
                
            except Exception as e:
                continue
        
        return articles
    
    def _calculate_relevance(self, title, summary):
        """Calcula score de relevancia 0-100"""
        text = f"{title} {summary}".lower()
        score = 0
        
        # Mención directa (40 puntos)
        if 'paloma valencia' in text:
            score += 40
        elif 'paloma' in text:
            score += 20
        
        # Centro Democrático (20 puntos)
        if 'centro democratico' in text or 'centrodemocratico' in text:
            score += 20
        
        # Temas electorales (20 puntos)
        if any(x in text for x in ['elecciones', 'senado', 'congreso', 'candidat', 'urna', 'voto']):
            score += 20
        
        # Uribe (10 puntos)
        if 'uribe' in text:
            score += 10
        
        # Regional (5 puntos)
        if any(x in text for x in ['bogotá', 'bogota', 'medellín', 'medellin', 'cali']):
            score += 5
        
        # Alerta keywords
        if any(x in text for x in self.ALERT_KEYWORDS):
            score += 10
        
        return min(score, 100)
    
    def _parse_date(self, date_str):
        """Parsea fechas"""
        if not date_str:
            return None
        
        try:
            struct_time = feedparser._parse_date(date_str)
            if struct_time:
                return datetime(*struct_time[:6]).replace(tzinfo=timezone.utc)
        except:
            pass
        
        formats = [
            '%a, %d %b %Y %H:%M:%S %z',
            '%a, %d %b %Y %H:%M:%S GMT',
            '%Y-%m-%dT%H:%M:%S%z',
            '%Y-%m-%dT%H:%M:%S',
            '%d/%m/%Y %H:%M:%S',
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
            except:
                continue
        
        return datetime.now(timezone.utc)
    
    def _clean_html(self, html):
        """Limpia HTML"""
        if not html:
            return ''
        clean = re.sub(r'<[^>]+>', '', html)
        return clean.strip()
    
    def get_departamentos_con_rss(self):
        """Retorna lista de departamentos que tienen RSS"""
        return [d for d, medios in self.DEPARTAMENTAL_SOURCES.items() if medios]
    
    def get_departamentos_sin_rss(self):
        """Retorna lista de departamentos que necesitan scraper"""
        return [d for d, medios in self.DEPARTAMENTAL_SOURCES.items() if not medios]
