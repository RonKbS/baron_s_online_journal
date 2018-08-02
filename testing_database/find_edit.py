import os
import psycopg2
import psycopg2.extras
from testing_database.config import config


class db:
    def __init__(self):
        self.connection = os.environ.get('DATABASE_URI') or \
                        psycopg2.connect(database='users', user='postgres',
                                password='lefty3064', host='localhost',
                                port='5432')
        self.connection.autocommit = True

    def create_tables(self, users, entries):
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
        cur = self.connection.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()

        



def find_user_by_id(user_id):
    # parameters = config()
    connection = psycopg2.connect(database='users', user='postgres',
                                password='lefty3064', host='localhost',
                                port='5432')
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = "SELECT * FROM users WHERE user_id='{}'".format(user_id)
    cur.execute(sql)
    user = cur.fetchone()
    cur.close()
    return user


def find_user_by_name(name):
    # parameters = config()
    connection = psycopg2.connect(database='users', user='postgres',
                                password='lefty3064', host='localhost',
                                port='5432')
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = "SELECT * FROM users WHERE name='{}'".format(name)
    cur.execute(sql)
    user = cur.fetchone()
    cur.close()
    if user:
        return user
    return False


def find_entries(user_id):
    parameters = config()
    connection = psycopg2.connect(database='users', user='postgres',
                                password='lefty3064', host='localhost',
                                port='5432')
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = '''SELECT * FROM entries WHERE user_id=%s'''  % (user_id)
    cur.execute(sql)
    entries = cur.fetchall()
    cur.close()
    return entries


def find_entry(user_id, entry_id):
    # parameters = config()
    connection = psycopg2.connect(database='users', user='postgres',
                                password='lefty3064', host='localhost',
                                port='5432')
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = '''SELECT * FROM entries WHERE user_id=%s AND entry_id=%s'''  % (user_id, entry_id)
    cur.execute(sql)
    entry = cur.fetchone()
    cur.close()
    return entry


def update_entry(user_id, entry_id, title, content):
    # parameters = config()
    connection = psycopg2.connect(database='users', user='postgres',
                                password='lefty3064', host='localhost',
                                port='5432')
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = "UPDATE entries SET title ='{0}', content ='{1}' WHERE user_id='{2}' AND entry_id='{3}'".format(title, content, user_id, entry_id)
    cur.execute(sql)
    connection.commit()
    cur.close()


def delete_entry(user_id, entry_id):
    # parameters = config()
    connection = psycopg2.connect(database='users', user='postgres',
                                password='lefty3064', host='localhost',
                                port='5432')
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = "DELETE FROM entries WHERE user_id='{0}' AND entry_id='{1}'".format(user_id, entry_id)
    cur.execute(sql)
    connection.commit()
    cur.close()
