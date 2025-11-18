
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
import os
import time
import random


driver = webdriver.Edge()

categories = [
    "amazon-renewed", "boost", "mobile-apps", "baby", "luggage",
    "beauty", "books", "apparel", "computers", "electronics", "garden", "gift-cards", "grocery",
    "hpc", "kitchen", "home-improvement", "industrial", "jewelry", "digital-text",
    "dvd", "music", "musical-instruments", "office", "pet-supplies", "shoes", "software",
    "sports", "toys", "videogames", "watches"
]
os.makedirs("amazon_bestseller", exist_ok=True)

for catg in categories:
    page = 1
    while True:
        
        time.sleep(random.uniform(5, 8))
        url = f"https://www.amazon.in/gp/bestsellers/{catg}/ref=zg_bs_pg_{page}_{catg}?ie=UTF8&pg={page}"
        driver.get(url)
        time.sleep(3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        elems = driver.find_elements(By.CSS_SELECTOR, "div.p13n-sc-uncoverable-faceout")
        print(f"[{catg} - Page {page}] Total products:", len(elems))

        if not elems:
            break  # Exit loop if no products found

        for idx, elem in enumerate(elems):
            d = elem.get_attribute("outerHTML")
            if d:
                filename = f"amazon_bestseller/{catg}_page{page}_item{idx+1}.html"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(d)
                    print(f"Saved: {filename}")


        page += 1

driver.quit()
