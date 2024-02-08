from __main__  import app

from flask import render_template, request
from service_profile import user_db

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
    
    