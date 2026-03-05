"""
Gemini Agent - IA para análisis avanzado de noticias
Usa Google Gemini (1.5 Flash, 1.5 Pro, 3.0 Flash) para análisis inteligente
"""
import os
import json
import time
from datetime import datetime, timezone
import google.generativeai as genai

class GeminiAgent:
    """
    Agente de IA usando Google Gemini para:
    - Análisis de sentimiento avanzado
    - Resúmenes inteligentes
    - Detección de crisis/alertas
    - Análisis de tendencias
    - Extracción de entidades políticas
    """
    
    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.enabled = False
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                # Usar Flash por defecto (rápido y económico)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
                self.enabled = True
                print("[Gemini] IA activada - Usando Gemini 1.5 Flash")
            except Exception as e:
                print(f"[Gemini] Error inicializando: {e}")
                self.model = None
        else:
            print("[Gemini] No configurado - Usando análisis básico")
    
    def analyze_article_advanced(self, title, content, source):
        """Análisis avanzado de una noticia usando Gemini"""
        if not self.enabled or not self.model:
            return None
        
        try:
            prompt = f"""
            Analiza esta noticia sobre las elecciones en Colombia y responde SOLO con JSON válido:
            
            TÍTULO: {title}
            CONTENIDO: {content[:1000]}
            FUENTE: {source}
            
            Responde con este formato JSON exacto:
            {{
                "sentimiento": "positivo|negativo|neutral",
                "confianza": 0.0-1.0,
                "relevancia_electoral": 0-100,
                "riesgo_desarrollo_elecciones": true|false,
                "tipo_riesgo": "violencia|intimidacion|irregularidades|logistica|desinformacion|null",
                "es_alerta_urgente": true|false,
                "razon_alerta": "explicacion breve o null",
                "ubicacion_mencionada": "municipio/departamento o null",
                "temas_principales": ["tema1", "tema2"],
                "grupos_armados_mencionados": ["grupo1"] o [],
                "resumen_2lineas": "resumen muy breve"
            }}
            
            CRITERIOS PARA ALERTAS URGENTES (riesgo_desarrollo_elecciones = true):
            - Presencia de grupos armados (ELN, Clan del Golfo, FARC disidencias, etc.)
            - Violencia o intimidación en zonas electorales
            - Irregularidades en logística electoral (urnas, transporte, puestos de votación)
            - Cierres de vías o bloqueos que impidan votar
            - Denuncias de fraude o compra de votos
            - Amenazas a candidatos, testigos o votantes
            - Problemas de seguridad en puestos de votación
            
            Relevancia electoral:
            - 90-100: Riesgo inmediato para desarrollo de elecciones en zona específica
            - 70-89: Problemas logísticos o de seguridad que podrían afectar votación
            - 50-69: Denuncias o irregularidades menores
            - 0-49: Noticias políticas normales sin impacto en logística electoral
            """
            
            response = self.model.generate_content(prompt)
            
            # Limpiar respuesta y parsear JSON
            text = response.text.strip()
            # Remover markdown si existe
            if text.startswith('```json'):
                text = text[7:]
            if text.endswith('```'):
                text = text[:-3]
            text = text.strip()
            
            result = json.loads(text)
            
            return {
                'sentiment': result.get('sentimiento', 'neutral'),
                'confidence': result.get('confianza', 0.5),
                'relevance_score': result.get('relevancia_electoral', 0),
                'is_alert': result.get('es_alerta_urgente', False),
                'alert_reason': result.get('razon_alerta'),
                'election_risk': result.get('riesgo_desarrollo_elecciones', False),
                'risk_type': result.get('tipo_riesgo'),
                'location': result.get('ubicacion_mencionada'),
                'armed_groups': result.get('grupos_armados_mencionados', []),
                'topics': result.get('temas_principales', []),
                'ai_summary': result.get('resumen_2lineas', ''),
                'analyzed_by': 'gemini-3.0-flash'
            }
            
        except Exception as e:
            print(f"[Gemini] Error analizando: {e}")
            return None
    
    def generate_campaign_report(self, articles, hours=24):
        """Genera reporte de campaña inteligente con IA"""
        if not self.enabled or not self.model or not articles:
            return None
        
        try:
            # Preparar resumen de artículos
            articles_text = "\n\n".join([
                f"- {a.get('title', '')} (Fuente: {a.get('source', '')}, Sentimiento: {a.get('sentiment', 'neutral')})"
                for a in articles[:20]  # Limitar a 20 para no sobrecargar
            ])
            
            prompt = f"""
            Eres un analista de seguridad electoral experto. Genera un informe ejecutivo sobre riesgos
            y amenazas al desarrollo de las elecciones en Colombia en las últimas {hours} horas.
            
            NOTICIAS MONITOREADAS:
            {articles_text}
            
            Genera un informe en formato markdown con:
            
            1. ## Resumen Ejecutivo (3-4 párrafos)
            2. ## Tendencias Principales (bullet points)
            3. ## Análisis de Sentimiento
            4. ## Riesgos y Oportunidades
            5. ## Recomendaciones para la Campaña
            
            Sé objetivo, profesional y estratégico. Máximo 500 palabras.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"[Gemini] Error generando reporte: {e}")
            return None
    
    def analyze_competitor_activity(self, articles, competitor_name):
        """Analiza actividad de un competidor específico"""
        if not self.enabled or not self.model:
            return None
        
        try:
            relevant = [a for a in articles if competitor_name.lower() in a.get('title', '').lower()]
            
            if not relevant:
                return f"No se encontraron noticias sobre {competitor_name} en el período."
            
            articles_text = "\n".join([f"- {a.get('title')}" for a in relevant[:10]])
            
            prompt = f"""
            Analiza la actividad mediática de {competitor_name} basándote en estas noticias:
            
            {articles_text}
            
            Proporciona:
            1. Narrativa principal (de qué hablan)
            2. Sentimiento general de la cobertura
            3. Temas recurrentes
            4. Impacto potencial en la campaña de Paloma Valencia
            
            Responde en 2-3 párrafos concisos.
            """
            
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            print(f"[Gemini] Error analizando competidor: {e}")
            return None
    
    def detect_fake_news_risk(self, title, content, source):
        """Detecta riesgo de desinformación"""
        if not self.enabled or not self.model:
            return None
        
        try:
            prompt = f"""
            Evalúa el riesgo de que esta noticia sea desinformación o fake news:
            
            Título: {title}
            Fuente: {source}
            Contenido: {content[:800]}
            
            Responde con JSON:
            {{
                "riesgo_fake_news": "alto|medio|bajo",
                "confianza_fuente": "alta|media|baja",
                "indicadores_sospechosos": ["indicador1", "indicador2"],
                "recomendacion": "texto breve"
            }}
            
            Indicadores de riesgo: titular amarillista, falta de fuentes,
            lenguaje exagerado, información no verificable.
            """
            
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            
            if text.startswith('```json'):
                text = text[7:]
            if text.endswith('```'):
                text = text[:-3]
            
            return json.loads(text.strip())
            
        except Exception as e:
            print(f"[Gemini] Error detectando fake news: {e}")
            return None
    
    def quick_sentiment(self, text):
        """Análisis rápido de sentimiento (fallback)"""
        if not self.enabled or not self.model:
            return None
        
        try:
            prompt = f"Clasifica el sentimiento como positivo, negativo o neutral. Responde solo una palabra:\n\n{text[:500]}"
            response = self.model.generate_content(prompt)
            return response.text.strip().lower()
        except:
            return None
