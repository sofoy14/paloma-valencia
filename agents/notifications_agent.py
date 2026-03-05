"""
Notifications Agent - Envío de alertas GRATIS
Opciones: CallMeBot (WhatsApp), Telegram, Email
Sin Twilio, 100% gratuito
"""
import os
import requests
from datetime import datetime

class NotificationsAgent:
    """
    Agente para enviar notificaciones GRATIS
    - CallMeBot: WhatsApp gratuito (https://www.callmebot.com/)
    - Telegram: Bot gratuito
    - Email: SMTP gratuito (Gmail)
    """
    
    def __init__(self):
        # CallMeBot (WhatsApp gratis)
        self.callmebot_apikey = os.getenv('CALLMEBOT_APIKEY', '')
        self.callmebot_phone = os.getenv('CALLMEBOT_PHONE', '573174018932')
        
        # Telegram
        self.telegram_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID', '')
        
        # Email (G SMTP)
        self.email_user = os.getenv('EMAIL_USER', '')
        self.email_password = os.getenv('EMAIL_PASSWORD', '')  # App password
        self.email_to = os.getenv('EMAIL_TO', 'paloma.campana@email.com')
        
        # Verificar qué servicios están disponibles
        self.services = []
        if self.callmebot_apikey:
            self.services.append('whatsapp')
        if self.telegram_token and self.telegram_chat_id:
            self.services.append('telegram')
        if self.email_user and self.email_password:
            self.services.append('email')
    
    def send_alert(self, title, source, reason, url, relevance=0):
        """Envía alerta por todos los servicios disponibles"""
        results = {}
        
        if 'whatsapp' in self.services:
            results['whatsapp'] = self._send_whatsapp(title, source, reason, url, relevance)
        
        if 'telegram' in self.services:
            results['telegram'] = self._send_telegram(title, source, reason, url, relevance)
        
        if 'email' in self.services:
            results['email'] = self._send_email(title, source, reason, url, relevance)
        
        # Si no hay servicios configurados, solo loguear
        if not self.services:
            print(f"[Notifications] ALERTA SIMULADA:")
            print(f"  📰 {title[:60]}...")
            print(f"  📡 {source}")
            print(f"  🔥 Relevancia: {relevance}")
            print(f"  ⚠️  {reason}")
            return {'simulated': True}
        
        return results
    
    def _send_whatsapp(self, title, source, reason, url, relevance):
        """Envía WhatsApp via CallMeBot (GRATIS)"""
        try:
            emoji = "🚨" if relevance >= 50 else "⚠️" if relevance >= 30 else "📰"
            
            message = f"""{emoji} *ALERTA - Paloma Valencia*

📰 *{title[:100]}*

📡 Fuente: {source}
🔥 Relevancia: {relevance}/100
⚠️ Razón: {reason}

🔗 {url}

⏰ {datetime.now().strftime('%H:%M %d/%m')}"""

            # CallMeBot API (gratis)
            api_url = f"https://api.callmebot.com/whatsapp.php"
            params = {
                'phone': self.callmebot_phone,
                'text': message,
                'apikey': self.callmebot_apikey
            }
            
            response = requests.get(api_url, params=params, timeout=30)
            
            if response.status_code == 200:
                print(f"[WhatsApp] Alerta enviada via CallMeBot")
                return True
            else:
                print(f"[WhatsApp] Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"[WhatsApp] Error: {e}")
            return False
    
    def _send_telegram(self, title, source, reason, url, relevance):
        """Envía Telegram Bot (GRATIS)"""
        try:
            emoji = "🚨" if relevance >= 50 else "⚠️" if relevance >= 30 else "📰"
            
            message = f"""{emoji} <b>ALERTA - Paloma Valencia</b>

📰 <b>{title[:100]}</b>

📡 Fuente: {source}
🔥 Relevancia: {relevance}/100
⚠️ Razón: {reason}

🔗 <a href="{url}">Ver noticia</a>

⏰ {datetime.now().strftime('%H:%M %d/%m')}"""

            api_url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            data = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'HTML',
                'disable_web_page_preview': True
            }
            
            response = requests.post(api_url, data=data, timeout=30)
            
            if response.status_code == 200:
                print(f"[Telegram] Alerta enviada")
                return True
            else:
                print(f"[Telegram] Error: {response.text}")
                return False
                
        except Exception as e:
            print(f"[Telegram] Error: {e}")
            return False
    
    def _send_email(self, title, source, reason, url, relevance):
        """Envía Email via Gmail SMTP"""
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            msg = MIMEMultipart()
            msg['From'] = self.email_user
            msg['To'] = self.email_to
            msg['Subject'] = f"🚨 Alerta Monitoreo - {title[:50]}..."
            
            body = f"""
<h2>🚨 Alerta de Monitoreo - Paloma Valencia</h2>

<h3>{title}</h3>

<p><strong>Fuente:</strong> {source}</p>
<p><strong>Relevancia:</strong> {relevance}/100</p>
<p><strong>Razón:</strong> {reason}</p>

<p><a href="{url}">🔗 Ver noticia completa</a></p>

<hr>
<p style="color: gray; font-size: 12px;">
    Enviado: {datetime.now().strftime('%d/%m/%Y %H:%M')}<br>
    Sistema de Monitoreo Electoral
</p>
"""
            
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_user, self.email_password)
            server.send_message(msg)
            server.quit()
            
            print(f"[Email] Alerta enviada a {self.email_to}")
            return True
            
        except Exception as e:
            print(f"[Email] Error: {e}")
            return False
    
    def send_hourly_report(self, stats, top_articles):
        """Envía reporte horario"""
        results = {}
        
        message = f"""📊 <b>REPORTE HORARIO - Paloma Valencia</b>

📈 <b>Estadísticas (última hora):</b>
• Total: {stats.get('total', 0)}
• Positivas: {stats.get('positive', 0)} ✅
• Negativas: {stats.get('negative', 0)} ⚠️
• Alertas: {stats.get('alerts', 0)} 🚨

📰 <b>Noticias destacadas:</b>
"""
        for i, article in enumerate(top_articles[:3], 1):
            emoji = "✅" if article.get('sentiment') == 'positive' else "⚠️" if article.get('sentiment') == 'negative' else "⚪"
            message += f"\n{i}. {emoji} {article.get('title', 'Sin título')[:50]}..."
        
        message += f"\n\n⏰ {datetime.now().strftime('%H:%M %d/%m/%Y')}"
        
        # Enviar por Telegram (más confiable para reportes largos)
        if 'telegram' in self.services:
            try:
                api_url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
                data = {
                    'chat_id': self.telegram_chat_id,
                    'text': message,
                    'parse_mode': 'HTML'
                }
                requests.post(api_url, data=data, timeout=30)
                results['telegram'] = True
            except Exception as e:
                print(f"[Telegram] Error reporte: {e}")
        
        # WhatsApp (versión corta)
        if 'whatsapp' in self.services:
            try:
                short_msg = f"""📊 Reporte Horario

Total: {stats.get('total', 0)} | Pos: {stats.get('positive', 0)} | Neg: {stats.get('negative', 0)}

Ver dashboard: http://localhost:5000"""
                
                api_url = f"https://api.callmebot.com/whatsapp.php"
                params = {
                    'phone': self.callmebot_phone,
                    'text': short_msg,
                    'apikey': self.callmebot_apikey
                }
                requests.get(api_url, params=params, timeout=30)
                results['whatsapp'] = True
            except Exception as e:
                print(f"[WhatsApp] Error reporte: {e}")
        
        return results
    
    def get_status(self):
        """Retorna estado de los servicios"""
        return {
            'whatsapp': 'whatsapp' in self.services,
            'telegram': 'telegram' in self.services,
            'email': 'email' in self.services,
            'any_available': len(self.services) > 0,
            'services_count': len(self.services)
        }
