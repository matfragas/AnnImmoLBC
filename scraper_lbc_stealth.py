import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time

URL = "https://www.leboncoin.fr/recherche?category=9&locations=Louverné_53950__48.12273_-0.72003_5000,L&#x27;Huisserie_53970__48.02281_-0.77001_5000,Saint-Berthevin_53940__48.06967_-0.83152_5000,Chang%C3%A9_53810__48.09901_-0.78975_5000,Laval_53000__48.07268_-0.77307_5000&price=min-320000&square=85-max&real_estate_type=1,3&page=1"

options = uc.ChromeOptions()
options.headless = True
driver = uc.Chrome(options=options)

print("🚀 Ouverture du navigateur...")
driver.get(URL)
time.sleep(5)  # attendre le JS

print("✅ Page chargée. Extraction du HTML...")
soup = BeautifulSoup(driver.page_source, "html.parser")

ads = soup.select("a[data-qa-id='aditem_container']")
print(f"🔍 {len(ads)} annonces détectées")

for i, ad in enumerate(ads, start=1):
    title = ad.select_one("[data-qa-id='aditem_title']")
    price = ad.select_one("[data-qa-id='aditem_price']")
    location = ad.select_one("[data-qa-id='aditem_location']")
    print(f"🏠 {i}. {title.text.strip() if title else ''} | {price.text.strip() if price else ''} | {location.text.strip() if location else ''}")

driver.quit()
