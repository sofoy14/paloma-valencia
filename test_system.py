#!/usr/bin/env python3
"""Test del sistema de monitoreo"""

from agents.rss_agent import RSSAgent
from agents.analyzer_agent import AnalyzerAgent
from agents.competitor_agent import CompetitorAgent

print("=" * 60)
print("TEST DEL SISTEMA DE MONITOREO")
print("=" * 60)

# Test RSS Agent
print("\n[1] RSS Agent - Modo all_politics")
rss = RSSAgent(mode='all_politics')
rss_articles = rss.fetch_all(max_age_hours=48, limit_per_source=5)
print(f"    Articulos encontrados: {len(rss_articles)}")

if rss_articles:
    print(f"\n    Ejemplo: {rss_articles[0]['title'][:60]}...")
    print(f"    Fuente: {rss_articles[0]['source']}")
    print(f"    Relevancia: {rss_articles[0].get('relevance_score', 0)}")

# Test Analyzer
print("\n[2] Analyzer Agent")
analyzer = AnalyzerAgent()
if rss_articles:
    result = analyzer.analyze_article(rss_articles[0])
    print(f"    Sentimiento: {result['sentiment']}")
    print(f"    Score: {result['sentiment_score']}")
    print(f"    Alerta: {result['is_alert']}")

# Test Competitor
print("\n[3] Competitor Agent")
comp = CompetitorAgent()
summary = comp.get_competitor_summary(rss_articles)
print(f"    Competidores detectados: {len(summary)}")
for name in summary:
    print(f"    - {name}: {summary[name]['mentions']} menciones")

print("\n" + "=" * 60)
print("OK - TODOS LOS AGENTES FUNCIONAN")
print("=" * 60)
