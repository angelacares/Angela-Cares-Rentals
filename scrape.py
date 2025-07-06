import requests
from bs4 import BeautifulSoup
from db import init_db, save_listings

URL = 'https://www.realestate.com.au/rent/in-zetland,+nsw+2017/list-1'

def scrape():
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    cards = soup.select('[data-testid="listing-card"]')

    listings = []
    for card in cards:
        try:
            link = 'https://www.realestate.com.au' + card.find('a')['href']
            listing_id = link.split('/')[-1]
            title = card.find('h2').text.strip()
            address = card.find('span', {'data-testid': 'address'}).text.strip()
            price = card.find('span', {'data-testid': 'listing-card-price'}).text.strip()
            img = card.find('img')
            image = img['src'] if img else ''
            listings.append({
                'id': listing_id,
                'title': title,
                'address': address,
                'price': price,
                'link': link,
                'image': image
            })
        except Exception:
            continue

    save_listings(listings)

if __name__ == '__main__':
    init_db()
    scrape()
