
from main import app
from flask import request, redirect, url_for, render_template, make_response
import drawing_db
from app_services import *
from flask_login import current_user
from user_db import get_profile_pic


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
    drawing_db.vote(id)
    
    return response

# Handle the /submit route
@app.route('/submit', methods=['POST'])
def submit():
    
    # Get the image data from the POST request
    base64_image = request.form['image']
    
    # Upload image to bucket
    image_url, filename = upload_image_to_bucket(base64_image)
    
    # Then, create a new entry in the images table 
    id = filename[:-4]
    votes = 0
    message = request.form['comment']

    # Get the daily word and seed
    random_word, seed = get_daily_word_and_seed()
    
    # see who drew it
    if current_user.is_authenticated:
        print("User is logged in")
        user = current_user.get_id()
    else:
        print("User is not logged in")
        user = 'Guest Drawer'        

    drawing_db.create_entry(id, image_url, votes, message, random_word, user)
    
    response = redirect(url_for("view"))
    response.set_cookie('voted_image', '0')
    
    return response


# Handle the /view route
@app.route('/view')
def view():
    
    random_word, seed = get_daily_word_and_seed()
    
    print('viewing images with word: ', random_word)
    
    # Retrieve all image data from the database
    submissions = drawing_db.select_all(random_word)
    
    # Sort the submissions by vote
    submissions_sorted = sorted(submissions, key=lambda x: x[2], reverse=True)
    
    context = {
        'submissions': submissions_sorted,
        'get_profile_pic': get_profile_pic
    }

    return render_template('submissions.html', **context)