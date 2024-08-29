import os
import subprocess
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_tiktok_video_urls(profile_url):
    edge_options = Options()
    edge_options.add_argument("--no-sandbox")
    edge_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Edge(service=EdgeService(), options=edge_options)
    driver.get(profile_url)

    time.sleep(10)


    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@href, "/video/")]')))

    video_urls = []
    elements = driver.find_elements(By.XPATH, '//a[contains(@href, "/video/")]')
    for elem in elements:
        href = elem.get_attribute('href')
        if href:
            video_urls.append(href)

    driver.quit()
    return video_urls


def download_tiktok_videos(video_urls):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    for url in video_urls:
        output_path = os.path.join(desktop_path, '%(title)s.%(ext)s')
        subprocess.run(['yt-dlp', '-o', output_path, url])


profile_url = 'https://www.tiktok.com/@XXXX'  #Instead of X, write the nickname.

video_urls = get_tiktok_video_urls(profile_url)

print(f'Download Links: {video_urls}')


download_tiktok_videos(video_urls)
