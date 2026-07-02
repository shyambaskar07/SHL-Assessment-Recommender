import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


CATALOG_URL = (
    "https://www.shl.com/solutions/products/"
    "product-catalog/"
)


driver = webdriver.Chrome(
    service=Service(
        ChromeDriverManager().install()
    )
)

driver.get(CATALOG_URL)

time.sleep(5)

cards = driver.find_elements(
    By.CSS_SELECTOR,
    "a[href*='/products/product-catalog/view/']"
)

urls = set()

for card in cards:
    href = card.get_attribute("href")

    if href and "/view/" in href:
        urls.add(href)

driver.quit()

with open(
    "data/raw_urls.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(
        sorted(list(urls)),
        f,
        indent=4
    )

print(
    f"Collected {len(urls)} URLs"
)