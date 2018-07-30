from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from mydiary import login
import os


class Users(UserMixin):
    users = []
    count_user_id = 1
    token = ''

    '''Create hashes of user passwords, use next function to retrieve them'''
    @classmethod
    def set_password(cls, password):
        cls.password_hash = generate_password_hash(password)

    @staticmethod
    def check_password(password):
        return check_password_hash(Diary.set_password, password)
        
    @staticmethod
    def add_user(name, user_id, email, password, count_user_id):
        User = {
            'name': name,
            'email': email,
            'password': Users.set_password(password),
            'Userid': count_user_id
        }
        Users.count_user_id += 1
        Diary.users.append(User)
        return User

    @staticmethod
    def find_user_by_id(user_id):
        for user in Diary.entries:
            if user_id == user["ID"]:
                return user
        return 'No such entry'


class Diary(Users, UserMixin):
    entries = []
    users = []
    entry_id = 1
    toekn_expiration = datetime.now()

    @staticmethod
    def add_entry(user_id, enter_content):
        '''create empty entry if entry has been used before'''
        entry = {}
        date = datetime.now()
        content = enter_content
        new_entry = {
            "date": date.strftime('%A.%B.%Y'),
            "content": content,
            "entry_id": Diary.entry_id,
            "user_id": user_id

        }
        for entry in Diary.entries:
            if Diary.entries == []:
                Diary.entries.append(new_entry)
                return entry
            elif new_entry["content"] == entry["content"]:
                return "New entry is similar to older entry"
            else:
                entry["ID"] = entry["ID"] + 1
        Diary.entries.append(new_entry)
        return new_entry

    @staticmethod
    def find_entry_by_id(entry_id):
        for entry in Diary.entries:
            if entry_id == entry["ID"]:
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
