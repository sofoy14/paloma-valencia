"""
Sistema de Monitoreo Electoral - Paloma Valencia
Agent Swarm completo con cobertura de 32 departamentos
"""
import os
import sys
from datetime import datetime
from threading import Thread
from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

# Importar modelos y agentes
from models.database import NewsDatabase
from agents.rss_agent import RSSAgent
from agents.web_scraper_agent import WebScraperAgent
from agents.newsapi_agent import NewsAPIAgent
from agents.google_news_agent import GoogleNewsAgent
from agents.twitter_agent import TwitterAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.competitor_agent import CompetitorAgent
from agents.notifications_agent import NotificationsAgent
from agents.excel_reporter import ExcelReporter
from agents.orchestrator import Orchestrator

load_dotenv()

# Configuración Flask
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Inicializar componentes
db = NewsDatabase()
reporter = ExcelReporter(output_dir='reports')

# Inicializar agentes individuales
rss_agent = RSSAgent(mode='all_politics')
web_scraper_agent = WebScraperAgent()
newsapi_agent = NewsAPIAgent()
google_news_agent = GoogleNewsAgent()
twitter_agent = TwitterAgent()
analyzer_agent = AnalyzerAgent(use_openai=False)
competitor_agent = CompetitorAgent()
notifications_agent = NotificationsAgent()

# Orchestrator - Coordina todo el swarm
orchestrator = Orchestrator(
    db=db,
    rss_agent=rss_agent,
    web_scraper_agent=web_scraper_agent,
    newsapi_agent=newsapi_agent,
    google_news_agent=google_news_agent,
    twitter_agent=twitter_agent,
    analyzer_agent=analyzer_agent,
    competitor_agent=competitor_agent,
    notifications_agent=notifications_agent,
    reporter=reporter
)

# Scheduler
scheduler = BackgroundScheduler()

# Configuración

CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL_MINUTES', 5))

def run_monitoring_job():
    """Job de monitoreo ejecutado por el scheduler"""
    try:
        orchestrator.run_full_cycle(socketio=socketio)
    except Exception as e:
        print(f"[Scheduler] Error en monitoreo: {e}")

def run_hourly_report():
    """Job de reporte horario"""
    try:
        orchestrator.generate_hourly_report()
    except Exception as e:
        print(f"[Scheduler] Error en reporte: {e}")

# Configurar jobs
scheduler.add_job(
    run_monitoring_job,
    'interval',
    minutes=CHECK_INTERVAL,
    id='monitoring_job',
    replace_existing=True
)

scheduler.add_job(
    run_hourly_report,
    'interval',
    hours=1,
    id='hourly_report',
    replace_existing=True
)

# ============================================================
# RUTAS API
# ============================================================

@app.route('/')
def index():
    return send_from_directory('static', 'dashboard.html')

@app.route('/api/articles')
def get_articles():
    """Obtiene artículos con filtros"""
    hours = request.args.get('hours', 24, type=int)
    limit = request.args.get('limit', 200, type=int)
    sentiment = request.args.get('sentiment')
    min_relevance = request.args.get('min_relevance', 0, type=int)
    region = request.args.get('region')
    
    articles = db.get_recent_articles(hours=hours, limit=limit)
    
    if sentiment:
        articles = [a for a in articles if a.get('sentiment') == sentiment]
    if min_relevance > 0:
        articles = [a for a in articles if a.get('relevance_score', 0) >= min_relevance]
    if region and region != 'all':
        articles = [a for a in articles if (a.get('region') or 'Nacional') == region]
    
    return jsonify(articles)

@app.route('/api/stats')
def get_stats():
    """Obtiene estadísticas"""
    hours = request.args.get('hours', 24, type=int)
    return jsonify(db.get_stats(hours=hours))

@app.route('/api/coverage')
def get_coverage():
    """Obtiene estadísticas de cobertura de departamentos"""
    return jsonify(orchestrator.get_coverage_stats())

@app.route('/api/trigger', methods=['POST'])
def trigger_monitoring():
    """Dispara monitoreo manual"""
    thread = Thread(target=run_monitoring_job)
    thread.start()
    return jsonify({'status': 'Monitoreo iniciado', 'timestamp': datetime.now().isoformat()})

@app.route('/api/summary')
def get_summary():
    """Genera resumen ejecutivo"""
    hours = request.args.get('hours', 24, type=int)
    articles = db.get_recent_articles(hours=hours)
    summary = analyzer_agent.generate_summary(articles, hours=hours)
    return jsonify({'summary': summary})

@app.route('/api/competitors')
def get_competitors():
    """Obtiene análisis de competidores"""
    hours = request.args.get('hours', 24, type=int)
    articles = db.get_recent_articles(hours=hours)
    summary = competitor_agent.get_competitor_summary(articles)
    return jsonify(summary)

@app.route('/api/search', methods=['POST'])
def search_news():
    """Búsqueda manual en Google News"""
    data = request.json
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query required'}), 400
    
    articles = google_news_agent.search(query)
    return jsonify({'articles': articles, 'count': len(articles)})

@app.route('/api/notifications/test', methods=['POST'])
def test_notifications():
    """Envía mensaje de prueba"""
    results = notifications_agent.send_alert(
        title="Prueba Sistema - Paloma Valencia",
        source="Agent Swarm",
        reason="Configuración OK",
        url="http://localhost:5000",
        relevance=50
    )
    status = notifications_agent.get_status()
    return jsonify({
        'results': results,
        'services': status,
        'message': 'Mensaje enviado' if status['any_available'] else 'Modo simulado - Configura .env'
    })

@app.route('/api/reports/download/<filename>')
def download_report(filename):
    """Descarga reporte Excel"""
    filepath = os.path.join('reports', filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

@app.route('/api/reports/list')
def list_reports():
    """Lista reportes generados"""
    try:
        files = sorted([f for f in os.listdir('reports') if f.endswith('.xlsx')], reverse=True)
        return jsonify({'reports': files[:30]})
    except:
        return jsonify({'reports': []})

@app.route('/api/departamentos')
def get_departamentos():
    """Lista departamentos y su estado de cobertura"""
    con_rss = rss_agent.get_departamentos_con_rss()
    sin_rss = rss_agent.get_departamentos_sin_rss()
    
    return jsonify({
        'con_rss': con_rss,
        'con_web_scraper': sin_rss,
        'total': 32
    })

# ============================================================
# WEBSOCKET
# ============================================================

@socketio.on('connect')
def handle_connect():
    """Cliente conectado"""
    emit('connected', {
        'status': 'Agent Swarm activo',
        'services': notifications_agent.get_status(),
        'coverage': orchestrator.get_coverage_stats()
    })
    emit('stats_update', db.get_stats(hours=24))

@socketio.on('disconnect')
def handle_disconnect():
    pass

# ============================================================
# MAIN
# ============================================================

if __name__ == '__main__':
    # Banner
    print("\n" + "="*80)
    print("   🤖 AGENT SWARM - SISTEMA DE MONITOREO ELECTORAL")
    print("   Paloma Valencia - Elecciones Colombia 2026")
    print("="*80)
    
    coverage = orchestrator.get_coverage_stats()
    print(f"\n   📊 COBERTURA:")
    print(f"      • Departamentos con RSS: {coverage['departamentos_con_rss']}/32")
    print(f"      • Departamentos con Scraper: {coverage['departamentos_con_scraper']}/32")
    print(f"      • Total cubierto: 32/32 departamentos + Bogotá DC")
    print(f"\n   📱 Alertas WhatsApp: {ALERT_PHONE}")
    print(f"   📈 Reportes Excel: Cada hora en /reports/")
    print(f"   🌐 Dashboard: http://localhost:5000")
    print("="*80)
    
    # Crear directorios
    os.makedirs('reports', exist_ok=True)
    os.makedirs('data', exist_ok=True)
    
    # Iniciar scheduler
    scheduler.start()
    
    # Ciclo inicial
    print("\n🚀 Ejecutando ciclo inicial de monitoreo...\n")
    run_monitoring_job()
    
    # Iniciar servidor
    print("\n✅ Sistema activo - 6 agentes corriendo\n")
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, use_reloader=False)
