import psycopg2
import psycopg2.extras
from testing_database.config import config


def find_user_by_id(user_id):
    parameters = config()
    connection = psycopg2.connect(**parameters)
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = "SELECT * FROM users WHERE user_id='{}'".format(user_id)
    cur.execute(sql)
    user = cur.fetchone()
    cur.close()
    return user


def find_user_by_name(name):
    parameters = config()
    connection = psycopg2.connect(**parameters)
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
    connection = psycopg2.connect(**parameters)
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = '''SELECT * FROM entries WHERE user_id=%s'''  % (user_id)
    cur.execute(sql)
    entries = cur.fetchall()
    cur.close()
    return entries


def find_entry(user_id, entry_id):
    parameters = config()
    connection = psycopg2.connect(**parameters)
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = '''SELECT * FROM entries WHERE user_id=%s AND entry_id=%s'''  % (user_id, entry_id)
    cur.execute(sql)
    entry = cur.fetchone()
    cur.close()
    return entry


def update_entry(user_id, entry_id, title, content):
    parameters = config()
    connection = psycopg2.connect(**parameters)
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = "UPDATE entries SET title ='{0}', content ='{1}' WHERE user_id='{2}' AND entry_id='{3}'".format(title, content, user_id, entry_id)
    cur.execute(sql)
    connection.commit()
    cur.close()


def delete_entry(user_id, entry_id):
    parameters = config()
    connection = psycopg2.connect(**parameters)
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = "DELETE FROM entries WHERE user_id='{0}' AND entry_id='{1}'".format(user_id, entry_id)
    cur.execute(sql)
    connection.commit()
    cur.close()
