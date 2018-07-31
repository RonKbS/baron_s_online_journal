from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from testing_database.add import add_entry, add_user
from testing_database.find_edit import find_entry
import os


class Users(UserMixin):
    '''Create hashes of user passwords, use next function to retrieve them'''
    @staticmethod
    def set_password(password):
        password_hash = generate_password_hash(password)
        return password_hash

    @staticmethod
    def check_password(saved_password, sent_password):
        return check_password_hash(saved_password, sent_password)
        
    @staticmethod
    def add_user(name, email, password):
        User = {
            'name': name,
            'email': email,
            'password': password
        }
        add_user(User)
        return User

    @staticmethod
    def find_user_by_id(user_id):
        for user in Diary.entries:
            if user_id == user["ID"]:
                return user
        return 'No such entry'


class Diary(Users, UserMixin):
    entries = []
    entry_id = 1
    toekn_expiration = datetime.now()

    @staticmethod
    def add_entry(enter_content, user_id):
        '''create empty entry if entry has been used before'''
        # entry = {}
        date = datetime.now()
        content = enter_content
        new_entry = {
            "user_id": 1,
            "date": date.strftime('%a.%d.%B.%Y'),
            "content": content,
            "entry_id": Diary.entry_id

        }
        Diary.entry_id = Diary.entry_id + 1
        add_entry(new_entry)
        return new_entry

    @staticmethod
    def find_entry_by_id(user_id, entry_id):
        entry = find_entry(user_id, entry_id)
        if entry:
            return entry
        return 'No such entry'

    @staticmethod
    def modify_entry(user_id, entry_id, content):
        for entry in Diary.entries:
            if entry_id == entry["ID"]:
                entry["content"] = content
                return entry
        return 'No such entry'

    @staticmethod
    def delete_entry(user_id, entry_id):
        for entry in Diary.entries:
            if entry_id == entry['ID']:
                Diary.entries.remove(entry)
                return "Entry deleted"
        return 'No such entry'

    @staticmethod
    def list_all_entries(user_id):
        if Diary.entries != []:
            return Diary.entries
        return 'No entries'
