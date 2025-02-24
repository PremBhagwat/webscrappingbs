from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager # type: ignore
from bs4 import BeautifulSoup
import logging
import time
import random
import csv


def get_random_user_agent() -> str:
    """Return a random user agent string"""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59"
    ]
    return random.choice(user_agents)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

def scrape_dell_support_page():
    url = "https://www.dell.com/support/home/en-us"
    
    try:
        # Set up Chrome options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
        
        # Initialize WebDriver with WebDriver Manager
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
        # Fetch the page
        driver.get(url)
        
        # Wait for page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        
        # Get page source
        page_source = driver.page_source
        
        # Parse HTML content
        soup = BeautifulSoup(page_source, "html.parser")
        
        # Extract and log images
        logging.info("\n=== Images ===")
        images = soup.find_all("img")
        for img in images:
            src = img.get("src", "No source URL")
            alt = img.get("alt", "No alt text")
            logging.info(f"Source: {src}\nAlt: {alt}\n")
        
        # Extract and log hyperlinks
        logging.info("\n=== Hyperlinks ===")
        links = soup.find_all("a")
        for link in links:
            href = link.get("href", "No URL")
            text = link.text.strip()
            if href and href.startswith(('http', '/')):
                logging.info(f"URL: {href}\nText: {text}\n")
        
        # Extract and log buttons
        logging.info("\n=== Buttons ===")
        buttons = soup.find_all("button")
        for button in buttons:
            text = button.text.strip()
            logging.info(f"Text: {text}\n")
        
        # Save data to CSV
        with open('scraped_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow(['Type', 'Source/URL', 'Text/Alt'])
            
            # Write images
            for img in images:
                writer.writerow(['Image', img.get("src", ""), img.get("alt", "")])
            
            # Write links
            for link in links:
                if link.get("href", "").startswith(('http', '/')):
                    writer.writerow(['Link', link.get("href", ""), link.text.strip()])
            
            # Write buttons
            for button in buttons:
                writer.writerow(['Button', '', button.text.strip()])
        
        # Log summary
        logging.info(f"\nSummary:\nImages found: {len(images)}\nLinks found: {len(links)}\nButtons found: {len(buttons)}")
        logging.info("Data saved to scraped_data.csv")

    
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        driver.quit()
        logging.info("Scraping completed.")

if __name__ == "__main__":
    scrape_dell_support_page()
