"""
Ejemplo completo de scraping de noticias usando nodriver
Extrae artículos de un sitio de noticias genérico
"""
import nodriver as uc
import asyncio
import json
from datetime import datetime


class NewsScraper:
    def __init__(self):
        self.browser = None
        self.articles = []
    
    async def start(self, headless=False):
        """Inicia el navegador"""
        self.browser = await uc.start(headless=headless)
        print("✅ Navegador iniciado")
    
    async def scrape_news_site(self, url, selectors):
        """
        Extrae artículos de un sitio de noticias
        
        Args:
            url: URL del sitio de noticias
            selectors: Dict con selectores CSS para título, link, descripción, fecha
        """
        print(f"\n🌐 Navegando a: {url}")
        tab = await self.browser.get(url)
        
        # Esperar a que cargue el contenido
        await tab.sleep(2)
        
        # Opcional: Aceptar cookies si aparece el banner
        await self._accept_cookies(tab)
        
        # Buscar contenedores de artículos
        article_selector = selectors.get('article', 'article')
        articles = await tab.select_all(article_selector)
        
        print(f"📰 Encontrados {len(articles)} artículos")
        
        for i, article in enumerate(articles[:10], 1):  # Limitar a 10 artículos
            try:
                data = await self._extract_article_data(article, selectors)
                if data['title']:
                    self.articles.append(data)
                    print(f"  ✓ Artículo {i}: {data['title'][:60]}...")
            except Exception as e:
                print(f"  ✗ Error en artículo {i}: {e}")
        
        return self.articles
    
    async def _accept_cookies(self, tab):
        """Intenta aceptar cookies si aparece el banner"""
        try:
            # Buscar botón de aceptar cookies por texto común
            accept_btn = await tab.find("accept all", best_match=True)
            if accept_btn:
                await accept_btn.click()
                print("✓ Cookies aceptadas")
                await tab.sleep(1)
        except:
            pass
    
    async def _extract_article_data(self, article_elem, selectors):
        """Extrae datos de un elemento artículo"""
        data = {
            'title': '',
            'link': '',
            'description': '',
            'date': '',
            'scraped_at': datetime.now().isoformat()
        }
        
        # Extraer título
        title_selector = selectors.get('title', 'h2 a, h3 a, .title')
        title_elem = await article_elem.select(title_selector)
        if title_elem:
            data['title'] = title_elem.text.strip()
            data['link'] = title_elem.href
        
        # Extraer descripción
        desc_selector = selectors.get('description', 'p, .description, .summary')
        desc_elem = await article_elem.select(desc_selector)
        if desc_elem:
            data['description'] = desc_elem.text.strip()
        
        # Extraer fecha
        date_selector = selectors.get('date', 'time, .date, .published')
        date_elem = await article_elem.select(date_selector)
        if date_elem:
            data['date'] = date_elem.text.strip()
        
        return data
    
    async def scrape_with_infinite_scroll(self, url, scroll_times=3):
        """
        Para sitios con scroll infinito (carga dinámica)
        """
        print(f"\n🌐 Navegando a: {url}")
        tab = await self.browser.get(url)
        
        # Scroll para cargar más contenido
        for i in range(scroll_times):
            print(f"  Scrolling... ({i+1}/{scroll_times})")
            await tab.scroll_down(800)
            await tab.sleep(2)
        
        # Extraer artículos después del scroll
        articles = await tab.select_all('article, .news-item, .post')
        print(f"📰 Encontrados {len(articles)} artículos después del scroll")
        
        for article in articles[:15]:
            try:
                title = await article.select('h2, h3, .title')
                link = await article.select('a')
                if title and link:
                    self.articles.append({
                        'title': title.text.strip(),
                        'link': link.href,
                        'description': '',
                        'scraped_at': datetime.now().isoformat()
                    })
            except:
                pass
        
        return self.articles
    
    def save_to_json(self, filename='noticias.json'):
        """Guarda los artículos en un archivo JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.articles, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Guardados {len(self.articles)} artículos en {filename}")
    
    def stop(self):
        """Cierra el navegador"""
        if self.browser:
            self.browser.stop()
            print("\n✅ Navegador cerrado")


# ==================== EJEMPLOS DE USO ====================

async def ejemplo_basico():
    """Ejemplo básico de scraping de noticias"""
    scraper = NewsScraper()
    
    try:
        await scraper.start(headless=False)
        
        # Ejemplo con un sitio de noticias real
        # Cambia la URL y selectores según el sitio que quieras scrapear
        
        # Para Hacker News (ejemplo simple)
        selectors_hn = {
            'article': '.athing',
            'title': '.titleline > a',
            'description': '.subtext',
            'date': '.age'
        }
        
        articles = await scraper.scrape_news_site(
            'https://news.ycombinator.com/',
            selectors_hn
        )
        
        # Mostrar resultados
        print("\n" + "="*60)
        print("RESULTADOS:")
        print("="*60)
        for i, art in enumerate(articles[:5], 1):
            print(f"\n{i}. {art['title']}")
            print(f"   Link: {art['link']}")
            print(f"   Fecha: {art['date']}")
        
        scraper.save_to_json('noticias_hackernews.json')
        
    finally:
        scraper.stop()


async def ejemplo_scroll_infinito():
    """Ejemplo para sitios con scroll infinito"""
    scraper = NewsScraper()
    
    try:
        await scraper.start(headless=False)
        
        # Ejemplo genérico para sitios con scroll infinito
        articles = await scraper.scrape_with_infinite_scroll(
            url='https://example-news-site.com',
            scroll_times=3
        )
        
        scraper.save_to_json('noticias_scroll.json')
        
    finally:
        scraper.stop()


async def ejemplo_simple_una_pagina():
    """Ejemplo más simple - una sola página"""
    browser = await uc.start(headless=False)
    
    try:
        tab = await browser.get('https://news.ycombinator.com/')
        
        # Esperar a que cargue
        await tab.select('.athing')
        
        # Extraer todos los títulos
        titles = await tab.select_all('.titleline > a')
        
        print("\n📰 Artículos de Hacker News:")
        print("="*60)
        
        for i, title in enumerate(titles[:10], 1):
            print(f"{i}. {title.text}")
            print(f"   → {title.href}\n")
        
    finally:
        browser.stop()


async def ejemplo_bypass_cloudflare():
    """Ejemplo de cómo bypass Cloudflare"""
    browser = await uc.start(headless=False)
    
    try:
        tab = await browser.get('https://www.nowsecure.nl')
        
        # Esperar carga
        await tab.sleep(3)
        
        # Si aparece el challenge de Cloudflare, nodriver lo maneja automáticamente
        # Pero también puedes verificar manualmente:
        
        if "cloudflare" in await tab.get_content():
            print("⚠️ Detectado Cloudflare, esperando...")
            await tab.sleep(5)
        
        # Intentar verificar checkbox de Cloudflare si existe
        try:
            await tab.cf_verify()  # Requiere opencv-python: pip install opencv-python
            print("✓ Cloudflare verificado")
        except:
            pass
        
        # Continuar con el scraping
        content = await tab.get_content()
        print(f"✓ Página cargada: {len(content)} caracteres")
        
    finally:
        browser.stop()


# ==================== EJECUTAR ====================

if __name__ == '__main__':
    print("="*60)
    print("SCRAPING DE NOTICIAS CON NODRIVER")
    print("="*60)
    
    # Ejecutar el ejemplo que prefieras:
    
    # 1. Ejemplo básico con Hacker News
    uc.loop().run_until_complete(ejemplo_basico())
    
    # 2. Ejemplo simple (descomenta para usar)
    # uc.loop().run_until_complete(ejemplo_simple_una_pagina())
    
    # 3. Ejemplo con bypass de Cloudflare (descomenta para usar)
    # uc.loop().run_until_complete(ejemplo_bypass_cloudflare())
