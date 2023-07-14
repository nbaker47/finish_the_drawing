from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from user import User
import bcrypt
import user_db
from main import app, login_manager
from images import upload_image_to_bucket
from drawing_db import select_where_user


@login_manager.user_loader
def load_user(username):
    return User.get(username)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('select'))

# login
@app.route('/login')
def login():
    
    wrong_pass = request.args.get('wrong_pass')
    print(wrong_pass)

    return render_template('login.html', wrong_pass = wrong_pass)


@app.route('/verify-user', methods=['POST'])
def verify_user():
    username = request.form.get('username')
    password = request.form.get('password')

    stored_password = user_db.get_password_from_database(username)

    if stored_password is None or not bcrypt.checkpw(password.encode('utf-8'), stored_password[0].encode('utf-8')):
        # Invalid username or password
        return redirect(url_for("login", wrong_pass=True))

    # Password is correct
    # Retrieve the user ID from the database

    # Load the user object using the user ID
    user = User(username, None)
    
    print('LOGGING IN USER', user.get_id())
    
    # Log in the user
    login_user(user, remember=True)  # Set remember=True to remember the user across sessions
    
    # Check if the user is logged in
    if current_user.is_authenticated:
        print("User is logged in")
    else:
        print("User is not logged in")

    return redirect(url_for("index"))


# register
@app.route('/register')
def register():

    username_exists = request.args.get('username_exists')
    print(username_exists)

    return render_template('register.html', username_exists = username_exists)


# create user
@app.route('/create-user', methods=['POST'])
def create_user():
    
    # Extract data from form
    username = request.form.get('username')
    password = request.form.get('password')
    drawing_data = request.form.get('drawingData')
    
    # Upload image to bucket
    image_url, filename = upload_image_to_bucket(drawing_data, username=username)
    
    # hash pass
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # create user
    success = user_db.create_user(username, hashed_password, image_url)

    # validate
    if success:
        # Load the user object using the user ID
        user = User(username, image_url)

        # Log in the user
        login_user(user, remember=True)  # Set remember=True to remember the user across sessions

        response = redirect(url_for("index"))
    else:
        response = redirect(url_for("register", username_exists=True))

    return response

# select
@app.route('/select')
def select():
    # Check if the user is logged in
    if current_user.is_authenticated:
        print("User is logged in")
        
        images = select_where_user(current_user.get_id())
        
        return render_template('profile.html', images=images)
    else:
        print("User is not logged in")
        return render_template('select.html')
    
# select
@app.route('/view-profile', methods=['POST'])
def view_profile():
    # Check if the user is logged in
    
    username = request.form.get('username')
    
    user = user_db.get_user(username)
        
    images = select_where_user(username)
    
    return render_template('view-profile.html', images=images, view_user=user)

    
@app.route('/redraw')
def redraw():
    return render_template('redraw.html')


@app.route('/update-profile-pic', methods=['POST'])
def update_profile_pic():
    
    try:
    
        drawing_data = request.form.get('drawingData')
        
        username = current_user.get_id()
        
        image_url, filename = upload_image_to_bucket(drawing_data, username=username)
        
        user_db.update_profile_pic(current_user.get_id(), image_url)
    
    except:
        print('ERROR UPDATING PROFILE PIC')
    
    return render_template('profile.html')


@app.route('/delete-user', methods=['POST'])
def delete_user():
    
    try:
        
        username = request.form.get('username')
        
        
        print('UPDATING PROFILE PIC', username)
    
        
        image_url = 'https://storage.googleapis.com/drawoff-391919.appspot.com/profilepic_nathan.png'
        
        user_db.update_profile_pic(username, image_url)
    
    except:
        print('ERROR UPDATING PROFILE PIC')
    
    return redirect(url_for('view'))