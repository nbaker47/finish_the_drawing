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
    "CREATE TABLE IF NOT EXISTS drawing_data (id VARCHAR(255) PRIMARY KEY, image BLOB, votes INT, message VARCHAR(255))"
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
    "INSERT INTO drawing_data (id, image, votes, message) VALUES (:id, :image, :votes, :message)",
)

with pool.connect() as db_conn:
    
    # drop table
    db_conn.execute(drop_stmt)
    
    # create table
    db_conn.execute(create_stmt)
    
    # insert into database
    db_conn.execute(insert_stmt, parameters={"id": "test_id", "image": "test_image", "votes": 0, "message": "test_message"})

    # query database
    result = db_conn.execute(sqlalchemy.text("SELECT * from drawing_data")).fetchall()

    # commit transaction (SQLAlchemy v2.X.X is commit as you go)
    db_conn.commit()

    # Do something with the results
    for row in result:
        print(row)