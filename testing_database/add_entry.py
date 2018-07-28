import psycopg2
from config import config

def add_entry():
    """Add new User to User table"""
    User = {
            'user_id': 6, 'name': 'ron', 'email': 'ron@gmail.com', 'password': 'okay'
        }
    # column_header = []
    # column_data = []
    # for keys, data in User.items():
    #     column_header.append(keys)
    #     column_data.append(data)
    placeholders = ', '.join(['%s'] * len(User))
    columns = ', '.join(User.keys())
    parameters = config()
    conn = psycopg2.connect(**parameters)
    cur = conn.cursor()
    sql = '''INSERT INTO users ( %s ) VALUES ( %s )'''  % (columns, placeholders)
    cur.execute (sql, list(User.values()))
    conn.commit()
    cur.close()

if __name__ == '__main__':
    add_user()