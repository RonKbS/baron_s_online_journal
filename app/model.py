from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from database.queries import db
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
        db.adds(User)
        return User

    @staticmethod
    def modify_detail(user_id, detail):
        db.update_user_details(user_id, detail)

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
        '''create new entry for a specific user'''
        date = datetime.now()
        content = enter_content
        new_entry = {
            "user_id": user_id,
            "date": date.strftime('%a.%d.%B.%Y'),
            "title": title,
            "content": content
        }
        db.adds(new_entry)
        return new_entry

    @staticmethod
    def find_entry_by_id(user_id, entry_id):
        entry = db.find_entry(user_id, entry_id)
        if entry: 
            return entry
        return 'No such entry'

    @staticmethod
    def modify_entry(user_id, entry_id, title, content):
        entry = db.find_entry(user_id, entry_id)
        if entry:
            db.update_entry(user_id, entry_id, title, content)
            return True
        return 'No such entry'

    @staticmethod
    def delete_entry(user_id, entry_id):
        entry = db.find_entry(user_id, entry_id)
        if entry:
            db.deletes(user_id, entry_id)
            return 'Entry deleted'
        return 'No such entry'

    @staticmethod
    def list_all_entries(user_id):
        entries = db.find_entries(user_id)
        if entries:
            return entries
        return 'No entries'
