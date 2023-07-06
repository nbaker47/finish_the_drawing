from flask import Flask, jsonify, render_template, request, send_from_directory, redirect, url_for, g
import nltk
from nltk.corpus import wordnet
from datetime import date, datetime, timedelta
import random
import base64
import sqlite3

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
    # Get the image data from the POST request
    image_data = request.form['image']

    # Store the image data in the database
    g.cursor.execute('INSERT INTO images (image_data) VALUES (?)', (image_data,))
    g.sqlite_db.commit()

    # Get the last inserted row id
    image_id = g.cursor.lastrowid

    # Redirect to the /view route
    return redirect(url_for('view'))

# Handle the /view route
@app.route('/view')
def view():
    # Retrieve all image data from the database
    g.cursor.execute('SELECT image_data FROM images')
    image_data_rows = g.cursor.fetchall()

    # Extract image data from the rows
    image_datas = [row[0] for row in image_data_rows]
    
    print("Image Data:", image_datas)

    return render_template('submissions.html', submissions=image_datas, vote_count=vote_count)

# entry point
if __name__ == '__main__':
    # Route to serve the favicon1.ico file
    app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='favicon.ico'))
    app.run(debug=False)
