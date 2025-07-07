from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import os

app = Flask(__name__)

LISTINGS_FILE = "listings.json"
UPLOAD_FOLDER = os.path.join("static", "videos")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    with open(LISTINGS_FILE, 'r') as f:
        listings = json.load(f)
    return render_template('index.html', listings=listings)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        video_file = request.files.get("video_file")
        video_path = ""

        if video_file and video_file.filename != "":
            filename = secure_filename(video_file.filename)
            video_path = f"/static/videos/{filename}"
            video_file.save(os.path.join(UPLOAD_FOLDER, filename))

        new_listing = {
            "title": request.form["title"],
            "address": request.form["address"],
            "price": request.form["price"],
            "link": request.form["link"],
            "image": request.form["image"],
            "video": video_path
        }

        if os.path.exists(LISTINGS_FILE):
            with open(LISTINGS_FILE, 'r') as f:
                listings = json.load(f)
        else:
            listings = []

        listings.insert(0, new_listing)

        with open(LISTINGS_FILE, 'w') as f:
            json.dump(listings, f, indent=2)

        return redirect(url_for('index'))

    return render_template('admin.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
