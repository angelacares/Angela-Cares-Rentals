import json
import os

DB_FILE = 'listings.json'

def init_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, 'w') as f:
            json.dump([], f)

def save_listings(listings):
    with open(DB_FILE, 'w') as f:
        json.dump(listings, f)

def get_listings():
    with open(DB_FILE, 'r') as f:
        return json.load(f)
