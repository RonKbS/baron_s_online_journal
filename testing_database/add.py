import psycopg2
from testing_database.config import config

def add_entry(entry):
    """Add new User to User table"""
    placeholders = ', '.join(['%s'] * len(entry))
    columns = ', '.join(entry.keys())
    parameters = config()
    connection = psycopg2.connect(**parameters)
    cur = connection.cursor()
    # sql = '''INSERT INTO entries (user_id, date, content, entry_id) VALUES (%s, %s, %s, %s))'''
    sql = '''INSERT INTO entries ( %s ) VALUES ( %s )'''  % (columns, placeholders)
    # cur.execute (sql, entry['user_id'], entry['date'], entry['content'], entry['entry_id'])
    cur.execute (sql, list(entry.values()))
    connection.commit()
    cur.close()

def add_user(user):
    """Add new User to User table"""
    placeholders = ', '.join(['%s'] * len(user))
    columns = ', '.join(user.keys())
    parameters = config()
    conn = psycopg2.connect(**parameters)
    cur = conn.cursor()
    sql = '''INSERT INTO users ( %s ) VALUES ( %s )'''  % (columns, placeholders)
    cur.execute (sql, list(user.values()))
    conn.commit()
    cur.close()

# if __name__ == '__main__':
#     add_user()