from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from service_profile.user import User
import bcrypt
from service_profile import user_db
from main import app, login_manager
from service_drawing.images import upload_image_to_bucket
from service_drawing.drawing_db import select_where_user

# Handle the /partymode-index route
@app.route('/partymode-index')
def partymode_index():
    return render_template('service_partymode/partymode-index.html')

# Handle the /settings-info route
@app.route('/search-for-user', methods=['POST'])
def search_for_user():
    
    username = request.form.get('username')
    
    user = user_db.get_user(username)
    
    if user:
        return render_template('service_partymode/partymode-index.html', result=user)

    else:
        return render_template('service_partymode/partymode-index.html', error='User not found')
    
@app.route('/invite-user/')
def invite_user():
    
    username = request.args.get('username')
    
    