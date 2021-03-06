import os
import re
import psycopg2
import psycopg2.extras
from app import app, mail
from datetime import datetime
from pyisemail import is_email
from flask_mail import Message


def message(sender, recipient, name):
    msg = Message(
        subject="MyDiary Reminder", sender=sender,\
        recipients=recipient.split())
    msg.body = 'Hello, ' + name + '. It\'s that time again!\nCheckout your diary and save any highlights you\'ve had today.'
    with app.app_context():
        mail.send(msg)


class db:
    def __init__(self):
        self.connection = app.config['connection']
        # psycopg2.connect(
        #     'postgresql://postgres:lefty3064@localhost:5432')
        self.connection.autocommit = True

    def create_tables(self, users, entries, notifications):
        """create tables in the PostgreSQL database"""
        commands = (
            "CREATE TABLE IF NOT EXISTS {} (\
            user_id SERIAL PRIMARY KEY,\
            name VARCHAR(50) NOT NULL,\
            email VARCHAR(50) NOT NULL,\
            password VARCHAR(150) NOT NULL\
            )".format(users),
            "CREATE TABLE IF NOT EXISTS {} (\
            title VARCHAR(30),\
            user_id INTEGER NOT NULL,\
            date VARCHAR(30) NOT NULL,\
            content VARCHAR(500),\
            entry_id SERIAL PRIMARY KEY,\
            FOREIGN KEY (user_id)\
                REFERENCES Users (user_id)\
            )".format(entries),
            "CREATE TABLE IF NOT EXISTS {} (\
            user_id INTEGER NOT NULL,\
            Monday BOOLEAN DEFAULT false,\
            Tuesday BOOLEAN DEFAULT false,\
            Wednesday BOOLEAN DEFAULT false,\
            Thursday BOOLEAN DEFAULT false,\
            Friday BOOLEAN DEFAULT false,\
            Saturday BOOLEAN DEFAULT false,\
            Sunday BOOLEAN DEFAULT false,\
            FOREIGN KEY (user_id)\
                REFERENCES Users (user_id)\
            )".format(notifications)
        )
        cur = self.connection.cursor()
        for command in commands:
            cur.execute(command)
        cur.close()

    def send_email(self):
        cur = self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        #Get all the names from users table
        sql = '''SELECT name, email, user_id FROM users'''
        cur.execute(sql)
        names = cur.fetchall()

        sql2 = '''SELECT * FROM notifications'''
        cur.execute(sql2)
        notifications = cur.fetchall()
        cur.close()

        days = ['monday', 'tuesday', 'wednesday', 'thursday'\
                , 'friday', 'saturday', 'sunday']
        date = datetime.now()
        for day in days:
            if date.strftime('%A').lower() == day:
                for name, notification in zip(names, notifications):
                    if notification[day] == True:
                        message(app.config['ADMINS'][0], name['email'], name['name'])

    @staticmethod
    def reg_ex(word):
        u_name = re.compile(r'^[a-zA-Z_]*$')
        p_word = re.compile(r'^[a-zA-Z0-9_]*$')
        if u_name.match(word) or p_word.match(word):
            return True
        return False

    @staticmethod
    def adds(entry):
        """Add new entry to entry table"""
        placeholders = ', '.join(['%s'] * len(entry))
        columns = ', '.join(entry.keys())
        ob = db()
        cur = ob.connection.cursor()
        if len(entry) == 4:
            sql = '''INSERT INTO entries ( %s ) VALUES ( %s )''' % (
            columns, placeholders)
            cur.execute(sql, list(entry.values()))
        elif len(entry) < 4:
            sql = '''INSERT INTO users ( %s ) VALUES ( %s )''' % (
                columns, placeholders)
            cur.execute(sql, list(entry.values()))
            user = db.find_user_by_name(entry['name'])
            notifs = '''INSERT INTO notifications VALUES ( %s )''' % (
                user['user_id'])
            cur.execute(notifs)
        cur.close()

    @staticmethod
    def find_user_by_id(user_id):
        ob = db()
        cur = ob.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = "SELECT * FROM users WHERE user_id='{}'".format(user_id)
        cur.execute(sql)
        user = cur.fetchone()
        cur.close()
        if user:
            return user
        return False

    @staticmethod
    def find_user_by_name(name):
        ob = db()
        cur = ob.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = "SELECT * FROM users WHERE name='{}'".format(name)
        cur.execute(sql)
        user = cur.fetchone()
        cur.close()
        if user:
            return user
        return False

    @staticmethod
    def set_notifs(day, val, user_id):
        ob = db()
        cur = ob.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = "UPDATE notifications SET %s=%s WHERE user_id=%s" % (day, val, user_id)
        cur.execute(sql)
        cur.close()
    
    @staticmethod
    def get_notifs(user_id):
        '''Return a dictionary of user_id and days'''
        ob = db()
        cur = ob.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = "SELECT * FROM notifications WHERE user_id=%s" % (user_id)
        cur.execute(sql)
        notifs = cur.fetchall()
        cur.close()
        return notifs

    @staticmethod
    def find_entries(user_id):
        ob = db()
        cur = ob.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = '''SELECT * FROM entries WHERE user_id=%s''' % (user_id)
        cur.execute(sql)
        entries = cur.fetchall()
        cur.close()
        return entries

    @staticmethod
    def find_entry(user_id, entry_id):
        ob = db()
        cur = ob.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = \
        '''SELECT * FROM entries WHERE user_id=%s AND entry_id=%s''' % (
            user_id, entry_id)
        cur.execute(sql)
        entry = cur.fetchone()
        cur.close()
        return entry

    @staticmethod
    def update_entry(user_id, entry_id, title, content):
        ob = db()
        cur = ob.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = "UPDATE entries SET title ='{0}', content ='{1}' WHERE user_id='{2}' AND entry_id='{3}'"\
                .format(title, content, user_id, entry_id)
        cur.execute(sql)
        cur.close()

    @staticmethod
    def update_user_details(user_id, detail):
        ob = db()
        cur = ob.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        if detail is not None and is_email(detail):
            sql = "UPDATE users SET email ='{0}' WHERE user_id='{1}'".format(detail, user_id)
            cur.execute(sql)
        elif detail is not None and not is_email(detail):
            sql = "UPDATE users SET password ='{0}' WHERE user_id='{1}'".format(detail, user_id)
            cur.execute(sql)
        cur.close()

    @staticmethod
    def deletes(user_id, entry_id):
        ob = db()
        cur = ob.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        sql = \
        "DELETE FROM entries WHERE user_id='{0}' AND entry_id='{1}'"\
        .format(user_id, entry_id)
        cur.execute(sql)
        cur.close()
