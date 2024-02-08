from google.cloud.sql.connector import Connector, IPTypes
import pytds
import sqlalchemy
import pymysql

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

def create_table():
    # create table
    create_stmt = sqlalchemy.text(
        "CREATE TABLE IF NOT EXISTS drawing_data (id VARCHAR(255) PRIMARY KEY, image VARCHAR(255), votes INT, message VARCHAR(255), word VARCHAR(255), user VARCHAR(255) )"
    )
    
    with connect_with_connector().connect() as db_conn:
        # wipe table
        db_conn.execute(create_stmt)
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()

def create_entry(id, image, votes, message, word, user):
    # insert statement
    insert_stmt = sqlalchemy.text(
        "INSERT INTO drawing_data (id, image, votes, message, word, user) VALUES (:id, :image, :votes, :message, :word, :user)"
    )

    with connect_with_connector().connect() as db_conn:
        # insert into database
        db_conn.execute(insert_stmt, parameters={"id": id, "image": image, "votes": votes, "message": message, 'word': word, 'user': user})
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()

def select_all(word):
    with connect_with_connector().connect() as db_conn:
        # query database
        result = db_conn.execute(sqlalchemy.text("SELECT * from drawing_data WHERE word = :word"), {'word' : word}).fetchall()
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()
    return result

def select_where_id(id):
    with connect_with_connector().connect() as db_conn:
        # query database
        result = db_conn.execute(sqlalchemy.text("SELECT * from drawing_data WHERE id = :id"), {'id' : id}).fetchall()
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()
    return result

def wipe_table():
    # wipe table
    wipe_stmt = sqlalchemy.text(
        "DELETE FROM drawing_data"
    )
    
    with connect_with_connector().connect() as db_conn:
        # wipe table
        db_conn.execute(wipe_stmt)
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()

def drop_table():
    # delete table
    drop_stmt = sqlalchemy.text(
        "DROP TABLE drawing_data"
    )
    
    with connect_with_connector().connect() as db_conn:
        # wipe table
        db_conn.execute(drop_stmt)
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()

def vote(id, vote):
    # vote statement
    vote_stmt = sqlalchemy.text(
        "UPDATE drawing_data SET votes = votes + :vote WHERE id = :id"
    )
    
    with connect_with_connector().connect() as db_conn:
        # execute the vote statement
        db_conn.execute(vote_stmt, {"id": id, "vote": vote})
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()
        # retrieve and print the updated row
        select_stmt = sqlalchemy.text(
            "SELECT * FROM drawing_data WHERE id = :id"
        )
        result = db_conn.execute(select_stmt, {"id": id})
        updated_row = result.fetchone()
        # print(updated_row)

def select_where_user(user):
    with connect_with_connector().connect() as db_conn:
        # query database
        result = db_conn.execute(sqlalchemy.text("SELECT * from drawing_data WHERE user = :user"), {'user' : user}).fetchall()
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()
    return result

def delete_row_by_id(id):
    # delete statement
    delete_stmt = sqlalchemy.text(
        "DELETE FROM drawing_data WHERE id = :id"
    )

    with connect_with_connector().connect() as db_conn:
        # delete the row with the given id
        db_conn.execute(delete_stmt, {"id": id})
        # commit transaction (SQLAlchemy v2.X.X is commit as you go)
        db_conn.commit()

create_table()
