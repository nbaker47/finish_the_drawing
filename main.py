from flask import Flask, jsonify, render_template, request, send_from_directory, redirect, url_for, g, Response, make_response, session
import nltk
from nltk.corpus import wordnet
from datetime import date, datetime, timedelta
import random
import base64
from google.cloud import storage
from PIL import Image
from io import BytesIO
import pytz
import db_config

''' ---------------------------- PREAMBLE ---------------------------- '''

# Download NLTK data for NOUNS
nltk.download('wordnet')

# Specify the time zone
timezone = pytz.timezone('America/New_York')

# Get the current date and time
today = datetime.now(timezone)
# Get the current date
today = today.date()
# Get tomorrow's date
tomorrow = today + timedelta(days=1)
print("Tomorrow's date:", tomorrow)

# Set up Flask app
app = Flask(__name__)

''' ---------------------------- API SERVICES ---------------------------- '''

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
    db_config.wipe_table()

    return 'Deletion of .png files completed'

# serve favicon.ico
@app.route('/favicon.ico')
def serve_favicon():
    return send_from_directory('static', 'media/favicon.ico')

# serve manifest.json
@app.route('/manifest.json')
def serve_manifest():
    return send_from_directory(app.root_path, 'manifest.json')

# serve service-worker.js
@app.route('/service-worker.js')
def serve_worker():
    return send_from_directory(app.root_path, 'service-worker.js')

''' ---------------------------- INDEX ---------------------------- '''

# book selection page
@app.route('/')
def index():
    
    # RETRIEVE DAILY NOUN ------------
    
    # Get the current time
    current_time = datetime.now(timezone)

    # Print the current time
    print("Current time:", current_time, 'timezone:', timezone)

    # Set a seed for consistent random noun each day
    current_date = current_time.date()
    
    # get tomorrow
    global tomorrow
    print("Todays's date:", current_date)
    print("Tomorrow's date:", tomorrow)
    
    # Compare if the current time has reached tomorrow
    if current_date >= tomorrow:
        # The current time has reached tomorrow
        print("tomorrow has arrived, wiping files and DB")
        wipe()
        tomorrow = current_date + timedelta(days=1)
        
    
    # set seed for today
    seed = current_date.year * 10000 + current_date.month * 100 + current_date.day
    random.seed(seed)

    # Retrieve a random noun
    synsets = list(wordnet.all_synsets(wordnet.NOUN))
    random.shuffle(synsets)
    random_noun = synsets[0].lemmas()[0].name()

    # Clean up the noun
    random_noun = random_noun.replace("_", " ").title()
    
    print("Random Noun of the Day:", random_noun)
    

    return render_template('index.html', word=random_noun, seed=seed)


''' ---------------------------- SUBMIT, VOTE AND VIEW ROUTES ---------------------------- '''

# Handle the /submit route
@app.route('/submit', methods=['POST'])
def submit():
    print('submitting image')

    # First, upload image to bucket ----------------------------------------------
    
    # Get the image data from the POST request
    base64_image = request.form['image']

    # Extract the encoded image data from the base64 string
    encoded_image = base64_image.split(',')[1]

    # Decode the base64 image data
    decoded_image = base64.b64decode(encoded_image)

    # Create a BytesIO object to work with the binary image data
    image_io = BytesIO(decoded_image)

    # Open the image from the BytesIO object
    image = Image.open(image_io)

    # Save the image as PNG to the BytesIO object
    image_io = BytesIO()
    image.save(image_io, format='PNG')
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
    image_url = blob.public_url
    
    # Then, create a new entry in the images table --------------------------------------------
    id = filename[:-4]
    votes = 0
    message = request.form['comment']
    db_config.create_entry(id, image_url, votes, message)

    # Redirect to the /view route
    return redirect(url_for('view'))


@app.route('/vote', methods=['POST'])
def vote():
    # Get the data from the POST request
    id = request.form['id']

    # Retrieve the existing voted_image_ids from the cookie
    voted_image_cookie = request.cookies.get('voted_image')
    voted_image_ids = []
    
    if voted_image_cookie:
        # If the cookie exists, split the values into a list
        voted_image_ids = voted_image_cookie.split(',')
    
    if id not in voted_image_ids:
        # Append the new voted image ID to the list if it's not already present
        voted_image_ids.append(id)
    
    # Convert the list back to a comma-separated string
    voted_image_cookie = ','.join(voted_image_ids)
    
    # Save the updated voted image IDs in the cookie
    response = make_response(redirect(url_for('view')))
    response.set_cookie('voted_image', voted_image_cookie)
    
    # actually update the DB with vote
    db_config.vote(id)
    
    return response

@app.route('/print_session_cookie')
def print_session_cookie():
    voted_image_cookie = request.cookies.get('voted_image')
    voted_image_ids = voted_image_cookie.split(',') if voted_image_cookie else []
    for voted_image_id in voted_image_ids:
        print(voted_image_id)
    return 'Voted image IDs printed in the console.'


# Handle the /view route
@app.route('/view')
def view():
    
    # Retrieve all image data from the database
    submissions = db_config.select_all()
    
    # Sort the submissions by vote
    submissions_sorted = sorted(submissions, key=lambda x: x[2], reverse=True)
    
    print(submissions_sorted)

    return render_template('submissions.html', submissions=submissions_sorted)



''' ---------------------------- Entry ---------------------------- '''

# entry point
if __name__ == '__main__':
    
    # Create DB if doesnt exist
    db_config.create_table()
    
    app.run()
