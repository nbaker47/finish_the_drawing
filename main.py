from flask import Flask, jsonify, render_template, request, send_from_directory, redirect, url_for, g, Response
import nltk
from nltk.corpus import wordnet
from datetime import date, datetime, timedelta
import random
import base64
import sqlite3
from google.cloud import storage
from PIL import Image
import io
from io import BytesIO
import pytz


# Dictionary to store the vote scores for each image
image_votes = {}
app = Flask(__name__)
nltk.download('wordnet')
# Dictionary to store the vote count
vote_count = {"up": 0, "down": 0}

# serve manifest.json
@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory('static', 'manifest.json')

# serve service-worker.js
@app.route('/service-worker.js')
def serve_worker():
    return send_from_directory('static', 'service-worker.js')

# book selection page
@app.route('/')
def index():
    
    # Specify the time zone
    timezone = pytz.timezone('America/New_York')
    
    # Get the current time
    current_time = datetime.now(timezone)
    
    # Print the current time
    print("Current time:", current_time, 'timezone:', timezone)
    
    # Set a seed for consistent random noun each day
    current_date = current_time.date()
    
    # set seed
    seed = current_date.year * 10000 + current_date.month * 100 + current_date.day
    random.seed(seed)

    # Retrieve a random noun
    synsets = list(wordnet.all_synsets(wordnet.NOUN))
    random.shuffle(synsets)
    random_noun = synsets[0].lemmas()[0].name()

    # Clean up the noun
    random_noun = random_noun.replace("_", " ").title()

    print("Random Noun of the Day:", random_noun)

    return render_template('index.html', word=random_noun)

# Close the database connection at the end of each request
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# Create the database connection and cursor before each request
@app.before_request
def before_request():
    g.sqlite_db = sqlite3.connect('app.db')
    g.cursor = g.sqlite_db.cursor()


# Handle the /submit route
@app.route('/submit', methods=['POST'])
def submit():
    
    print('submitting image')
    
    # Get the image data from the POST request
    base64_image = request.form['image']
    
    print('read image')
    
    # Extract the encoded image data from the base64 string
    encoded_image = base64_image.split(',')[1]

    # Decode the base64 image data
    decoded_image = base64.b64decode(encoded_image)

    # Create a BytesIO object to work with the binary image data
    image_io = BytesIO(decoded_image)

    # Open the image from the BytesIO object
    image = Image.open(image_io)
    
    #----------------------
    
    image_io = BytesIO()
    
    image.save(image_io, format='PNG')
    
    # Reset the stream position to the beginning
    image_io.seek(0)

    # Set up GCS client
    storage_client = storage.Client()

    # Retrieve the bucket
    bucket = storage_client.bucket('drawoff-391919.appspot.com')

    # Generate a unique filename
    filename = f"image_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"

    # Upload the image data to the bucket
    blob = bucket.blob(filename)
    blob.upload_from_file(image_io, content_type='image/png')

    # Redirect to the /view route
    return redirect(url_for('view'))


# Handler for the route that deletes .png files
@app.route('/delete-png-files', methods=['POST'])
def delete_png_files():
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

    return 'Deletion of .png files completed'



# Handle the /view route
@app.route('/view')
def view():
    # Set up GCS client
    storage_client = storage.Client()

    # Retrieve the bucket
    bucket = storage_client.bucket('drawoff-391919.appspot.com')

    # List all blobs in the bucket
    blobs = bucket.list_blobs()

    # Get the image filenames from the blobs
    image_filenames = [blob.name for blob in blobs if blob.name.endswith('.png')]
    
    print(image_filenames)
    print('TRYING TO serving image')

    urls = []

    for image_filename in image_filenames:

        # Get the publicly accessible URL of the uploaded image
        blob = bucket.blob(image_filename)
        image_url = blob.public_url
        
        urls.append(image_url)

    return render_template('submissions.html', submissions=urls, vote_count=vote_count)



# entry point
if __name__ == '__main__':
    # Route to serve the favicon1.ico file
    # g.cursor.execute("DELETE FROM images")
    app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon1.ico'))
    app.run()
