from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from testing_database.add import add_entry, add_user
from testing_database.find_edit import find_entry, update_entry, delete_entry, find_entries
import os


class Users:
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


class Diary(Users):
    entries = []
    toekn_expiration = datetime.now()

    @staticmethod
    def add_entry(title, enter_content, user_id):
        '''create empty entry if entry has been used before'''
        # entry = {}
        date = datetime.now()
        content = enter_content
        new_entry = {
            "user_id": user_id,
            "date": date.strftime('%a.%d.%B.%Y'),
            "title": title,
            "content": content
        }
        add_entry(new_entry)
        return new_entry

    @staticmethod
    def find_entry_by_id(user_id, entry_id):
        entry = find_entry(user_id, entry_id)
        if entry: 
            return entry
        return 'No such entry'

    @staticmethod
    def modify_entry(user_id, entry_id, title, content):
        entry = find_entry(user_id, entry_id)
        if entry:
            update_entry(user_id, entry_id, title, content)
            return True
        return 'No such entry'

    @staticmethod
    def delete_entry(user_id, entry_id):
        entry = find_entry(user_id, entry_id)
        if entry:
            delete_entry(user_id, entry_id)
            return 'Entry deleted'
        return 'No such entry'

    @staticmethod
    def list_all_entries(user_id):
        entries = find_entries(user_id)
        if entries:
            return entries
        return 'No entries'
