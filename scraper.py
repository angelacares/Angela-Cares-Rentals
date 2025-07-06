import requests
from bs4 import BeautifulSoup

def scrape_domain():
    url = "https://www.domain.com.au/rent/zetland-nsw-2017/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        print(f"🌐 Fetching {url}")
        response = requests.get(url, headers=headers)
        print(f"🔁 Response status code: {response.status_code}")

        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        # Debug output
        print("🔍 Writing debug.html to inspect HTML content")
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(soup.prettify())

        cards = soup.select('li[data-testid="listing-card"]')
        print(f"✅ Found {len(cards)} listings on domain.com.au")

        listings = []
        for card in cards:
            try:
                link_tag = card.select_one('a[href]')
                link = link_tag['href']
                if not link.startswith('http'):
                    link = 'https://www.domain.com.au' + link

                address = card.select_one('[data-testid="address-label"]').get_text(strip=True)
                price_tag = card.select_one('[data-testid="listing-price"]')
                price = price_tag.get_text(strip=True) if price_tag else 'N/A'
                title = card.select_one('h2').get_text(strip=True)
                image_tag = card.select_one('img')
                image = image_tag['src'] if image_tag else ''

                listings.append({
                    'id': link.split('/')[-2],
                    'title': title,
                    'address': address,
                    'price': price,
                    'link': link,
                    'image': image
                })
            except Exception as e:
                print(f"⚠️ Error parsing card: {e}")
        return listings

    except Exception as e:
        print(f"❌ Exception in scrape_domain: {e}")
        return []
