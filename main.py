import requests
from flask import Flask, jsonify, render_template, request, send_from_directory, redirect, url_for, session
import nltk
from nltk.corpus import wordnet
from datetime import date, datetime, timedelta
import random
import os
import base64
from apscheduler.schedulers.background import BackgroundScheduler

image_data_dict = {}

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

    # Set a seed for consistent random noun each day
    today = date.today()
    seed = today.year * 10000 + today.month * 100 + today.day
    random.seed(seed)
    
    # Retrieve a random noun
    synsets = list(wordnet.all_synsets(wordnet.NOUN))
    random.shuffle(synsets)
    random_noun = synsets[0].lemmas()[0].name()
    
    # Clean up the noun
    random_noun = random_noun.replace("_", " ").title()

    print("Random Noun of the Day:", random_noun)

    return render_template('index.html', word=random_noun)

# Handle the /submit route
@app.route('/submit', methods=['POST'])
def submit():
    # Get the image data from the POST request
    image_data = request.form['image']

    # Create a unique identifier for the image
    image_id = str(random.randint(1, 1000000))

    # Store the image data in a dictionary with the image ID as the key
    image_data_dict[image_id] = image_data

    # Redirect to the /view route with the image ID as a query parameter
    return redirect(url_for('view', image_id=image_id))



# Handle the /view route
@app.route('/view')
def view():
    # Get the image IDs from the query parameters
    image_ids = request.args.getlist('image_id')

    # Retrieve the image data for each image ID
    submissions = []
    for image_id in image_ids:
        image_data = image_data_dict.get(image_id)
        if image_data:
            vote_score = image_votes.get(image_id, 0)
            submissions.append({'image': image_data, 'score': vote_score})

    return render_template('submissions.html', submissions=submissions, vote_count=vote_count)



@app.route('/vote', methods=['POST'])
def handle_vote():
    # Get the vote and image data from the request body
    vote_data = request.get_json()
    vote = vote_data.get('vote')
    image = vote_data.get('image')

    # Process the vote and image data as needed
    if vote == 'up':
        vote_count['up'] += 1
    elif vote == 'down':
        vote_count['down'] += 1

    # Update the vote score for the image
    if image in image_votes:
        image_votes[image] += 1 if vote == 'up' else -1
    else:
        image_votes[image] = 1 if vote == 'up' else -1

    # Retrieve the updated vote score for the image
    vote_score = image_votes.get(image, 0)

    print(image, vote_score)
    print(image_votes)

    # Return the updated vote score for the image
    return jsonify({'vote': vote, 'score': vote_score}), 200




# Function to delete images in /static/media/submissions directory
def delete_images():
    submissions_dir = 'static/media/submissions'
    for filename in os.listdir(submissions_dir):
        if filename.endswith('.png') or filename.endswith('.jpg') or filename.endswith('.jpeg'):
            image_path = os.path.join(submissions_dir, filename)
            os.remove(image_path)
    print('Deleted all images in /static/media/submissions directory.')

# Schedule the delete_images function to run once a day
def schedule_image_deletion():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_images, 'interval', days=1, start_date=datetime.now() + timedelta(days=1))
    scheduler.start()
    


@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon1.ico', mimetype='image/vnd.microsoft.icon')
# entry point
if __name__ == '__main__':
    schedule_image_deletion()
    # Route to serve the favicon1.ico file
    app.add_url_rule('/favicon.ico',redirect_to=url_for('static', filename='favicon.ico'))
    app.run(debug=False)
