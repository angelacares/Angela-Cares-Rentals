from flask import Flask, render_template
import json
import os

app = Flask(__name__)

def load_listings():
    try:
        with open("listings.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("❌ Failed to load listings:", e)
        return []

@app.route("/")
def home():
    listings = load_listings()
    print(f"🟢 Rendering {len(listings)} listings")
    return render_template("index.html", listings=listings)

# Required for Render.com
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
