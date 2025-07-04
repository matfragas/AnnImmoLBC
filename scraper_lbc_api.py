import requests

print("🚀 Lancement du scraper via l'API interne LeBonCoin")

# 🔍 Paramètres de recherche (exemple : achat maison dans Laval et alentours)
params = {
    "filters": {
        "category": {"id": "9"},
        "enums": {
            "real_estate_type": ["1", "3"]  # Maison ou appartement
        },
        "locations": [
            {"zipcode": "53000", "radius": 10000},
            {"zipcode": "53970", "radius": 10000},
            {"zipcode": "53810", "radius": 10000}
        ],
        "price": {"min": 320000},
        "square": {"max": 85}
    },
    "limit": 35,
    "offset": 0,
    "sort_by": "time",
    "sort_order": "desc"
}

headers = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/json"
}

# 💡 URL API du BonCoin
url = "https://api.leboncoin.fr/finder/search"

response = requests.post(url, json=params, headers=headers)

if response.status_code == 200:
    data = response.json()
    annonces = data.get("ads", [])
    print(f"🔄 {len(annonces)} annonces récupérées.")
    
    for a in annonces:
        print(f"\n🏠 {a.get('title')}")
        print(f"💰 Prix : {a.get('price')} €")
        print(f"📍 Ville : {a.get('location', {}).get('city')}")
        print(f"📅 Date : {a.get('index_date')}")
        print(f"🔗 Lien : {a.get('url')}")
else:
    print(f"❌ Erreur {response.status_code} lors de l'appel API.")
