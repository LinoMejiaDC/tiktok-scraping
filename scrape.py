from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import tempfile
import shutil


load_dotenv()

# AUTH = 'brd-customer-hl_bce0f29e-zone-scraping_browser1:w91l3u6tzami'
# SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

SBR_WEBDRIVER  =f'https://brd-customer-hl_a6de26b2-zone-scraping_browser1:dvvofz2u5jjd@brd.superproxy.io:9515'


#SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")



def scrape_website(website):
    print("Connecting to Scraping Browser...")
    sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
    with Remote(sbr_connection, options=ChromeOptions()) as driver:
        driver.get(website)
        print("Waiting captcha to solve...")
        solve_res = driver.execute(
            "executeCdpCommand",
            {
                "cmd": "Captcha.waitForSolve",
                "params": {"detectTimeout": 10000},
            },
        )
        print("Captcha solve status:", solve_res["value"]["status"])
        print("Navigated! Scraping page content...")
        html = driver.page_source
        return html


from tempfile import mkdtemp


def get_html(website):
    print("Initializing WebDriver...")

    # Set Chrome options
    options = Options()
    options.headless = True  # Run Chrome in headless mode
    options.add_argument("--incognito")  # Prevent profile conflicts
    options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional but safe)
    options.add_argument("--no-sandbox")  # Avoid sandboxing issues in some Linux environments
    options.add_argument("--disable-dev-shm-usage")  # Avoid shared memory issues on Linux

    # Path to your ChromeDriver
    service = Service("/home/linoccm/07_WebScrapping/AI-Web-Scraper/chromedriver")

    try:
        # Start WebDriver with options
        driver = webdriver.Chrome(service=service, options=options)

        # Load the website
        driver.get(website)
        print("Fetching page content...")

        # Get page HTML
        html = driver.page_source

        # Save to file
        output_path = "/home/linoccm/07_WebScrapping/AI-Web-Scraper/output/output2.txt"
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(html)

        print(f"HTML saved to {output_path}")
        return html

    finally:
        driver.quit()  # Always clean up
        
        

def get_html2(website):
    print("Initializing WebDriver...")
    
    # Create a temporary user data directory
    user_data_dir = tempfile.mkdtemp()

    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument(f"--user-data-dir={user_data_dir}")

    # Path to your chromedriver
    service = Service("/home/linoccm/07_WebScrapping/AI-Web-Scraper/chromedriver")
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get(website)
        print("Fetching page content...")

        # Wait until at least one video is loaded
        video_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[contains(@href, "/video/")]'))
        )

        video_url = video_link.get_attribute("href")
        print(f"Found video URL: {video_url}")

        html = driver.page_source
        output_path = "/home/linoccm/07_WebScrapping/AI-Web-Scraper/output/output.txt"
        with open(output_path, "w", encoding="utf-8") as file:
            file.write(html)

        print(f"HTML saved to {output_path}")
        return html, video_url

    finally:
        driver.quit()
        shutil.rmtree(user_data_dir)  # Clean up the temporary profile

        

def extract_body_content(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    body_content = soup.body
    if body_content:
        return str(body_content)
    return ""


def clean_body_content(body_content):
    soup = BeautifulSoup(body_content, "html.parser")

    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Get text or further process the content
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content


def split_dom_content(dom_content, max_length=6000):
    return [
        dom_content[i : i + max_length] for i in range(0, len(dom_content), max_length)
    ]
