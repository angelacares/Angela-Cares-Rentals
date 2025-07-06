from flask import Flask, render_template
import json

app = Flask(__name__)

def load_listings():
    try:
        with open('listings.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

@app.route("/")
def home():
    listings = load_listings()
    return render_template("index.html", listings=listings)

if __name__ == "__main__":
    app.run(debug=True)
