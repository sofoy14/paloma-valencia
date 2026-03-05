"""
Twitter/X Scraper usando Selenium
ADVERTENCIA: X/Twitter bloquea scraping agresivamente

Este código puede dejar de funcionar en cualquier momento
debido a los constantes cambios de X.

Alternativa recomendada: Usar Nitter (instancias limitadas)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd
from datetime import datetime

class TwitterScraper:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.setup_driver()
    
    def setup_driver(self):
        """Configura Chrome"""
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
    
    def scrape_user_tweets(self, username, max_tweets=20):
        """
        Extrae tweets de un usuario
        NOTA: X requiere login para ver muchos tweets
        """
        url = f"https://twitter.com/{username}"
        self.driver.get(url)
        time.sleep(5)
        
        tweets_data = []
        
        try:
            tweets = self.driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
            
            for tweet in tweets[:max_tweets]:
                try:
                    text_elem = tweet.find_element(By.CSS_SELECTOR, '[data-testid="tweetText"]')
                    text = text_elem.text
                    
                    tweets_data.append({
                        'username': username,
                        'text': text,
                        'scraped_at': datetime.now().isoformat()
                    })
                except:
                    continue
                    
        except Exception as e:
            print(f"Error: {e}")
        
        return tweets_data
    
    def close(self):
        if self.driver:
            self.driver.quit()


# EJEMPLO DE USO
if __name__ == "__main__":
    print("⚠️ ADVERTENCIA: X/Twitter bloquea scraping constantemente")
    print("Considera usar servicios pagos o la API oficial ($$$)")
    
    # scraper = TwitterScraper(headless=True)
    # try:
    #     tweets = scraper.scrape_user_tweets("usuario", max_tweets=10)
    #     print(tweets)
    # finally:
    #     scraper.close()
