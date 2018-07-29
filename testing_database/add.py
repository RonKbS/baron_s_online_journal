import psycopg2
from config import config

def add_entry_or_user(User_or_entry):
    """Add new User to User table"""
    placeholders = ', '.join(['%s'] * len(User_or_entry))
    columns = ', '.join(User_or_entry.keys())
    parameters = config()
    connection = psycopg2.connect(**parameters)
    cur = connection.cursor()
    sql = '''INSERT INTO entries ( %s ) VALUES ( %s )'''  % (columns, placeholders)
    cur.execute (sql, list(User_or_entry.values()))
    connection.commit()
    cur.close()
