# from TikTokApi import TikTokApi

# def download_tiktok_video(url, path):
#     # Initialize the TikTokApi
#     api = TikTokApi()

#     try:
#         # Get the video by URL
#         video_data = api.video(url=url)
#         # Download the video bytes
#         video_bytes = video_data.bytes()

#         # Save the video to the specified path
#         with open(path, "wb") as file:
#             file.write(video_bytes)
#         print(f"Video downloaded successfully to {path}")
#     finally:
#         # Clean up resources by closing the API connection properly
#         api.close()

# # URL of the TikTok video
# url = "https://www.tiktok.com/@metedanca/video/7432672150613462277?is_from_webapp=1&sender_device=pc&web_id=7456206532029220358"

# # Path where the video will be saved
# file_path = "/home/linoccm/07_WebScrapping/downloaded_video.mp4"

# # Call the function to download the video
# download_tiktok_video(url, file_path)



from bs4 import BeautifulSoup
from seleniumbase import Driver
from urllib.parse import urljoin
import time

# Your Bright Data Scraping Browser credentials
# AUTH = 'brd-customer-hl_bce0f29e-zone-scraping_browser1:w91l3u6tzami'
# SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

SBR_WEBDRIVER  =f'https://brd-customer-hl_a6de26b2-zone-scraping_browser1:dvvofz2u5jjd@brd.superproxy.io:9515'



def scrape_website(website):
    from selenium.webdriver import ChromeOptions
    from selenium.webdriver.remote.remote_connection import ChromiumRemoteConnection
    from selenium.webdriver.remote.webdriver import WebDriver as Remote

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
        time.sleep(3)  # Wait for videos to fully load
        html = driver.page_source
        return html


def get_video_urls(username_url):
    html = scrape_website(username_url)
    soup = BeautifulSoup(html, "html.parser")
    video_tags = soup.find_all("a", href=True)

    video_urls = []
    for tag in video_tags:
        href = tag["href"]
        if "/video/" in href:
            video_url = urljoin("https://www.tiktok.com", href)
            video_urls.append(video_url)

    # Remove duplicates
    return list(set(video_urls))


# Run test
if __name__ == "__main__":
    username_url = "https://www.tiktok.com/@anitta"  # You can change the username here
    urls = get_video_urls(username_url)
    print("Video URLs:")
    for url in urls:
        print(url)

