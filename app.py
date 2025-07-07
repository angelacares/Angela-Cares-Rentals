from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import json
import os

<!DOCTYPE html>
<html>
<head>
  <title>Angela Cares Rentals</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background: #f4fff6;
      padding: 2rem;
      margin: 0;
    }
    header {
      display: flex;
      align-items: center;
      padding: 1rem;
      background-color: #dff5e3;
      border-bottom: 2px solid #a0d6a0;
    }
    header img {
      height: 60px;
      margin-right: 15px;
    }
    header h1 {
      font-size: 1.8rem;
      color: #2e7d32;
      margin: 0;
    }
    .listing {
      border: 1px solid #ccc;
      background: white;
      padding: 1rem;
      border-radius: 12px;
      margin: 1rem 0;
      box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    img.property {
      width: 100%;
      height: auto;
      border-radius: 8px;
      margin-top: 10px;
    }
    video {
      width: 100%;
      border-radius: 8px;
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <header>
    <img src="/static/logo.png" alt="Logo">
    <h1>Angela Cares Rentals</h1>
  </header>

  <div class="content">
    {% for listing in listings %}
      <div class="listing">
        <h2>{{ listing.title }}</h2>
        <p><strong>Address:</strong> {{ listing.address }}</p>
        <p><strong>Price:</strong> {{ listing.price }}</p>
        <a href="{{ listing.link }}" target="_blank">View Listing</a>

        {% if listing.image %}
          <img class="property" src="{{ listing.image }}" alt="Property image">
        {% endif %}

        {% if listing.video %}
          <video controls>
            <source src="{{ listing.video }}" type="video/mp4">
            Your browser does not support the video tag.
          </video>
        {% endif %}
      </div>
    {% endfor %}
  </div>
</body>
</html>




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
