import psycopg2
import psycopg2.extras
'''Remove the testing_database namespace when running the file alone'''
from testing_database.config import config

def find_user_by_id(user_id):
    parameters = config()
    connection = psycopg2.connect(**parameters)
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "SELECT * FROM users WHERE user_id='{}'".format(user_id)
    cur.execute(sql)
    user = cur.fetchone()
    connection.commit()
    cur.close()
    return user

def find_user_by_name(name):
    parameters = config()
    connection = psycopg2.connect(**parameters)
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = "SELECT * FROM users WHERE name='{}'".format(name)
    cur.execute(sql)
    user = cur.fetchone()
    connection.commit()
    cur.close()
    return user


# def find_entries:


def find_entry(user_id, entry_id):
    parameters = config()
    connection = psycopg2.connect(**parameters)
    cur = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    sql = '''SELECT * FROM entries WHERE user_id=%s AND entry_id=%s'''  % (user_id, entry_id)
    cur.execute(sql)
    entry = cur.fetchone()
    connection.commit()
    cur.close()
    return entry

# if __name__ == '__main__':
#     find_entry()
