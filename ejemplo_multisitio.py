"""
Ejemplo de scraping de noticias adaptado a diferentes sitios
Muestra cómo configurar selectores para distintas estructuras HTML
"""
import nodriver as uc
import json


# Configuración de selectores para diferentes sitios de noticias
SITES_CONFIG = {
    'hackernews': {
        'url': 'https://news.ycombinator.com/',
        'container': '.athing',
        'title': '.titleline > a',
        'metadata': '.subtext',
        'link_attr': 'href',
        'wait_for': '.athing'
    },
    'reddit_programming': {
        'url': 'https://www.reddit.com/r/programming/',
        'container': '[data-testid="post-container"]',
        'title': '[data-testid="post-title"]',
        'metadata': '[data-click-id="timestamp"]',
        'link_attr': None,  # Se extrae del title
        'wait_for': '[data-testid="post-container"]'
    }
}


async def scrape_site(browser, config_name):
    """Scrapea un sitio según su configuración"""
    config = SITES_CONFIG.get(config_name)
    if not config:
        print(f"❌ Configuración '{config_name}' no encontrada")
        return []
    
    print(f"\n🌐 Scrapeando: {config['url']}")
    
    # Navegar al sitio
    tab = await browser.get(config['url'])
    
    # Esperar a que cargue el contenido
    await tab.sleep(3)
    
    # Intentar cerrar banners de cookies si existen
    try:
        accept_btn = await tab.find("accept all", best_match=True)
        if accept_btn:
            await accept_btn.click()
            await tab.sleep(1)
    except:
        pass
    
    # Esperar elemento específico
    try:
        await tab.select(config['wait_for'], timeout=10)
    except:
        print(f"⚠️ No se pudo encontrar {config['wait_for']}")
    
    # Extraer artículos
    containers = await tab.select_all(config['container'])
    print(f"   Encontrados {len(containers)} contenedores")
    
    articles = []
    for container in containers[:15]:  # Limitar a 15 artículos
        try:
            title_elem = await container.select(config['title'])
            if not title_elem:
                continue
            
            title = title_elem.text.strip()
            
            # Extraer link
            link = ""
            if config['link_attr']:
                link = getattr(title_elem, config['link_attr'], '')
            else:
                # Intentar obtener href del elemento
                link = getattr(title_elem, 'href', '')
            
            # Extraer metadata
            meta_elem = await container.select(config['metadata'])
            metadata = meta_elem.text.strip() if meta_elem else ""
            
            articles.append({
                'title': title,
                'link': link,
                'metadata': metadata,
                'source': config_name
            })
        except Exception as e:
            continue
    
    print(f"   ✅ Extraídos {len(articles)} artículos")
    return articles


async def main():
    # Iniciar navegador
    print("🚀 Iniciando navegador...")
    browser = await uc.start(headless=False)
    
    all_articles = []
    
    try:
        # Scrapear Hacker News
        hn_articles = await scrape_site(browser, 'hackernews')
        all_articles.extend(hn_articles)
        
        # Scrapear Reddit Programming
        # reddit_articles = await scrape_site(browser, 'reddit_programming')
        # all_articles.extend(reddit_articles)
        
        # Mostrar resultados
        print("\n" + "="*70)
        print("RESULTADOS DEL SCRAPING")
        print("="*70)
        
        for i, art in enumerate(all_articles[:10], 1):
            print(f"\n{i}. [{art['source']}] {art['title'][:70]}")
            print(f"   🔗 {art['link'][:60]}...")
            print(f"   📊 {art['metadata'][:50]}...")
        
        # Guardar a JSON
        with open('articulos_scrapeados.json', 'w', encoding='utf-8') as f:
            json.dump(all_articles, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 {len(all_articles)} artículos guardados en 'articulos_scrapeados.json'")
        
    finally:
        browser.stop()
        print("\n✅ Navegador cerrado")


if __name__ == '__main__':
    uc.loop().run_until_complete(main())
