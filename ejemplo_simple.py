"""
Ejemplo simple y directo de scraping con nodriver
Extrae noticias de Hacker News
"""
import nodriver as uc


async def main():
    # 1. Iniciar navegador
    browser = await uc.start(headless=False)  # headless=True para modo sin ventana
    
    # 2. Ir al sitio
    tab = await browser.get('https://news.ycombinator.com/')
    
    # 3. Esperar a que cargue (busca un elemento específico)
    await tab.select('.athing')
    
    # 4. Extraer todos los artículos
    articles = await tab.select_all('.athing')
    
    print(f"📰 Total de artículos encontrados: {len(articles)}\n")
    print("="*70)
    
    # 5. Procesar cada artículo
    for i, article in enumerate(articles[:10], 1):
        # Extraer título
        title_elem = await article.select('.titleline > a')
        title = title_elem.text if title_elem else "Sin título"
        link = title_elem.href if title_elem else ""
        
        # Extraer metadata (puntos, comentarios)
        subtext = await article.find_next_sibling()
        meta = subtext.text if subtext else ""
        
        print(f"{i}. {title}")
        print(f"   🔗 {link}")
        print(f"   📊 {meta}")
        print()
    
    # 6. Guardar screenshot
    await tab.save_screenshot('hackernews.png')
    print("💾 Screenshot guardado como 'hackernews.png'")
    
    # 7. Cerrar navegador
    browser.stop()


# Ejecutar
if __name__ == '__main__':
    uc.loop().run_until_complete(main())
