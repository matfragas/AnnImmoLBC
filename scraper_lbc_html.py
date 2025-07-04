from playwright.async_api import async_playwright
import asyncio

async def main():
    print("🚀 Lancement du scraper LeBonCoin via Playwright")
    url = "https://www.leboncoin.fr/recherche?category=9&locations=Louvern%C3%A9_53950__48.12273_-0.72003_5000%2CL%27Huisserie_53970__48.02281_-0.77001_5000%2CSaint-Berthevin_53940__48.06967_-0.83152_5000%2CChang%C3%A9_53810__48.09901_-0.78975_5000%2CLaval_53000__48.07268_-0.77307_5000&price=min-320000&square=85-max&real_estate_type=1%2C3&page=1"  # ← ton URL complète ici
    print(f"🔎 Chargement de l'URL : {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # ✅ HEADLESS en CI
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
            viewport={"width": 1280, "height": 800},
            locale="fr-FR"
        )
        page = await context.new_page()
        await page.goto(url, timeout=60000)

        # ✅ Attendre un élément plus général
        await page.wait_for_selector("a[data-qa-id='aditem_container']", timeout=20000)

        # ✅ Extraire les annonces
        items = await page.locator("a[data-qa-id='aditem_container']").all()
        print(f"✅ {len(items)} annonces trouvées.")

        for i, item in enumerate(items):
            title = await item.locator("[data-qa-id='aditem_title']").inner_text()
            price = await item.locator("[data-qa-id='aditem_price']").inner_text()
            print(f"🏠 {i+1}. {title} - {price}")

        await browser.close()

asyncio.run(main())
