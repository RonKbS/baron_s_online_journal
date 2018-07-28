from datetime import datetime
import psycopg2
from config import Config


def create_cursor(choice):
    '''Read connection parameters'''
    params = Config.config()
    '''Connect to the postgresql serve'''
    connection = psycopg2.connect(**params)
    if choice == 'close':
        connection.commit()
        connection.close()
        return connection
    return connection.cursor()


def make_connection(choice):
    cur = create_cursor('open')
    if choice == 'close':
        return cur.close()
    return cur


def create_tables():
    '''Creating User and Diary tables in postgreSQL
        database'''
    tables = ('''CREATE TABLE Users(user_id INTEGER,
                                   name VARCHAR(50), email VARCHAR(50),
                                   password VARCHAR(25)
                                   ) ''',
              '''CREATE TABLE Entries(user_id INTEGER NOT NULL,
                                      date VARCHAR(15),
                                      content VARCHAR(500),
                                      entry_id INTEGER,
                                      user_id INTEGER,
                                      FOREIGN KEY (user_id)
                                    ) ''')
    params = Config.config()
    connection = psycopg2.connect(**params)
    cur = connection.cursor()
    for table in tables:
        cur.execute(table)
        connection.commit()
        cur.close()
        connection.close()


entries = []
entry_id = 1
users = []
count_user_id = 1


class User:
    def __init__(self, name, email, password, user_id):
        self.name = name
        self.email = email
        self.password = password
        self.user_id = count_user_id

    
    def add_user(self, user_id, count_user_id):
        User = {
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'UserID': count_user_id
        }
        count_user_id += 1

        '''Add user to PostgreSQL User table'''
        add_user_sql = '''INSERT INTO Users(user_id, name,
                     email, password)'''
        params = Config.config()
        connection = psycopg2.connect(**params)
        cur = connection.cursor()
        cur.execute(add_user_sql, (User['name'], User['email'],
         User['password'], User['UserID']))
        connection.commit()
        cur.close()
        connection.close()

        return User

class Diary(User):

    @staticmethod
    def add_entry(enter_content):
        '''create empty entry if entry has been used before'''
        entry = {}
        date = datetime.now()
        content = enter_content
        new_entry = {
            "date": date.strftime('%A.%B.%Y'),
            "content": content,
            "ID": entry_id,
            "UserID": super.User.user_id
        }

        '''Add entry to Entries table in PostgreSQL table'''
        add_entry_sql = '''INSERT INTO Entries(user_id, date,
                     content, entry_id)'''
        params = Config.config()
        connection = psycopg2.connect(**params)
        cur = connection.cursor()
        cur.execute(add_entry_sql, (new_entry['date'], new_entry['content'],
                    new_entry['ID'], new_entry['UserID']))
        connection.commit()
        cur.close()
        connection.close()
        return new_entry

    @staticmethod
    def find_entry_by_id(user_id ,entry_id):
        params = Config.config()
        connect = psycopg2.connect(**params)
        cur = connect.cursor()
        entry = cur.execute('''SELECT * FROM Entries WHERE user_id = %s AND entry_id = %s''',
                            (user_id, entry_id))
        cur.close()
        connect.close()
        if entry != []:
            return entry
        return 'No such entry'

    
    
    @staticmethod
    def modify_entry(entry_id, content):
        '''Modify entry in PostgreSQL Entries table'''
        modify_entry_sql = ''' UPDATE Entries SET content = %s
                              WHERE content = %s'''
        params = Config.config()
        connection = psycopg2.connect(**params)
        cur = connection.cursor()
        cur.execute(modify_entry_sql, (content))

    @staticmethod
    def delete_entry(entry_id):
        for entry in entries:
            if entry_id == entry['ID']:
                entries.remove(entry)
                return "Entry deleted"
        return 'No such entry'

    @staticmethod
    def list_all_entries():
        if entries != []:
            return entries
        return 'No entries'
