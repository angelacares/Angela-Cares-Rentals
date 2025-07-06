import sqlite3
import time

DB = 'listings.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS listings (
                    id TEXT PRIMARY KEY,
                    title TEXT,
                    address TEXT,
                    price TEXT,
                    link TEXT,
                    image TEXT,
                    timestamp INTEGER
                )''')
    conn.commit()
    conn.close()

def save_listings(listings):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    new_ids = set()

    for l in listings:
        c.execute("REPLACE INTO listings VALUES (?, ?, ?, ?, ?, ?, ?)", (
            l['id'], l['title'], l['address'], l['price'], l['link'], l['image'], int(time.time())
        ))
        new_ids.add(l['id'])

    c.execute("SELECT id FROM listings")
    all_ids = {row[0] for row in c.fetchall()}
    removed = all_ids - new_ids
    for rid in removed:
        c.execute("DELETE FROM listings WHERE id = ?", (rid,))

    conn.commit()
    conn.close()
