import os
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from tinydb import TinyDB, Query
import boto3
from botocore.exceptions import NoCredentialsError
from datetime import datetime

# --- Flask Setup ---
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = TinyDB('db.json')

def load_listings():
    return db.all()

def save_listing(data):
    db.insert(data)

# --- AWS S3 Setup ---
AWS_ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('AWS_SECRET_KEY')
S3_BUCKET_NAME = "angela-cares-videos"

s3 = boto3.client('s3',
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY
)

def upload_to_s3(file_obj, filename):
    try:
        s3.upload_fileobj(
            file_obj, S3_BUCKET_NAME, filename,
            ExtraArgs={'ACL': 'public-read', 'ContentType': 'video/mp4'}
        )
        return f"https://{S3_BUCKET_NAME}.s3.amazonaws.com/{filename}"
    except NoCredentialsError:
        print("Credentials not available")
        return ""

# --- Routes ---
@app.route('/')
def index():
    listings = load_listings()
    return render_template('index.html', listings=listings)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        link = request.form.get('link')

        image = request.files.get('image')
        image_path = None
        if image and image.filename:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = url_for('static', filename=f'images/{filename}')

        video = request.files.get('video')
        video_url = None
        if video and video.filename:
            filename = datetime.utcnow().strftime('%Y%m%d%H%M%S_') + secure_filename(video.filename)
            video_url = upload_to_s3(video, filename)

        listing = {
            "title": title,
            "description": description,
            "link": link,
            "image": image_path,
            "video": video_url
        }
        save_listing(listing)
        return redirect(url_for('index'))
    return render_template('admin.html')

if __name__ == '__main__':
    app.run(debug=True)
