import requests
from bs4 import BeautifulSoup

def scrape_domain():
    url = "https://www.domain.com.au/rent/zetland-nsw-2017/"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    listings = []

    cards = soup.select('li[data-testid="listing-card"]')
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
            print(f"⚠️ Failed to parse a card: {e}")
    return listings
