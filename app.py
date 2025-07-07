from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

LISTINGS_FILE = "listings.json"

@app.route('/')
def index():
    with open(LISTINGS_FILE, 'r') as f:
        listings = json.load(f)
    return render_template('index.html', listings=listings)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # Get form data
        new_listing = {
            "title": request.form["title"],
            "address": request.form["address"],
            "price": request.form["price"],
            "link": request.form["link"],
            "image": request.form["image"]
        }

        # Save to JSON file
        if os.path.exists(LISTINGS_FILE):
            with open(LISTINGS_FILE, 'r') as f:
                listings = json.load(f)
        else:
            listings = []

        listings.insert(0, new_listing)  # Add newest first

        with open(LISTINGS_FILE, 'w') as f:
            json.dump(listings, f, indent=2)

        return redirect(url_for('index'))

    return render_template('admin.html')

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
