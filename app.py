from flask import Flask, jsonify, render_template
import sqlite3
from db import init_db

app = Flask(__name__)
DB = 'listings.db'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/listings')
def api_listings():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT title, address, price, link, image FROM listings ORDER BY timestamp DESC")
    rows = c.fetchall()
    conn.close()
    return jsonify([
        {'title': r[0], 'address': r[1], 'price': r[2], 'link': r[3], 'image': r[4]}
        for r in rows
    ])

@app.route('/run-scraper')
def run_scraper():
    from scrape import scrape
    scrape()
    return 'Scraper ran successfully.'

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
