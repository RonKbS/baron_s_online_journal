import os
import psycopg2
import psycopg2.extras


class db:
    def __init__(self, connection):
        self.connection = connection
        # psycopg2.connect(
        #     'postgresql://postgres:lefty3064@localhost:5432')
        # self.connection.autocommit = True

    def create_tables(self, users, entries):
        """create tables in the PostgreSQL database"""
        commands = (
            "CREATE TABLE IF NOT EXISTS {} (\
            user_id SERIAL PRIMARY KEY,\
            name VARCHAR(50) NOT NULL,\
            email VARCHAR(50) NOT NULL,\
            password VARCHAR(150) NOT NULL\
            )".format(users),
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
        self.connection.commit()
        cur.close()
        self.connection.close()

    def adds(self, entry):
        """Add new entry to entry table"""
        placeholders = ', '.join(['%s'] * len(entry))
        columns = ', '.join(entry.keys())
        cur = self.connection.cursor()
        sql = '''INSERT INTO entries ( %s ) VALUES ( %s )''' % (
            columns, placeholders)
        cur.execute(sql, list(entry.values()))
        self.connection.commit()
        cur.close()
        self.connection.close()

    def adds_a(self, user):
        """Add new usser to user table"""
        placeholders = ', '.join(['%s'] * len(user))
        columns = ', '.join(user.keys())
        cur = self.connection.cursor()
        sql = '''INSERT INTO users ( %s ) VALUES ( %s )''' % (
            columns, placeholders)
        cur.execute(sql, list(user.values()))
        self.connection.commit()
        cur.close()
        self.connection.close()

    def find_user_by_id(self, user_id):
        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = "SELECT * FROM users WHERE user_id='{}'".format(user_id)
        cur.execute(sql)
        user = cur.fetchone()
        cur.close()
        self.connection.close()
        return user

    def find_user_by_name(self, name):
        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = "SELECT * FROM users WHERE name='{}'".format(name)
        cur.execute(sql)
        user = cur.fetchone()
        cur.close()
        self.connection.close()
        if user:
            return user
        return False

    def find_entries(self, user_id):
        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = '''SELECT * FROM entries WHERE user_id=%s''' % (user_id)
        cur.execute(sql)
        entries = cur.fetchall()
        self.connection.close()
        cur.close()
        return entries

    def find_entry(self, user_id, entry_id):
        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = '''SELECT * FROM entries WHERE user_id=%s AND entry_id=%s''' % (
            user_id, entry_id)
        cur.execute(sql)
        entry = cur.fetchone()
        cur.close()
        return entry

    def update_entry(self, user_id, entry_id, title, content):
        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = "UPDATE entries SET title ='{0}', content ='{1}\
                ' WHERE user_id='{2}' AND entry_id='{3}'".format(title, content, user_id, entry_id)
        cur.execute(sql)
        self.connection.commit()
        cur.close()
        self.connection.close()

    def deletes(self, user_id, entry_id):
        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = "DELETE FROM entries WHERE user_id='{0}' AND entry_id='{1}'".format(
            user_id, entry_id)
        cur.execute(sql)
        self.connection.commit()
        cur.close()
        self.connection.close()
