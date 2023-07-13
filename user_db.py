from google.cloud.sql.connector import Connector
import sqlalchemy
import pymysql

# initialize Connector object
connector = Connector()

# function to return the database connection
def getconn() -> pymysql.connections.Connection:
    conn: pymysql.connections.Connection = connector.connect(
        "drawoff-391919:us-east4:drawoffdb",
        "pymysql",
        user="db-manager",
        password="RjMIUH6<}rxF);$6",
        db="drawings"
    )
    return conn

# create connection pool
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
    
)

# function to create table
def create_user_table():
    
    # create table
    create_stmt = sqlalchemy.text(
        "CREATE TABLE IF NOT EXISTS user_data (username VARCHAR(255) PRIMARY KEY, password VARCHAR(255), profilepic VARCHAR(255) )"
    )
    
    with pool.connect() as db_conn:
        
        # wipe table
        db_conn.execute(create_stmt)
        
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()
        

def create_user(username, password, profilepic):
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "SELECT COUNT(*) FROM user_data WHERE username = :username"
    )

    with pool.connect() as db_conn:
        result = db_conn.execute(select_stmt, {"username": username})
        count = result.scalar()

        if count > 0:
            # Username already exists, return False or raise an exception if desired
            return False

        # Insert statement
        insert_stmt = sqlalchemy.text(
            "INSERT INTO user_data (username, password, profilepic) VALUES (:username, :password, :profilepic)"
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

    with pool.connect() as db_conn:
        result = db_conn.execute(select_stmt)

        print(result.fetchall())

        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return True

        
def get_password_from_database(username):
    
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "SELECT password FROM user_data WHERE username = :username"
    )

    with pool.connect() as db_conn:
        result = db_conn.execute(select_stmt, {"username": username})
        password = result.fetchone()

        print(password)

        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return password


def get_user(username):
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "SELECT * FROM user_data WHERE username = :username"
    )

    with pool.connect() as db_conn:
        result = db_conn.execute(select_stmt, {"username": username})
        
        user = result.fetchone()

        print(user)

        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return user


def get_profile_pic(username):
    
    # Check if the username already exists
    select_stmt = sqlalchemy.text(
        "SELECT profilepic FROM user_data WHERE username = :username"
    )

    with pool.connect() as db_conn:
        result = db_conn.execute(select_stmt, {"username": username})
        pic = result.fetchone()

        print(pic)

        # Commit the transaction
        db_conn.commit()

    # User created successfully, return True or any other desired response
    return pic