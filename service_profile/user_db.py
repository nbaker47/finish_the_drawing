from google.cloud.sql.connector import Connector
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes
import pytds
import sqlalchemy
import pymysql

# python -c 'from service_profile.user_db import *; drop_table();'

def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    instance_connection_name = 'finish-the-drawing-413709:asia-east1:draw'
    db_user = 'root'
    db_pass = 'root' 
    db_name = 'draw'

    connector = Connector()
    
    def getconn() -> pytds.Connection:
        conn = connector.connect(
            instance_connection_name,
            "pymysql",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
        return conn

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
    )
    return pool


# function to create table
def create_user_table():
    
    # create table
    create_stmt = sqlalchemy.text(
        "CREATE TABLE IF NOT EXISTS user_data (username VARCHAR(255) PRIMARY KEY, password VARCHAR(255), profilepic VARCHAR(255), role VARCHAR(255), background VARCHAR(255) )"
    )
    
    with connect_with_connector().connect() as db_conn:
        
        # wipe table
        db_conn.execute(create_stmt)
        
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()
        

def create_user(username, password, profilepic):
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "SELECT COUNT(*) FROM user_data WHERE username = :username"
    )

    with connect_with_connector().connect() as db_conn:
        result = db_conn.execute(select_stmt, {"username": username})
        count = result.scalar()

        if count > 0:
            # Username already exists, return False or raise an exception if desired
            return False

        # Insert statement
        insert_stmt = sqlalchemy.text(
            "INSERT INTO user_data (username, password, profilepic, role) VALUES (:username, :password, :profilepic, 'artist')"
        )

        # Insert the new user data into the table
        db_conn.execute(insert_stmt, {"username": username, "password": password, "profilepic": profilepic})

        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return True


def list_users():
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "SELECT * FROM user_data"
    )

    with connect_with_connector().connect() as db_conn:
        result = db_conn.execute(select_stmt)


        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return True

        
def get_password_from_database(username):
    
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "SELECT password FROM user_data WHERE username = :username"
    )

    with connect_with_connector().connect() as db_conn:
        result = db_conn.execute(select_stmt, {"username": username})
        password = result.fetchone()


        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return password


def get_user(username):
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "SELECT * FROM user_data WHERE username = :username"
    )

    with connect_with_connector().connect() as db_conn:
        result = db_conn.execute(select_stmt, {"username": username})
        
        user = result.fetchone()

        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return user


def get_profile_pic(username):
    
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "SELECT profilepic FROM user_data WHERE username = :username"
    )

    with connect_with_connector().connect() as db_conn:
        result = db_conn.execute(select_stmt, {"username": username})
        pic = result.fetchone()


        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return pic

def get_background(username):
    
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "SELECT background FROM user_data WHERE username = :username"
    )

    with connect_with_connector().connect() as db_conn:
        result = db_conn.execute(select_stmt, {"username": username})
        pic = result.fetchone()

        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return pic

def update_profile_pic(username, profilepic):
    
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "UPDATE user_data SET profilepic = :profilepic WHERE username = :username"
    )

    with connect_with_connector().connect() as db_conn:
        db_conn.execute(select_stmt, {"username": username, "profilepic": profilepic})

        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return 

def update_background(username, background):
    
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "UPDATE user_data SET background = :background WHERE username = :username"
    )

    with connect_with_connector().connect() as db_conn:
        db_conn.execute(select_stmt, {"username": username, "background": background})

        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return 

def add_column():
    
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "ALTER TABLE user_data ADD COLUMN background VARCHAR(255);"
    )

    with connect_with_connector().connect() as db_conn:
        db_conn.execute(select_stmt)

        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return 


def set_role_artist(username):
    
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "UPDATE user_data SET role = 'artist' WHERE username = :username;"
    )

    with connect_with_connector().connect() as db_conn:
        db_conn.execute(select_stmt, {"username": username})

        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return 

def set_role_admin(username):
    
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "UPDATE user_data SET role = 'ace artist' WHERE username = :username;"
    )

    with connect_with_connector().connect() as db_conn:
        db_conn.execute(select_stmt, {"username": username})

        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return 


def is_admin(username):
    
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "SELECT role FROM user_data WHERE username = :username;"
    )

    with connect_with_connector().connect() as db_conn:
        result = db_conn.execute(select_stmt, {"username": username})
        
        try:
            role = result.fetchone()[0]
        except:
            role = "not ace artist"
        
        # Commit the transaction
        db_conn.commit()
        
    if role == "ace artist":
        return True

    # User created successfully, return True or any other desired response
    return False

def drop_table():
    # delete table
    drop_stmt = sqlalchemy.text(
        "DROP TABLE user_data"
    )
    
    with connect_with_connector().connect() as db_conn:
        # wipe table
        db_conn.execute(drop_stmt)
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()

def get_hall_of_fame():
    # Get the ordered list of users based on the total number of drawings
    select_stmt_drawings = sqlalchemy.text(
        "SELECT user, COUNT(*) AS total_drawings FROM drawing_data GROUP BY user ORDER BY total_drawings DESC"
    )
    
    select_stmt_votes = sqlalchemy.text(
        "SELECT user, SUM(votes) AS total_votes FROM drawing_data GROUP BY user ORDER BY total_votes DESC"
    )

    with connect_with_connector().connect() as db_conn:
        result_drawings = db_conn.execute(select_stmt_drawings)
        users_drawings = result_drawings.fetchall()

        result_votes = db_conn.execute(select_stmt_votes)
        users_votes = result_votes.fetchall()
        
        # Merge the lists based on username
        merged_users = []
        for user_drawings in users_drawings:
            for user_votes in users_votes:
                if user_drawings[0] == user_votes[0]:
                    merged_users.append((user_drawings[0], user_drawings[1], user_votes[1]))
                    break

        # Pass the merged users list as context to the template
        return merged_users
    

create_user_table()