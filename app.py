from flask import Flask, jsonify, request
from scraper import scrape_domain
from db import init_db, save_listings, get_listings

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Angela Cares Rentals 🏡</h1><ul>' + ''.join([
        f'<li><a href="{l["link"]}" target="_blank">{l["address"]} – {l["price"]}</a></li>'
        for l in get_listings()
    ]) + '</ul>'

@app.route('/api/listings')
def api_listings():
    return jsonify(get_listings())

@app.route('/run-scraper')
def run_scraper():
    listings = scrape_domain()
    if listings:
        save_listings(listings)
        return 'Scraper ran successfully.'
    return 'Scraper failed.'

@app.route('/upload', methods=['POST'])
def upload_listings():
    data = request.get_json()
    if not data or not isinstance(data, list):
        return 'Invalid data', 400
    save_listings(data)
    return 'Listings uploaded successfully.', 200

@app.route('/debug')
def debug_file():
    try:
        with open("debug.html", "r", encoding="utf-8") as f:
            return f.read(), 200, {'Content-Type': 'text/html'}
    except FileNotFoundError:
        return "debug.html not found", 404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
