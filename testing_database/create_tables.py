import psycopg2
from testing_database.config import config
 
 
def create_tables(users, entries):
    """create tables in the PostgreSQL database"""
    commands = (
        "CREATE TABLE IF NOT EXISTS {} (\
            user_id SERIAL PRIMARY KEY,\
            name VARCHAR(50) NOT NULL,\
            email VARCHAR(50) NOT NULL,\
            password VARCHAR(150) NOT NULL\
            )".format(users)
            ,
        "CREATE TABLE IF NOT EXISTS {} (\
            user_id INTEGER NOT NULL,\
            date VARCHAR(30) NOT NULL,\
            title VARCHAR(30),\
            content VARCHAR(500),\
            entry_id SERIAL PRIMARY KEY,\
            FOREIGN KEY (user_id)\
                REFERENCES Users (user_id)\
            )".format(entries)
            )
    conn = None
    try:
        # read the connection parameters
        # params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(database='users', user='postgres',
                                password='lefty3064', host='localhost',
                                port='5432')
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
