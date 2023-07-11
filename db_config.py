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

# create table
create_stmt = sqlalchemy.text(
    "CREATE TABLE IF NOT EXISTS drawing_data (id VARCHAR(255) PRIMARY KEY, image VARCHAR(255), votes INT, message VARCHAR(255), word VARCHAR(255))"
)

# delete table
drop_stmt = sqlalchemy.text(
    "DROP TABLE drawing_data"
)

# wipe table
wipe_stmt = sqlalchemy.text(
    "DELETE FROM drawing_data"
)

# insert statement
insert_stmt = sqlalchemy.text(
    "INSERT INTO drawing_data (id, image, votes, message, word) VALUES (:id, :image, :votes, :message, :word)",
)

# function to create entry in database
def create_entry(id, image, votes, message, word):
    
    with pool.connect() as db_conn:
        
        # insert into database
        db_conn.execute(insert_stmt, parameters={"id": id, "image": image,
                                                 "votes": votes, "message": message, 'word': word})

        # query database
        # result = db_conn.execute(sqlalchemy.text("SELECT * from drawing_data")).fetchall()

        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()

        # Do something with the results
        #for row in result:
        #    print(row)

# function to create entry in database
def select_all():
    
    with pool.connect() as db_conn:

        # query database
        result = db_conn.execute(sqlalchemy.text("SELECT * from drawing_data")).fetchall()

        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()

        # Do something with the results
        # for row in result:
            # print(row)
            
    return result

# function to wipe table
def wipe_table():
    
    with pool.connect() as db_conn:
        
        # wipe table
        db_conn.execute(wipe_stmt)
        
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()
        
# function to drop table
def drop_table():
    
    with pool.connect() as db_conn:
        
        # wipe table
        db_conn.execute(drop_stmt)
        
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()
        
# function to create table
def create_table():
    
    with pool.connect() as db_conn:
        
        # wipe table
        db_conn.execute(create_stmt)
        
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()

        
# function to vote
def vote(id):
    # vote statement
    vote_stmt = sqlalchemy.text(
        "UPDATE drawing_data SET votes = votes + 1 WHERE id = :id"
    )
    
    print(id)

    with pool.connect() as db_conn:
        # execute the vote statement
        db_conn.execute(vote_stmt, {"id": id})

        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()

        # retrieve and print the updated row
        select_stmt = sqlalchemy.text(
            "SELECT * FROM drawing_data WHERE id = :id"
        )
        
        result = db_conn.execute(select_stmt, {"id": id})
        updated_row = result.fetchone()
        
        # print(updated_row)