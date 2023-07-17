
from main import app
from flask import request, redirect, url_for, render_template, make_response
from service_drawing import drawing_db
from app_services import *
from flask_login import current_user
from service_profile.user_db import get_profile_pic, is_admin
from service_drawing.drawing_db import delete_row_by_id


@app.route('/vote', methods=['POST'])
def vote():
    # Get the data from the POST request
    id = request.form['id']
    vote = int(request.form['vote'])  # Convert vote to an integer

    # Retrieve the existing voted_image_ids from the cookie
    voted_image_cookie = request.cookies.get('voted_image')
    voted_image_ids = []

    # Retrieve the existing downvoted_image_ids from the cookie
    downvoted_image_cookie = request.cookies.get('downvoted_image')
    downvoted_image_ids = []

    if voted_image_cookie:
        # If the voted_image cookie exists, split the values into a list
        voted_image_ids = voted_image_cookie.split(',')

    if downvoted_image_cookie:
        # If the downvoted_image cookie exists, split the values into a list
        downvoted_image_ids = downvoted_image_cookie.split(',')

    if vote == 1:
        if id not in voted_image_ids:
            # Append the new voted image ID to the list if it's not already present
            voted_image_ids.append(id)
        if id in downvoted_image_ids:
            # Remove the downvoted image ID from the list if it's present
            downvoted_image_ids.remove(id)
    elif vote == -1:
        if id not in downvoted_image_ids:
            # Append the new downvoted image ID to the list if it's not already present
            downvoted_image_ids.append(id)
        if id in voted_image_ids:
            # Remove the voted image ID from the list if it's present
            voted_image_ids.remove(id)

    # Convert the lists back to comma-separated strings
    voted_image_cookie = ','.join(voted_image_ids)
    downvoted_image_cookie = ','.join(downvoted_image_ids)

    # Save the updated voted image IDs and downvoted image IDs in the cookies
    response = make_response(redirect(url_for('view')))
    response.set_cookie('voted_image', voted_image_cookie)
    response.set_cookie('downvoted_image', downvoted_image_cookie)

    # Actually update the DB with the vote
    drawing_db.vote(id, vote)

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

    # See who drew it
    if current_user.is_authenticated:
        print("User is logged in")
        user = current_user.get_id()
    else:
        print("User is not logged in")
        user = 'Guest Drawer'

    drawing_db.create_entry(id, image_url, votes, message, random_word, user)

    response = redirect(url_for("view"))
    response.set_cookie('submitted_image', '1')

    return response



@app.route('/view')
def view():
    random_word, seed = get_daily_word_and_seed()
    
    print('viewing images with word:', random_word)
    
    # Retrieve all image data from the database
    submissions = drawing_db.select_all(random_word)
    
    # Sort the submissions by vote
    submissions_sorted = sorted(submissions, key=lambda x: x[2], reverse=True)
    
    context = {
        'submissions': submissions_sorted,
        'get_profile_pic': get_profile_pic,
        'is_admin' : is_admin
    }

    response = make_response(render_template('service_drawing/submissions.html', **context))

    return response



# Handle the /view route
@app.route('/view-single-card/')
def view_single_card():
    
    id = request.args.get('id')
    
    # Retrieve all image data from the database
    submission = drawing_db.select_where_id(id)[0]
    
    print('viewing single card: ', submission)
    
    context = {
        'submission': submission,
        'get_profile_pic': get_profile_pic,
        'is_admin' : is_admin,
        'word' : submission[4],
    }

    return render_template('service_drawing/single-card.html', **context)


# Handle the /submit route
@app.route('/delete-submission', methods=['POST'])
def delete_submission():
    
    # Get the image data from the POST request
    image_id = request.form['id']
    
    # Set up GCS client
    storage_client = storage.Client()

    # Retrieve the bucket
    bucket = storage_client.bucket('drawoff-391919.appspot.com')

    # delete from bucket
    existing_blob = bucket.blob(image_id+'.png')
    if existing_blob.exists():
        print("File already exists, deleting...")
        existing_blob.delete()
        
    # delete from DB
    delete_row_by_id(image_id)
    
    # Redirect to the same page they were on
    return redirect(request.referrer)