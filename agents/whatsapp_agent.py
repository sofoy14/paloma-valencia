"""
WhatsApp Agent - Envío de alertas por WhatsApp
Usa Twilio API (requiere cuenta Twilio)
"""
import os
from twilio.rest import Client
from datetime import datetime

class WhatsAppAgent:
    """Agente para enviar alertas de monitoreo por WhatsApp"""
    
    def __init__(self):
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.from_number = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')  # Sandbox de Twilio
        self.to_number = os.getenv('ALERT_PHONE_NUMBER', 'whatsapp:+573174018932')  # Número del usuario
        
        if self.account_sid and self.auth_token:
            self.client = Client(self.account_sid, self.auth_token)
            self.enabled = True
        else:
            self.client = None
            self.enabled = False
            print("[WhatsApp] Modo desactivado - Configura TWILIO_ACCOUNT_SID y TWILIO_AUTH_TOKEN")
    
    def send_alert(self, title, source, reason, url, relevance=0):
        """Envía una alerta por WhatsApp"""
        if not self.enabled:
            print(f"[WhatsApp] ALERTA SIMULADA (Twilio no configurado):")
            print(f"  - {title[:60]}...")
            return False
        
        try:
            emoji = "🚨" if relevance >= 50 else "⚠️" if relevance >= 30 else "📰"
            
            message = f"""{emoji} *ALERTA DE MONITOREO - Paloma Valencia*

📰 *{title[:100]}*

📡 Fuente: {source}
🔥 Relevancia: {relevance}/100
⚠️ Razón: {reason}

🔗 {url}

⏰ {datetime.now().strftime('%H:%M - %d/%m/%Y')}"""

            msg = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=self.to_number
            )
            
            print(f"[WhatsApp] Alerta enviada - SID: {msg.sid}")
            return True
            
        except Exception as e:
            print(f"[WhatsApp] Error enviando: {e}")
            return False
    
    def send_hourly_report(self, stats, top_articles):
        """Envía reporte de la hora"""
        if not self.enabled:
            print("[WhatsApp] REPORTE SIMULADO (Twilio no configurado)")
            return False
        
        try:
            message = f"""📊 *REPORTE HORARIO - Monitoreo*

📈 Estadísticas (última hora):
• Total noticias: {stats.get('total', 0)}
• Positivas: {stats.get('positive', 0)} ✅
• Negativas: {stats.get('negative', 0)} ⚠️
• Alertas: {stats.get('alerts', 0)} 🚨

📰 Noticias destacadas:
"""
            for i, article in enumerate(top_articles[:3], 1):
                sentiment = "✅" if article.get('sentiment') == 'positive' else "⚠️" if article.get('sentiment') == 'negative' else "⚪"
                message += f"\n{i}. {sentiment} {article.get('title', 'Sin título')[:50]}...\n"
            
            message += f"\n⏰ {datetime.now().strftime('%H:%M - %d/%m/%Y')}"

            msg = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=self.to_number
            )
            
            print(f"[WhatsApp] Reporte enviado - SID: {msg.sid}")
            return True
            
        except Exception as e:
            print(f"[WhatsApp] Error enviando reporte: {e}")
            return False
    
    def send_daily_digest(self, articles_summary):
        """Envía resumen diario"""
        if not self.enabled:
            return False
        
        try:
            message = f"""📋 *RESUMEN DIARIO - Paloma Valencia*

{articles_summary}

⏰ {datetime.now().strftime('%d/%m/%Y %H:%M')}"""

            self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=self.to_number
            )
            return True
        except Exception as e:
            print(f"[WhatsApp] Error: {e}")
            return False
