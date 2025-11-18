from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import pandas as pd
import time
import os
import re

# Output CSV path
output_file = "amazon_scraped_data.csv"

# Initialize data dictionary
data_csv = {
    "title": [],
    "rating": [],
    "link": [],
    "category": [],
    "image": [],
    "img_url": [],
    "scrap_time": [],
    "price": [],
    "gender":[]
}


def gender_inter(text):
    text= text.lower()
    if any(word in text for word in ["men","gents","male","men's"]):
        return "Men"
    if any(word in text  for word in ["womem","women","lady","female"]):
        return "Women"
    if any(word in text for word in ["kids","kid","child","children","junior","boy","boys","girl","girls"]):
        return "Kids"
    else:
        return  "Unisex"
    

# Loop through HTML files
for file in os.listdir("amazon_bestseller"):
    if file.endswith(".html"):
        try:
            with open(os.path.join("amazon_bestseller", file), "r", encoding="utf-8") as f:
                html_doc = f.read()

            soup = BeautifulSoup(html_doc, "html.parser")
            products = soup.find_all("div", class_="p13n-sc-uncoverable-faceout")

            for product in products:
                try:
                    # Title
                    t = product.find("div", class_="_cDEzb_p13n-sc-css-line-clamp-3_g3dy1")
                    title = t.get_text(strip=True) if t else None
                    
                    
                    # Price
                    p = product.find("span", class_="_cDEzb_p13n-sc-price_3mJ9Z")
                    price = p.get_text().strip() if p else "null"

                    # Rating
                    r = product.find("span", class_="a-icon-alt")
                    rating = r.get_text().strip() if r else "null"
                    
                     # Category from href
                    catg = re.search(r'ref=zg_bs_g_([^_]+)', link)
                    category = catg.group(1).replace('-', ' ').title() if catg else "null"
                    
                     # Gender
                    gender = gender_inter(title or link)
                    
                    # Link
                    a_tag = product.find("a", href=True)
                    link = a_tag['href'] if a_tag else "null"

                    # Image URL
                    img_tag = product.find("img")
                    img_url = img_tag['src'] if img_tag else "null"

                    # Timestamp
                    scrap_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Append to data
                    data_csv["title"].append(title)
                    data_csv["price"].append(price)
                    data_csv["category"].append(category)
                    data_csv["gender"].append(gender)
                    data_csv["rating"].append(rating)
                    data_csv["link"].append(link)
                    data_csv["image"].append("yes" if img_tag else "no")
                    data_csv["img_url"].append(img_url)
                    data_csv["scrap_time"].append(scrap_time)
                    

                except Exception as e:
                    print(f"Error processing product in {file}: {e}")

        except Exception as e:
            print(f"Error reading {file}: {e}")

# Convert to DataFrame
df = pd.DataFrame(data_csv)

# Clean price and rating
df['price'] = df['price'].str.replace(r'[^\d.]', '', regex=True).replace('', '0').astype(float)
df['rating'] = df['rating'].str.extract(r'([\d.]+)').fillna(0).astype(float)

# Add full Amazon link
df['full_link'] = "https://www.amazon.in" + df['link']

# Deduplicate and sort
df.drop_duplicates(subset='title', inplace=True)
df.sort_values(by='scrap_time', ascending=False, inplace=True)

# Save to CSV
df.to_csv(output_file, index=False)
print("✅ Scraping complete. Data saved to:", output_file)

