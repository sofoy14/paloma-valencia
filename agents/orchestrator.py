"""
Orchestrator - Coordina el Agent Swarm completo
Gestiona 6 agentes para cobertura total de Colombia (32 departamentos)
"""
from datetime import datetime, timezone
from threading import Thread
import time

class Orchestrator:
    """
    Orchestrator del Agent Swarm para monitoreo electoral.
    Coordina 6 agentes especializados:
    1. RSS Agent - Fuentes con RSS (nacionales + 13 departamentos)
    2. Web Scraper Agent - Fuentes sin RSS (19 departamentos via nodriver)
    3. NewsAPI Agent - APIs de noticias
    4. Google News Agent - Búsquedas
    5. Twitter/X Agent - Redes sociales
    6. Analyzer Agent - Procesamiento NLP
    """
    
    def __init__(self, db, rss_agent, web_scraper_agent, newsapi_agent, 
                 google_news_agent, twitter_agent, analyzer_agent, 
                 competitor_agent, notifications_agent, reporter):
        
        self.db = db
        self.agents = {
            'rss': rss_agent,
            'web_scraper': web_scraper_agent,
            'newsapi': newsapi_agent,
            'google_news': google_news_agent,
            'twitter': twitter_agent,
            'analyzer': analyzer_agent,
            'competitor': competitor_agent,
            'whatsapp': notifications_agent,
            'reporter': reporter
        }
        
        self.stats = {
            'total_cycles': 0,
            'articles_collected': 0,
            'alerts_sent': 0,
            'last_run': None
        }
    
    def run_full_cycle(self, socketio=None):
        """Ejecuta un ciclo completo de monitoreo con todos los agentes"""
        start_time = time.time()
        print(f"\n{'='*80}")
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 AGENT SWARM - INICIANDO CICLO COMPLETO")
        print(f"{'='*80}")
        
        all_articles = []
        
        # ============================================================
        # AGENTE 1: RSS (Nacionales + 13 departamentos con RSS)
        # ============================================================
        rss_articles = self._run_agent('rss', lambda: self.agents['rss'].fetch_all(
            max_age_hours=2, 
            limit_per_source=8
        ))
        all_articles.extend(rss_articles)
        print(f"   📊 Subtotal RSS: {len(rss_articles)} artículos")
        
        # ============================================================
        # AGENTE 2: Web Scraper (19 departamentos sin RSS via nodriver)
        # ============================================================
        # Solo ejecutar cada 2 ciclos para no sobrecargar
        if self.agents.get('web_scraper') and self.stats['total_cycles'] % 2 == 0:
            web_articles = self._run_agent('web_scraper', lambda: self.agents['web_scraper'].scrape_sync(
                max_age_hours=24,
                max_per_site=3
            ))
            all_articles.extend(web_articles)
            print(f"   📊 Subtotal Web Scraper: {len(web_articles)} artículos")
        else:
            print(f"   ⏭️  Web Scraper omitido (no disponible o ciclo par)")
        
        # ============================================================
        # AGENTE 3: NewsAPI
        # ============================================================
        newsapi_articles = self._run_agent('newsapi', lambda: self.agents['newsapi'].fetch_all(hours_back=2))
        all_articles.extend(newsapi_articles)
        print(f"   📊 Subtotal NewsAPI: {len(newsapi_articles)} artículos")
        
        # ============================================================
        # AGENTE 4: Google News
        # ============================================================
        gn_articles = self._run_agent('google_news', lambda: self.agents['google_news'].search_political())
        all_articles.extend(gn_articles)
        print(f"   📊 Subtotal Google News: {len(gn_articles)} artículos")
        
        # ============================================================
        # AGENTE 5: Twitter/X
        # ============================================================
        twitter_articles = self._run_agent('twitter', lambda: self.agents['twitter'].monitor_all())
        all_articles.extend(twitter_articles)
        print(f"   📊 Subtotal Twitter/X: {len(twitter_articles)} tweets")
        
        # ============================================================
        # AGENTE 6: Analyzer (Procesa todo)
        # ============================================================
        print(f"\n   🤖 Analyzer Agent procesando {len(all_articles)} items...")
        processed = self._process_articles(all_articles, socketio)
        
        # ============================================================
        # Competitor Agent + IA
        # ============================================================
        try:
            competitor_summary = self.agents['competitor'].get_competitor_summary(processed)
            
            # Análisis con IA de competidores
            if self.agents['gemini'] and self.agents['gemini'].enabled and processed:
                for competitor in ['Gustavo Petro', 'Federico Gutiérrez']:
                    try:
                        ia_analysis = self.agents['gemini'].analyze_competitor_activity(processed, competitor)
                        if ia_analysis and competitor in competitor_summary:
                            competitor_summary[competitor]['ia_analysis'] = ia_analysis[:200]
                    except:
                        pass
            
            if socketio and competitor_summary:
                socketio.emit('competitor_update', competitor_summary)
        except Exception as e:
            print(f"   ⚠️  Competitor error: {e}")
        
        # ============================================================
        # Estadísticas
        # ============================================================
        elapsed = time.time() - start_time
        self.stats['total_cycles'] += 1
        self.stats['articles_collected'] += len(processed)
        self.stats['last_run'] = datetime.now()
        
        print(f"\n   {'='*76}")
        print(f"   ✅ CICLO COMPLETADO en {elapsed:.1f}s")
        print(f"   📈 Total artículos: {len(all_articles)}")
        print(f"   💾 Guardados: {len([p for p in processed if p.get('id')])}")
        print(f"   🚨 Alertas: {len([p for p in processed if p.get('is_alert')])}")
        print(f"   {'='*76}\n")
        
        return processed
    
    def _run_agent(self, agent_name, fetch_func):
        """Ejecuta un agente con manejo de errores"""
        try:
            print(f"\n   [{agent_name.upper()}] Recolectando...")
            return fetch_func()
        except Exception as e:
            print(f"   ❌ [{agent_name.upper()}] Error: {e}")
            return []
    
    def _process_articles(self, articles, socketio):
        """Procesa artículos con el analyzer y guarda en DB"""
        processed = []
        new_count = 0
        alert_count = 0
        
        for article in articles:
            try:
                # Análisis básico primero
                analysis = self.agents['analyzer'].analyze_article(article)
                article.update(analysis)
                
                # Análisis con IA (Gemini) si está disponible
                if self.agents['gemini'] and self.agents['gemini'].enabled:
                    try:
                        gemini_analysis = self.agents['gemini'].analyze_article_advanced(
                            article.get('title', ''),
                            article.get('summary', ''),
                            article.get('source', '')
                        )
                        if gemini_analysis:
                            # Mezclar análisis básico con IA
                            article.update(gemini_analysis)
                            # Sobrescribir con análisis más preciso de IA
                            article['sentiment'] = gemini_analysis.get('sentiment', article['sentiment'])
                            article['relevance_score'] = gemini_analysis.get('relevance_score', article.get('relevance_score', 0))
                            article['is_alert'] = gemini_analysis.get('is_alert', article.get('is_alert', False))
                    except Exception as e:
                        print(f"   ⚠️  Gemini analysis error: {e}")
                
                # Análisis específico para Twitter
                if article.get('collected_via') == 'twitter':
                    sent, score = self.agents['twitter'].analyze_tweet_sentiment(article)
                    article['sentiment'] = sent
                    article['sentiment_score'] = score
                
                # Guardar en DB
                article_id = self.db.save_article(article)
                
                if article_id:
                    article['id'] = article_id
                    new_count += 1
                    
                    # Enviar alerta si es relevante
                    if article.get('is_alert') or article.get('relevance_score', 0) >= 35:
                        alert_count += 1
                        self._send_alert(article)
                        
                        # Socket alert
                        if socketio:
                            socketio.emit('new_alert', {
                                'title': article['title'][:100],
                                'source': article['source'],
                                'reason': article.get('alert_reason', 'Alta relevancia'),
                                'url': article['url'],
                                'relevance': article.get('relevance_score', 0)
                            })
                
                processed.append(article)
                
            except Exception as e:
                print(f"   ⚠️  Error procesando artículo: {e}")
                continue
        
        # Emitir stats
        if socketio:
            stats = self.db.get_stats(hours=24)
            socketio.emit('stats_update', stats)
        
        self.stats['alerts_sent'] += alert_count
        return processed
    
    def _send_alert(self, article):
        """Envía alerta por WhatsApp"""
        try:
            self.agents['notifications'].send_alert(
                title=article['title'],
                source=article['source'],
                reason=article.get('alert_reason', f"Relevancia: {article.get('relevance_score', 0)}"),
                url=article['url'],
                relevance=article.get('relevance_score', 0)
            )
        except Exception as e:
            print(f"   ⚠️  WhatsApp error: {e}")
    
    def generate_hourly_report(self):
        """Genera reporte horario con IA"""
        try:
            print(f"\n[{datetime.now().strftime('%H:%M')}] 📊 Generando reporte horario...")
            
            articles = self.db.get_recent_articles(hours=1, limit=200)
            stats = self.db.get_stats(hours=1)
            
            # Excel
            hour_label = datetime.now().strftime('%Y%m%d_%H%M')
            filename = self.agents['reporter'].generate_hourly_report(articles, stats, hour_label)
            
            # Reporte con IA si está disponible
            if self.agents['gemini'] and self.agents['gemini'].enabled and articles:
                try:
                    ia_report = self.agents['gemini'].generate_campaign_report(articles, hours=1)
                    if ia_report:
                        print(f"   📝 Reporte IA generado ({len(ia_report)} chars)")
                except Exception as e:
                    print(f"   ⚠️  Error reporte IA: {e}")
            
            # Notificaciones
            top_articles = sorted(articles, key=lambda x: x.get('relevance_score', 0), reverse=True)[:5]
            self.agents['notifications'].send_hourly_report(stats, top_articles)
            
            print(f"   ✅ Reporte: {filename}")
            
        except Exception as e:
            print(f"   ❌ Error reporte: {e}")
    
    def get_coverage_stats(self):
        """Retorna estadísticas de cobertura"""
        depto_con_rss = self.agents['rss'].get_departamentos_con_rss()
        depto_sin_rss = self.agents['rss'].get_departamentos_sin_rss()
        
        stats = {
            'departamentos_con_rss': len(depto_con_rss),
            'departamentos_con_scraper': len(depto_sin_rss),
            'total_departamentos_cobertos': 32,
            'cobertura_total': f"{len(depto_con_rss) + len(depto_sin_rss)}/32",
            'agentes_activos': 6,
            'ciclos_completados': self.stats['total_cycles'],
            'articulos_totales': self.stats['articles_collected'],
            'alertas_enviadas': self.stats['alerts_sent']
        }
        
        # Info de IA
        if self.agents['gemini']:
            gemini_info = self.agents['gemini'].get_model_info()
            stats['ia_enabled'] = gemini_info['enabled']
            stats['ia_model'] = gemini_info['model']
        
        return stats
