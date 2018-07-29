from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from mydiary import login
import os
import base64


'''Note that user model has not been included
which will enable more distinguishing between
several users'''


@login.user_loader
def load_diary(id):
    return int(Diary.count_user_id)

class Diary(UserMixin):
    entries = []
    users = []
    entry_id = 1
    users = []
    count_user_id = 1
    token = ''
    toekn_expiration = datetime.now()

    '''Return token to a user'''
    def get_token(self, expires_in = 1800):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds = 1)

    @staticmethod
    def check_token(token):
        for user in Diary.users:
            if user['token'] == token and user.token_expiration < datetime.utcnow():
                return None
        return user

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
            'password': Diary.set_password(password),
            'token': Diary.get_token,
            'Userid': Diary.count_user_id
        }
        Diary.count_user_id += 1
        Diary.users.append(User)
        return User

    @staticmethod
    def add_entry(enter_content):
        '''create empty entry if entry has been used before'''
        entry = {}
        date = datetime.now()
        content = enter_content
        new_entry = {
            "date": date.strftime('%A.%B.%Y'),
            "content": content,
            "entry_id": Diary.entry_id,
            "user_id": Diary.count_user_id

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
    def modify_entry(entry_id, content):
        for entry in Diary.entries:
            if entry_id == entry["ID"]:
                entry["content"] = content
                return entry
        return 'No such entry'

    @staticmethod
    def delete_entry(entry_id):
        for entry in Diary.entries:
            if entry_id == entry['ID']:
                Diary.entries.remove(entry)
                return "Entry deleted"
        return 'No such entry'

    @staticmethod
    def list_all_entries():
        if Diary.entries != []:
            return Diary.entries
        return 'No entries'
