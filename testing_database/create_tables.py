import psycopg2
from config import config
 
 
def create_tables():
    """create tables in the PostgreSQL database"""
    commands = (
        '''CREATE TABLE Users (
            user_id INTEGER NOT NULL UNIQUE,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(50) NOT NULL,
            password VARCHAR(25) NOT NULL
            )
            ''',
        '''CREATE TABLE Entries (
            user_id INTEGER NOT NULL,
            date VARCHAR(15) NOT NULL,
            content VARCHAR(500),
            entry_id INTEGER NOT NULL,
            FOREIGN KEY (user_id)
                REFERENCES Users (user_id)
            )
            ''')
    # (
    #     """
    #     DROP TABLE vendors CASCADE
    #     """,
    #     """ DROP TABLE parts CASCADE
    #     """,
    #     """
    #     DROP TABLE part_drawings
    #     """,
    #     """
    #     DROP TABLE vendor_parts
    #     """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
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
 
 
if __name__ == '__main__':
    create_tables()