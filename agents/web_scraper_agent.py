"""
Web Scraper Agent - Usa undetected-chromedriver para sitios sin RSS
Scraping de noticias de portales de los 32 departamentos
Compatible con Python 3.9
"""
import undetected_chromedriver as uc
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
import time

class WebScraperAgent:
    """
    Agente que usa undetected-chromedriver para scrapear
    portales de noticias que no tienen RSS feed
    """
    
    # Sitios de los 32 departamentos que NO tienen RSS
    DEPARTAMENTOS_SCRAPE = {
        'Arauca': {
            'La Voz del Cinaruco': {
                'url': 'https://lavozdelcinaruco.com',
                'selector_article': 'article, .post, .entry',
                'selector_title': 'h2 a, .entry-title a, h1 a',
            }
        },
        'Boyacá': {
            'Boyacá 7 Días': {
                'url': 'https://boyaca7dias.com.co',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .post-title a',
            }
        },
        'Caquetá': {
            'Caquetá al Día': {
                'url': 'https://caquetaaldia.com',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .entry-title a',
            }
        },
        'Cauca': {
            'El Nuevo Liberal': {
                'url': 'https://elnuevoliberal.com',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .post-title a',
            }
        },
        'Córdoba': {
            'La Razón': {
                'url': 'https://larazon.co',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .entry-title a',
            }
        },
        'Cundinamarca': {
            'Periodismo Público': {
                'url': 'https://periodismopublico.com',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .entry-title a',
            }
        },
        'La Guajira': {
            'Diario del Norte': {
                'url': 'https://diariodelnorte.net',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .post-title a',
            }
        },
        'Meta': {
            'Periódico del Meta': {
                'url': 'https://periodicodelmeta.com',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .entry-title a',
            }
        },
        'Nariño': {
            'Diario del Sur': {
                'url': 'https://diariodelsur.com.co',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .post-title a',
            }
        },
        'Norte de Santander': {
            'La Opinión': {
                'url': 'https://laopinion.co',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .post-title a',
            }
        },
        'Putumayo': {
            'Conexión Putumayo': {
                'url': 'https://conexionputumayo.com',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .post-title a',
            }
        },
        'Quindío': {
            'El Quindiano': {
                'url': 'https://elquindiano.com',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .post-title a',
            }
        },
        'Santander': {
            'Vanguardia Liberal': {
                'url': 'https://vanguardia.com',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .entry-title a',
            }
        },
        'Sucre': {
            'El Meridiano de Sucre': {
                'url': 'https://elmeridiano.co',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .post-title a',
            }
        },
        'Tolima': {
            'El Nuevo Día': {
                'url': 'https://elnuevodia.com.co',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .post-title a',
            }
        },
        'Amazonas': {
            'El Espectador Amazonas': {
                'url': 'https://www.elespectador.com/tags/amazonas/',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .headline a',
            }
        },
        'Guainía': {
            'El Morichal': {
                'url': 'https://elmorichal.com',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .post-title a',
            }
        },
        'Guaviare': {
            'Guaviare Estéreo': {
                'url': 'https://guaviareestereo.com',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .post-title a',
            }
        },
        'Vaupés': {
            'El Morichal Vaupés': {
                'url': 'https://elmorichal.com/category/vaupes/',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .post-title a',
            }
        },
        'Vichada': {
            'Vichada al Día': {
                'url': 'https://vichadaaldia.co',
                'selector_article': 'article, .post',
                'selector_title': 'h2 a, .post-title a',
            }
        }
    }
    
    CAMPAIGN_KEYWORDS = [
        'paloma valencia', 'palomavalencia', 'centro democratico',
        'uribe', 'elecciones 2026', 'senado', 'congreso'
    ]
    
    def __init__(self):
        self.articles = []
        self.driver = None
    
    def _get_driver(self):
        """Inicializa el driver de Chrome si no existe"""
        if self.driver is None:
            options = uc.ChromeOptions()
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--disable-gpu')
            self.driver = uc.Chrome(options=options)
        return self.driver
    
    def scrape_all(self, max_age_hours=24, max_per_site=3):
        """Scrapea todos los sitios de departamentos"""
        all_articles = []
        
        # Solo procesar algunos sitios por ciclo para no saturar
        departamentos = list(self.DEPARTAMENTOS_SCRAPE.items())[:5]  # 5 por ciclo
        
        for departamento, medios in departamentos:
            for medio_name, config in medios.items():
                try:
                    articles = self._scrape_site(departamento, medio_name, config, max_per_site)
                    all_articles.extend(articles)
                except Exception as e:
                    print(f"[WebScraper] Error {departamento}/{medio_name}: {e}")
        
        self._close_driver()
        return all_articles
    
    def _scrape_site(self, departamento, medio_name, config, max_per_site):
        """Scrapea un sitio específico"""
        articles = []
        
        try:
            driver = self._get_driver()
            driver.get(config['url'])
            
            # Esperar carga
            time.sleep(3)
            
            # Obtener HTML
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            # Buscar artículos
            article_elements = soup.select(config['selector_article'])[:max_per_site]
            
            for element in article_elements:
                try:
                    title_elem = element.select_one(config['selector_title'])
                    if not title_elem:
                        continue
                    
                    title = title_elem.get_text(strip=True)
                    url = title_elem.get('href', '')
                    
                    # Arreglar URL
                    if url and url.startswith('/'):
                        url = config['url'].rstrip('/') + url
                    elif url and not url.startswith('http'):
                        url = config['url'].rstrip('/') + '/' + url
                    
                    relevance = self._calculate_relevance(title)
                    
                    article = {
                        'title': title,
                        'source': f"{medio_name} ({departamento})",
                        'url': url or config['url'],
                        'summary': '',
                        'published_at': datetime.now(timezone.utc).isoformat(),
                        'author': '',
                        'collected_via': 'web_scraper',
                        'relevance_score': relevance,
                        'region': departamento,
                        'mentions_candidate': 'paloma' in title.lower()
                    }
                    
                    articles.append(article)
                    
                except Exception as e:
                    continue
                    
        except Exception as e:
            print(f"[WebScraper] Error con {medio_name}: {e}")
        
        return articles
    
    def _close_driver(self):
        """Cierra el driver"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
    
    def scrape_sync(self, max_age_hours=24, max_per_site=3):
        """Versión síncrona para usar desde Flask"""
        return self.scrape_all(max_age_hours, max_per_site)
    
    def _calculate_relevance(self, title):
        """Calcula score de relevancia"""
        text = title.lower()
        score = 0
        
        if 'paloma valencia' in text:
            score += 40
        elif 'paloma' in text:
            score += 20
        
        if 'centro democratico' in text or 'centrodemocratico' in text:
            score += 20
        
        if any(x in text for x in ['elecciones', 'senado', 'congreso', 'candidat']):
            score += 15
        
        if 'uribe' in text:
            score += 10
        
        return min(score, 100)
