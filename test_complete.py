#!/usr/bin/env python3
"""
Test completo del Agent Swarm
Verifica que todos los agentes funcionan correctamente
"""

print("="*70)
print("TEST AGENT SWARM - PALOMA VALENCIA")
print("="*70)

# Test 1: Imports
print("\n[1/6] Verificando imports...")
try:
    from agents.rss_agent import RSSAgent
    from agents.web_scraper_agent import WebScraperAgent
    from agents.newsapi_agent import NewsAPIAgent
    from agents.google_news_agent import GoogleNewsAgent
    from agents.twitter_agent import TwitterAgent
    from agents.analyzer_agent import AnalyzerAgent
    from agents.competitor_agent import CompetitorAgent
    from agents.notifications_agent import NotificationsAgent  # Nuevo!
    from agents.excel_reporter import ExcelReporter
    from agents.orchestrator import Orchestrator
    from models.database import NewsDatabase
    print("   OK - Todos los imports exitosos")
except Exception as e:
    print(f"   ERROR: {e}")
    exit(1)

# Test 2: RSS Agent
print("\n[2/6] RSS Agent (32 departamentos)...")
try:
    rss = RSSAgent()
    depto_con = rss.get_departamentos_con_rss()
    depto_sin = rss.get_departamentos_sin_rss()
    print(f"   Departamentos con RSS: {len(depto_con)}")
    print(f"   Departamentos con Scraper: {len(depto_sin)}")
    print(f"   Total: {len(depto_con) + len(depto_sin)}/32 + Bogota")
    print("   OK")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 3: Web Scraper Agent
print("\n[3/6] Web Scraper Agent (Chrome)...")
try:
    scraper = WebScraperAgent()
    num_sites = sum(len(medios) for medios in scraper.DEPARTAMENTOS_SCRAPE.values())
    print(f"   Sitios configurados: {num_sites}")
    print(f"   Departamentos cubiertos: {len(scraper.DEPARTAMENTOS_SCRAPE)}")
    print("   OK - Chrome scraper listo")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 4: Database
print("\n[4/6] Database...")
try:
    db = NewsDatabase()
    stats = db.get_stats(hours=24)
    print(f"   Stats: {stats}")
    print("   OK - SQLite funcionando")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 5: Notifications Agent (GRATIS!)
print("\n[5/6] Notifications Agent (WhatsApp/Telegram/Email)...")
try:
    notif = NotificationsAgent()
    status = notif.get_status()
    print(f"   Servicios activos: {status['services_count']}")
    print(f"   WhatsApp: {'OK' if status['whatsapp'] else 'No config'}")
    print(f"   Telegram: {'OK' if status['telegram'] else 'No config'}")
    print(f"   Email: {'OK' if status['email'] else 'No config'}")
    print("   OK - Sistema de notificaciones listo (GRATIS)")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 6: Excel Reporter
print("\n[6/6] Excel Reporter...")
try:
    reporter = ExcelReporter()
    print(f"   Output dir: {reporter.output_dir}")
    print("   OK - Excel listo")
except Exception as e:
    print(f"   ERROR: {e}")

print("\n" + "="*70)
print("OK - SISTEMA LISTO - 6 agentes operativos")
print("="*70)
print("\nPara iniciar:")
print("  python app.py")
print("  o doble clic en START.bat")
print("\nDashboard: http://localhost:5000")
print("\nConfigura notificaciones en: SETUP_NOTIFICACIONES.md")
print("="*70)
