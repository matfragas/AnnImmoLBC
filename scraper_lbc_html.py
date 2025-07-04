import asyncio
from playwright.async_api import async_playwright

async def main():
    print("🚀 Lancement du scraper LeBonCoin via Playwright")

    url = (
        "https://www.leboncoin.fr/recherche"
        "?category=9"
        "&locations=Laval_53000__48.07268_-0.77307_5000"
        "&price=min-320000"
        "&square=85-max"
        "&real_estate_type=1,3"
    )

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()

        print(f"🔎 Chargement de l'URL : {url}")
        await page.goto(url, timeout=60000)

        # Attente du chargement des annonces
        await page.wait_for_selector("[data-qa-id='aditem_container']", timeout=15000)

        annonces = await page.query_selector_all("[data-qa-id='aditem_container']")
        print(f"✅ {len(annonces)} annonces récupérées.")

        for a in annonces:
            titre = await a.query_selector("[data-qa-id='aditem_title']")
            prix = await a.query_selector("[data-qa-id='aditem_price']")
            if titre and prix:
                titre_txt = await titre.inner_text()
                prix_txt = await prix.inner_text()
                print(f"🏠 {titre_txt} - {prix_txt}")

        await browser.close()

asyncio.run(main())
