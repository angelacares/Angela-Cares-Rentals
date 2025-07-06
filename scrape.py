# scrape.py
import requests
from bs4 import BeautifulSoup
from db import init_db, save_listings

URL = 'https://www.realestate.com.au/rent/in-zetland,+nsw+2017/list-1'

def scrape():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    cards = soup.select('[data-testid="listing-card"]')

    listings = []

    for card in cards:
        try:
            a_tag = card.find('a', href=True)
            if not a_tag:
                continue

            link = 'https://www.realestate.com.au' + a_tag['href']
            listing_id = link.split('/')[-1].split('?')[0]

            title_tag = card.find('h2')
            title = title_tag.text.strip() if title_tag else 'No title'

            address_tag = card.find('span', {'data-testid': 'address'})
            address = address_tag.text.strip() if address_tag else 'No address'

            price_tag = card.find('span', {'data-testid': 'listing-card-price'})
            price = price_tag.text.strip() if price_tag else 'No price'

            img_tag = card.find('img')
            image = img_tag['src'] if img_tag and img_tag.has_attr('src') else ''

            listings.append({
                'id': listing_id,
                'title': title,
                'address': address,
                'price': price,
                'link': link,
                'image': image
            })
        except Exception as e:
            print(f"Error parsing card: {e}")
            continue

    save_listings(listings)

if __name__ == '__main__':
    init_db()
    scrape()
