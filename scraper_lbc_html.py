import asyncio
from playwright.async_api import async_playwright

URL = (
    "https://www.leboncoin.fr/recherche"
    "?category=9"
    "&locations=Louverné_53950__48.12273_-0.72003_5000,"
    "L'Huisserie_53970__48.02281_-0.77001_5000,"
    "Saint-Berthevin_53940__48.06967_-0.83152_5000,"
    "Chang%C3%A9_53810__48.09901_-0.78975_5000,"
    "Laval_53000__48.07268_-0.77307_5000"
    "&price=min-320000"
    "&square=85-max"
    "&real_estate_type=1,3"
)

async def main():
    print("🚀 Lancement du scraper LeBonCoin via Playwright")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # ← headless=False pour éviter le blocage
        context = await browser.new_context()
        page = await context.new_page()

        print(f"🔎 Chargement de l'URL : {URL}")
        await page.goto(URL, timeout=60000)

        # Attendre que la page charge les annonces
        await page.wait_for_selector("a:has([data-qa-id='aditem_title'])", timeout=20000)

        # On scrolle pour charger plus d'annonces
        for _ in range(5):
            await page.mouse.wheel(0, 3000)
            await asyncio.sleep(1)

        annonces = await page.query_selector_all("a:has([data-qa-id='aditem_title'])")
        print(f"🔄 {len(annonces)} annonces récupérées")

        for annonce in annonces:
            titre_el = await annonce.query_selector("[data-qa-id='aditem_title']")
            prix_el = await annonce.query_selector("[data-qa-id='aditem_price']")
            titre = await titre_el.inner_text() if titre_el else "N/A"
            prix = await prix_el.inner_text() if prix_el else "N/A"
            print(f"🏠 {titre} - {prix}")

        await browser.close()

asyncio.run(main())
