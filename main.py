from flask import Flask, jsonify, render_template, request, send_from_directory, redirect, url_for, g, Response, make_response, session
from datetime import datetime
import random
from google.cloud import storage
import pytz
import bcrypt
from flask_login import LoginManager

# import interface with drawing_data
import drawing_db
# import app services
from app_services import *

''' ---------------------------- PREAMBLE ---------------------------- '''

# Specify the time zone
timezone = pytz.timezone('America/New_York')

# Set up Flask app
app = Flask(__name__)
app.secret_key = 'drawoff'

# Login Manager
login_manager = LoginManager(app)
login_manager.init_app(app)

# Import login.py routes
from login import *
# import images.py routes
from images import *

''' ---------------------------- SERVICES ---------------------------- '''

# Handler for the route that deletes .png files
@app.route('/wipe', methods=['POST'])
def wipe():
    # Set up GCS client
    storage_client = storage.Client()
    bucket_name = 'drawoff-391919.appspot.com'

    # Retrieve the bucket
    bucket = storage_client.bucket(bucket_name)

    # List all blobs in the bucket
    blobs = bucket.list_blobs()

    # Iterate through the blobs and delete .png files
    for blob in blobs:
        if blob.name.endswith('.png'):
            blob.delete()
            
    # Wipe DB
    drawing_db.wipe_table()

    return 'Deletion of .png files completed'

# serve favicon.ico
@app.route('/favicon.ico')
def serve_favicon():
    return send_from_directory('static', 'media/favicon.ico')

# serve manifest.json
@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory(app.root_path, 'manifest.json')

# serve assetlinks.json
@app.route('/.well-known/assetlinks.json')
def serve_assetlinks():
    return send_from_directory(app.root_path, 'assetlinks.json')

# serve service-worker.js
@app.route('/service-worker.js')
def serve_worker():
    return send_from_directory(app.root_path, 'service-worker.js')

# Handle the /privacy route
@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

# Inject user data into all templates
@app.context_processor
def inject_user():
    # Get the current logged-in user (assuming you have implemented Flask-Login)
    user = current_user if current_user.is_authenticated else None

    # Return the variables you want to make available to all templates
    return dict(user=user)

# Show user his session cookies route
@app.route('/print_session_cookie')
def print_session_cookie():
    voted_image_cookie = request.cookies.get('voted_image')
    voted_image_ids = voted_image_cookie.split(',') if voted_image_cookie else []
    for voted_image_id in voted_image_ids:
        print(voted_image_id)
    return 'Voted image IDs printed in the console.'


''' ---------------------------- INDEX ---------------------------- '''

# index router
@app.route('/index')
def index():
    
    # Get the daily word and seed
    random_word, seed = get_daily_word_and_seed()

    return render_template('index.html', word=random_word, seed=seed)


@app.route('/')
def select_or_index():
    
    # Get the daily word and seed
    random_word, seed = get_daily_word_and_seed()
    
    # Check if the user is logged in
    if current_user.is_authenticated:
        return render_template('index.html', word=random_word, seed=seed)
    else:
        return redirect(url_for('select'))

    

''' ---------------------------- Entry ---------------------------- '''

# entry point
if __name__ == '__main__':
    
    app.run()
