from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import user_db

class User(UserMixin):
    def __init__(self, username, picture):
        self.username = username
        self.picture =picture

    @staticmethod
    def get(username):
        # Implement a method to retrieve a user from your database based on the user_id
        # Return the User object if the user exists, or None if not found
        print('GETTING USER', username)
        user_data = user_db.get_user(username)
        print('GOT USER DATA', user_data)
        
        if user_data:
            username, picture = user_data[0], user_data[2]
            return User(username, picture)

        return None
    
    def get_id(self):
        return self.username
    
    def get_profile_pic(self):
        return self.picture
